# VRT Workspace

## About VRT

**Virtual Techies** — self-paced coding education for kids aged 10-14. Kids learn real programming through a 2D campaign with video-based quests. No teacher needed.

**Target launch:** April 2026 (2 months from now).

## Team

| Person | Role | Contact |
|---|---|---|
| Alon | Product, Design, Business — owns all 3 departments | — |
| Matan | R&D, Development | — |
| Sahar | Marketing | saharuzan51@gmail.com |

## The 3 Departments

Everything VRT does falls into one of three departments. Alon owns all three:

1. **Marketing** — YouTube channel (parent + kids content), live courses marketing (liquidity), platform launch marketing
2. **Product** — Landing page (Lovable → Figma → components → R&D), MVP platform, payment/subscription system
3. **R&D** — Platform development, infrastructure, CI/CD, component library for R&D handoff

## Boundaries

- The Python course content at `~/Downloads/virtual-techies-master/` is Matan's domain. Do NOT modify actual course content, lessons, or game files there.
- Alon is the product/design person — Claude handles all code changes. Don't ask Alon to write code.

## Notion API

**Key:** stored in `~/Desktop/Alon-Workspace/.env` as `NOTION_API_KEY`
**Version header:** `Notion-Version: 2022-06-28`

Use `curl` for all Notion API calls. Load the key from `.env`.

## Key Notion IDs

| Resource | Notion ID |
|---|---|
| Workspace page | `9a0ef9f8-e383-4a28-8a12-ba27fc0697cf` |
| Workspace - VRT page | `30a5308b-6bc5-80ef-ae57-e27dbfdfd1f2` |
| **VRT Tracker DB** | `30a5308b-6bc5-8171-a2c3-d89200293d13` |
| VRT Feature Board DB | `30a5308b-6bc5-814f-ba07-d7ba33691adc` |
| Tool Inventory DB | `3408692e-ca14-4886-8143-86ceb7f979e6` |

## VRT Tracker — the management hub

The **VRT Tracker** is the single database for managing goals, projects, and tasks across all 3 departments. It lives on the Workspace - VRT Notion page.

**Properties:**
- Name (title)
- Department (select: Marketing / Product / R&D)
- Level (select: Goal / Project / Task)
- Progress (number, %)
- Status (select: Not Started / In Progress / Done / Blocked)
- Due (date)
- Owner (select: Alon / Matan / Sahar)
- Parent (self-relation — links Task→Project→Goal)
- Feature Board Tasks (relation → VRT Feature Board for granular tasks)
- Notes (rich text)

**Hierarchy:** Goal → Project → Task. Each department has one Goal, with Projects and Tasks beneath it.

## Always: Keep Notion in sync

Proactively update the VRT Tracker whenever progress happens during a session — don't wait to be asked. This includes:
- Marking tasks/projects as Done or In Progress when completed or started
- Updating Progress % after meaningful work
- Creating new tasks when new work is identified
- Recalculating parent progress (average of children) after any child update
- Flagging blockers immediately

If a session produces no Tracker-relevant changes, skip the update silently.

## First action: Morning Sync

When starting a session, run the morning sync:

1. **Pull the VRT Tracker** — query the database for all items where Status ≠ Done:
   ```
   POST https://api.notion.com/v1/databases/30a5308b-6bc5-8171-a2c3-d89200293d13/query
   Filter: Status != Done
   ```
2. **Display a dashboard** grouped by Department → Goal → Project → Task, showing Progress % and Status for each item. Flag anything overdue or blocked.
3. **Ask Alon** — "What's changed? Any updates?" Then wait.
4. **Update Notion** — based on what Alon says, update Progress % and Status via the API. Recalculate parent progress as the average of children.
5. **Sync tools.json** — compare the code block on the Workspace page against `~/Desktop/Alon-Workspace/tools.json`. Update local if different.

## GitHub Sync

**Repo:** `alondotb/alon-workspace` (public)
**URL:** https://github.com/alondotb/alon-workspace

This workspace is synced via GitHub so Alon can work from both Mac and PC with the same Claude Code context, scripts, and docs.

**What's tracked:** CLAUDE.md, .claude/, tools.json, Docs/ (markdown only), Scripts/, Visuals/, Marketing-Handoff/
**What's NOT tracked:**
- `.env` — secrets, local-only. Copy `.env.example` and fill in keys.
- `Alon - Renders/` — 2.2 GB, too large for Git. Synced via Google Drive.
- `Docs/dashboard.html` + `Docs/index.html` — generated files, regenerate locally.
- `.dashboard-deploy/` — temp clone of vrt-dashboard repo for deploys.

**Daily workflow (either machine):**
```bash
cd ~/Desktop/Alon-Workspace
git pull                    # get latest
# ... work ...
git add -A && git commit -m "Session update" && git push
```

**PC setup:**
```bash
git clone https://github.com/alondotb/alon-workspace.git ~/Desktop/Alon-Workspace
cd ~/Desktop/Alon-Workspace
cp .env.example .env        # then edit with your Notion API key
npm install --prefix Scripts/dashboard-server
```

**Dashboard deploys** go to a separate repo (`alondotb/vrt-dashboard` → GitHub Pages). The deploy script handles this automatically via a clone at `.dashboard-deploy/`.

## Local workspace structure

```
~/Desktop/Alon-Workspace/
  CLAUDE.md              # This file (tracked in Git)
  .claude/               # Claude Code settings (tracked)
  tools.json             # Tool stack (synced from Notion, tracked)
  .env                   # API keys — GITIGNORED (secrets)
  .env.example           # Template for .env setup
  .gitignore             # Git ignore rules
  Docs/                  # Local docs, design specs, dashboard output
    vrt-dashboard/       # Dashboard docs + Lovable handoffs
    design-specs/        # 12 PRD files (00-overview through 11-navigation)
  Scripts/               # Automation scripts + deploy
    dashboard-server/    # Express server (port 3001)
    deploy-dashboard.sh  # One-click regenerate + deploy
  Marketing-Handoff/     # Marketing assets for Sahar
  Visuals/               # Design assets, brand, UI concepts
  Alon - Renders/        # Large renders — GITIGNORED (Google Drive)
```

Source materials: `~/Downloads/virtual-techies-master/` (Matan's domain — course content, financials, contracts)

## Workflow

1. **Capture** — ideas/tasks into Notion VRT Tracker
2. **Plan** — weekly review: prioritize, set goals, assign owners
3. **Produce** — Matan codes, Alon handles content/design, Sahar runs marketing, Claude assists all
4. **Publish** — ship to site, YouTube, socials. Log links in Notion
5. **Measure** — check signals, capture learnings, feed back into Capture

## Lovable → Claude Code Workflow

Alon uses **Lovable** as his design sandbox for layout and visual experiments. When Alon shares a Lovable export or link:

1. **Compare** — diff the Lovable output against current `generate-dashboard.py` output
2. **Identify changes** — layout, CSS, new sections, section reordering, visual hierarchy
3. **Merge** — apply changes to the Python generator (CSS block, HTML structure, section order)
4. **Deploy** — run `#/deploy` to regenerate from Notion + push to Netlify

Lovable handoffs go in `Docs/vrt-dashboard/lovable-handoffs/`. See `Docs/vrt-dashboard/structural-brief.md` for the section mapping.

## #/deploy — One-Click Deploy

When Alon says `#/deploy`:
```bash
bash ~/Desktop/Alon-Workspace/Scripts/deploy-dashboard.sh
```
This regenerates the dashboard from live Notion data and deploys to https://alondotb.github.io/vrt-dashboard/.

## Auto-Scheduler

**Script:** `Scripts/auto-scheduler.py` — assigns due dates to all tracker tasks for the April 17 launch.

**CLI modes:**
```bash
python3 Scripts/auto-scheduler.py              # Full: audit + schedule + write
python3 Scripts/auto-scheduler.py --audit      # Audit only, no date changes
python3 Scripts/auto-scheduler.py --dry-run    # Preview assignments, don't write
python3 Scripts/auto-scheduler.py --recalculate  # Re-run on remaining non-Done tasks
```

**4 Phases:**
1. Foundation (Feb 18 – Mar 8): PRDs, brand, design, infra setup, marketing plan
2. Build Sprint (Mar 9 – Mar 29): Core dev, landing page, content production, YouTube
3. Polish & Test (Mar 30 – Apr 10): QA, payment, polish, marketing ramp
4. Launch Prep (Apr 11 – Apr 16): Final checklist, launch marketing

**Recalculation flow** — when Alon reports progress:
1. Mark tasks Done in Notion (update Status + Progress)
2. Run `python3 Scripts/auto-scheduler.py --recalculate`
3. Scheduler redistributes remaining tasks across available future dates
4. Run `bash Scripts/deploy-dashboard.sh` to regenerate + deploy
5. Show summary: "Rescheduled X tasks."

The dashboard server also exposes `POST /api/reschedule` to trigger `--recalculate` + dashboard regen.

## Tool Inventory Sync Rules

The **Tool Inventory** tracks every tool VRT uses. After any session that adds, removes, configures, or discusses a tool change, Claude must verify sync.

**Notion DB IDs:**
- Source DB: `9a174461-6e08-4f12-93a0-72b69365411a`
- Linked view (for queries): `3408692e-ca14-4886-8143-86ceb7f979e6`

**Properties per tool:**
`Tool` (title), `Purpose` (text), `Connections` (multi-select), `Type` (select), `Integrated` (checkbox), `Core` (select), `Is connected to Claude Code` (checkbox), `Last Synced` (date), `Owner / Team space` (people), `Notes / gotchas` (text), `Shared` (select), `Replacement options` (text), `Default workflow` (text), `Last reviewed` (date)

**Sync protocol — run after any tool-related change:**
1. Query all tools from the linked DB (`3408692e...`)
2. Compare against local `tools.json`
3. If changes detected:
   - Update Notion (write to source DB `9a174461...`)
   - Set `Last Synced` to today's date on each changed tool
   - Regenerate `tools.json` from the query result
   - Regenerate + deploy dashboard
4. If no changes: skip silently

**What triggers a sync:**
- A new tool is mentioned and agreed upon (add to inventory)
- An existing tool's integration status changes (e.g. Figma connected to Claude Code)
- A tool is removed or replaced
- Tool connections or purpose are updated
- Any `#/update` dispatch

**tools.json format:**
```json
{
  "generated_from": "Notion → Tool Inventory",
  "generated_at": "ISO timestamp",
  "tools": [{"name": "", "connections": [], "core": bool, "integrated": bool}]
}
```

## Principles

- Notion is the system of record. Claude Code is the terminal layer.
- One source of truth — everything lives in Notion or Git.
- Keep it simple. Build what you need now.
- Automate the boring stuff — if it's done twice, script it.
- Fewer tools, each with a clear job.
- **ALWAYS** go to the database sources relevant to the context in the relevant tool to fetch all the information necessary and stay up to date. Never work from stale data — query Notion, read local files, check live state before acting.

## End-of-conversation: Sync Status

At the end of every conversation, output a sync status block:

```
notion: synced/not synced
vrt dashboard: synced/not synced
calendar: synced/not synced
```

## Dashboard auto-refresh

The HTML dashboard at `Docs/dashboard.html` should auto-refresh in the browser. Regenerate it (`python3 Scripts/generate-dashboard.py`) after any Notion update so the open tab stays current. Both `dashboard.html` and `index.html` are generated (Netlify needs `index.html`).

## VRT Dispatch (#/update)

When `#/update` is called in VRT context, run all of these in order:

1. **Notion VRT Tracker** — update changed items (Progress, Status). Recalculate parent progress = avg of children.
2. **Notion Tool Inventory** — add/update tools if any were discussed or configured.
3. **Local sync** — regenerate `tools.json` from Tool Inventory. Update `links.md` if new resources.
4. **Dashboard** — run `bash Scripts/deploy-dashboard.sh` (regenerate + deploy).
5. **Report** — print dispatch summary with counts.

The dashboard has a Notion sidebar — every card (goal/project/task) has an arrow icon that opens a detail panel with an "Open in Notion" link. This is the bridge between dashboard and Notion.
