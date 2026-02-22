const express = require("express");
const { execSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
app.use(express.json());

const PORT = 3001;
const API_KEY = process.env.NOTION_API_KEY || "";
const TRACKER_DB = "30a5308b-6bc5-8171-a2c3-d89200293d13";
const DASHBOARD_PATH = path.resolve(__dirname, "../../Docs/dashboard.html");
const GENERATOR_PATH = path.resolve(__dirname, "../generate-dashboard.py");

// ─── Notion helpers ───

function notionRequest(method, endpoint, body) {
  const args = [
    "curl", "-s", "-X", method,
    `https://api.notion.com/v1/${endpoint}`,
    "-H", `Authorization: Bearer ${API_KEY}`,
    "-H", "Notion-Version: 2022-06-28",
    "-H", "Content-Type: application/json",
  ];
  if (body) args.push("-d", JSON.stringify(body));
  const result = execSync(args.map(a => `'${a.replace(/'/g, "'\\''")}'`).join(" "), {
    shell: true, encoding: "utf-8", timeout: 15000,
  });
  return JSON.parse(result);
}

function queryActiveTasks() {
  const data = notionRequest("POST", `databases/${TRACKER_DB}/query`, {
    page_size: 100,
    filter: {
      and: [
        { property: "Level", select: { equals: "Task" } },
        { property: "Status", select: { does_not_equal: "Done" } },
      ],
    },
  });
  return data.results.map(p => {
    const pr = p.properties;
    return {
      id: p.id,
      name: (pr.Name?.title || []).map(t => t.plain_text).join(""),
      status: pr.Status?.select?.name || "",
      owner: pr.Owner?.select?.name || "",
      department: pr.Department?.select?.name || "",
      due: pr.Due?.date?.start || "",
      progress: pr.Progress?.number || 0,
      parentIds: (pr.Parent?.relation || []).map(r => r.id),
    };
  });
}

function updateTask(pageId, updates) {
  const properties = {};
  if (updates.status) {
    properties.Status = { select: { name: updates.status } };
  }
  if (updates.progress !== undefined) {
    properties.Progress = { number: updates.progress };
  }
  return notionRequest("PATCH", `pages/${pageId}`, { properties });
}

function recalcParentProgress(parentId) {
  // Query children of this parent
  const data = notionRequest("POST", `databases/${TRACKER_DB}/query`, {
    page_size: 100,
    filter: { property: "Parent", relation: { contains: parentId } },
  });
  const children = data.results;
  if (!children.length) return;
  const avg = children.reduce((sum, c) => sum + (c.properties.Progress?.number || 0), 0) / children.length;
  notionRequest("PATCH", `pages/${parentId}`, {
    properties: { Progress: { number: Math.round(avg * 100) / 100 } },
  });
}

function regenerateDashboard() {
  try {
    execSync(`python3 '${GENERATOR_PATH}'`, { encoding: "utf-8", timeout: 30000, env: { ...process.env, VRT_NO_OPEN: "1" } });
    return true;
  } catch {
    return false;
  }
}

// ─── Command parser ───

// Intent keywords
const DONE_WORDS = ["done", "finished", "completed", "did", "delivered", "shipped"];
const START_WORDS = ["started", "working on", "beginning", "starting"];
const BLOCKED_WORDS = ["blocked", "stuck", "waiting", "can't"];

function parseIntent(message) {
  const lower = message.toLowerCase();
  if (DONE_WORDS.some(w => lower.includes(w))) return "Done";
  if (BLOCKED_WORDS.some(w => lower.includes(w))) return "Blocked";
  if (START_WORDS.some(w => lower.includes(w))) return "In Progress";
  return null;
}

function fuzzyMatch(query, tasks) {
  const lower = query.toLowerCase();
  // Remove common filler words and intent words
  const stopWords = [
    "i", "my", "the", "a", "an", "for", "to", "with", "on", "today", "just", "now",
    ...DONE_WORDS, ...START_WORDS, ...BLOCKED_WORDS,
  ];
  const keywords = lower.split(/\s+/).filter(w => w.length > 2 && !stopWords.includes(w));
  if (!keywords.length) return [];

  return tasks
    .map(task => {
      const taskLower = task.name.toLowerCase();
      const matchCount = keywords.filter(kw => taskLower.includes(kw)).length;
      const score = matchCount / keywords.length;
      return { ...task, score };
    })
    .filter(t => t.score > 0)
    .sort((a, b) => b.score - a.score);
}

// ─── Chat history (in-memory, recent 50) ───
const chatHistory = [];

// ─── Routes ───

// Serve dashboard
app.get("/", (req, res) => {
  if (fs.existsSync(DASHBOARD_PATH)) {
    res.sendFile(DASHBOARD_PATH);
  } else {
    res.status(404).send("Dashboard not generated yet. Run generate-dashboard.py first.");
  }
});

// Chat endpoint
app.post("/api/chat", (req, res) => {
  const { name, message } = req.body;
  if (!name || !message) {
    return res.status(400).json({ error: "name and message required" });
  }

  const timestamp = new Date().toISOString();
  chatHistory.push({ name, message, timestamp, type: "user" });
  if (chatHistory.length > 50) chatHistory.shift();

  try {
    const intent = parseIntent(message);
    const tasks = queryActiveTasks();

    // Filter to tasks owned by this person (or all if Alon)
    const ownerTasks = name === "Alon" ? tasks : tasks.filter(t => t.owner === name);
    const matches = fuzzyMatch(message, ownerTasks.length ? ownerTasks : tasks);

    if (!intent) {
      const reply = {
        reply: `Got it, ${name}. I couldn't detect a status update (done/started/blocked) in your message. Try something like "done with [task name]" or "started [task name]".`,
        matched: null,
        updated: false,
      };
      chatHistory.push({ name: "VRT Bot", message: reply.reply, timestamp: new Date().toISOString(), type: "bot" });
      return res.json(reply);
    }

    if (!matches.length) {
      const reply = {
        reply: `Couldn't find a matching task for "${message}". Your active tasks: ${ownerTasks.map(t => t.name).slice(0, 5).join(", ")}`,
        matched: null,
        updated: false,
      };
      chatHistory.push({ name: "VRT Bot", message: reply.reply, timestamp: new Date().toISOString(), type: "bot" });
      return res.json(reply);
    }

    const best = matches[0];
    const newProgress = intent === "Done" ? 1 : intent === "In Progress" ? Math.max(best.progress, 0.1) : best.progress;
    updateTask(best.id, { status: intent, progress: newProgress });

    // Recalc parent progress
    for (const pid of best.parentIds) {
      recalcParentProgress(pid);
    }

    // Regenerate dashboard
    const dashOk = regenerateDashboard();

    const reply = {
      reply: `Updated "${best.name}" → ${intent}${intent === "Done" ? " (100%)" : ` (${Math.round(newProgress * 100)}%)`}. ${dashOk ? "Dashboard refreshed." : "Dashboard regen failed."}`,
      matched: { id: best.id, name: best.name, score: best.score },
      updated: true,
    };
    chatHistory.push({ name: "VRT Bot", message: reply.reply, timestamp: new Date().toISOString(), type: "bot" });
    return res.json(reply);
  } catch (err) {
    const reply = { reply: `Error: ${err.message}`, matched: null, updated: false };
    chatHistory.push({ name: "VRT Bot", message: reply.reply, timestamp: new Date().toISOString(), type: "bot" });
    return res.json(reply);
  }
});

// Get chat history
app.get("/api/chat", (req, res) => {
  res.json(chatHistory);
});

// Get active tasks (for autocomplete / reference)
app.get("/api/tasks", (req, res) => {
  try {
    const tasks = queryActiveTasks();
    res.json(tasks);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Drag-and-drop: update any item property
app.post("/api/move", (req, res) => {
  const { pageId, updates } = req.body;
  if (!pageId || !updates) {
    return res.status(400).json({ error: "pageId and updates required" });
  }
  try {
    const properties = {};
    if (updates.status) {
      properties.Status = { select: { name: updates.status } };
      if (updates.status === "Done") {
        properties.Progress = { number: 1 };
      }
    }
    if (updates.owner) {
      properties.Owner = { select: { name: updates.owner } };
    }
    if (updates.due) {
      properties.Due = { date: { start: updates.due } };
    }
    if (updates.progress !== undefined) {
      properties.Progress = { number: updates.progress };
    }
    notionRequest("PATCH", `pages/${pageId}`, { properties });

    // Recalc parent if status changed
    if (updates.status) {
      const page = notionRequest("GET", `pages/${pageId}`);
      const parentIds = (page.properties?.Parent?.relation || []).map(r => r.id);
      for (const pid of parentIds) {
        recalcParentProgress(pid);
      }
    }

    // Regenerate async (don't block the response)
    setTimeout(() => regenerateDashboard(), 100);

    res.json({ success: true, pageId, updates });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Manual regenerate
app.post("/api/regenerate", (req, res) => {
  const ok = regenerateDashboard();
  res.json({ success: ok });
});

// Reschedule: re-run auto-scheduler on remaining tasks + regenerate dashboard
const SCHEDULER_PATH = path.resolve(__dirname, "../auto-scheduler.py");

app.post("/api/reschedule", (req, res) => {
  try {
    const output = execSync(`python3 '${SCHEDULER_PATH}' --recalculate`, {
      encoding: "utf-8",
      timeout: 120000,
      env: { ...process.env },
    });
    const dashOk = regenerateDashboard();
    res.json({ success: true, dashboard: dashOk, output });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`VRT Dashboard Server running at http://localhost:${PORT}`);
  console.log(`Dashboard: ${DASHBOARD_PATH}`);
});
