const express = require('express');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const os = require('os');

const app = express();
app.use(express.json());
const PORT = 3000;

const ROOT_DIRS = [
  path.join(os.homedir(), 'Desktop', 'Alon-Workspace'),
  path.join(os.homedir(), 'Downloads', 'virtual-techies-master'),
];

const SKIP = new Set(['node_modules', '.git', '.DS_Store', '__pycache__']);

function isAllowed(p) {
  const resolved = path.resolve(p);
  return ROOT_DIRS.some((root) => resolved.startsWith(root + path.sep) || resolved === root);
}

function scanDir(dirPath) {
  let results = [];
  let entries;
  try {
    entries = fs.readdirSync(dirPath, { withFileTypes: true });
  } catch {
    return results;
  }
  for (const entry of entries) {
    if (SKIP.has(entry.name)) continue;
    const fullPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      results.push({
        name: entry.name,
        path: fullPath,
        type: 'directory',
        children: scanDir(fullPath),
      });
    } else {
      let stat;
      try {
        stat = fs.statSync(fullPath);
      } catch {
        continue;
      }
      results.push({
        name: entry.name,
        path: fullPath,
        type: 'file',
        size: stat.size,
        modified: stat.mtime,
        ext: path.extname(entry.name).toLowerCase(),
      });
    }
  }
  results.sort((a, b) => {
    if (a.type !== b.type) return a.type === 'directory' ? -1 : 1;
    return a.name.localeCompare(b.name);
  });
  return results;
}

// Collect all directory paths for the "Move to" folder picker
function collectDirs(nodes, list) {
  for (const node of nodes) {
    if (node.type === 'directory') {
      list.push({ name: node.name, path: node.path });
      if (node.children) collectDirs(node.children, list);
    }
  }
  return list;
}

app.get('/', (_req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/api/files', (_req, res) => {
  const tree = ROOT_DIRS.map((dir) => ({
    name: path.basename(dir),
    path: dir,
    type: 'directory',
    children: scanDir(dir),
  }));
  res.json(tree);
});

app.get('/api/dirs', (_req, res) => {
  const tree = ROOT_DIRS.map((dir) => ({
    name: path.basename(dir),
    path: dir,
    type: 'directory',
    children: scanDir(dir),
  }));
  const dirs = [];
  for (const root of tree) {
    dirs.push({ name: root.name, path: root.path });
    collectDirs(root.children, dirs);
  }
  res.json(dirs);
});

app.get('/api/open', (req, res) => {
  const filePath = req.query.path;
  if (!filePath) return res.status(400).json({ error: 'Missing path' });
  if (!isAllowed(filePath)) return res.status(403).json({ error: 'Path not allowed' });

  const resolved = path.resolve(filePath);
  exec(`open "${resolved.replace(/"/g, '\\"')}"`, (err) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ ok: true });
  });
});

app.post('/api/move', (req, res) => {
  const { src, dest } = req.body;
  if (!src || !dest) return res.status(400).json({ error: 'Missing src or dest' });
  if (!isAllowed(src) || !isAllowed(dest)) return res.status(403).json({ error: 'Path not allowed' });

  const resolvedSrc = path.resolve(src);
  const resolvedDest = path.resolve(dest);

  // dest must be a directory
  try {
    const stat = fs.statSync(resolvedDest);
    if (!stat.isDirectory()) return res.status(400).json({ error: 'Destination is not a directory' });
  } catch {
    return res.status(400).json({ error: 'Destination does not exist' });
  }

  const newPath = path.join(resolvedDest, path.basename(resolvedSrc));

  // Don't overwrite existing files
  if (fs.existsSync(newPath)) {
    return res.status(409).json({ error: 'A file with that name already exists in the destination' });
  }

  // Don't move a folder into itself
  if (resolvedDest.startsWith(resolvedSrc + path.sep)) {
    return res.status(400).json({ error: 'Cannot move a folder into itself' });
  }

  try {
    fs.renameSync(resolvedSrc, newPath);
    res.json({ ok: true, newPath });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`File viewer running at http://localhost:${PORT}`);
});
