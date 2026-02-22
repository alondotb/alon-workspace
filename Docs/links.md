# VRT Links & Resources

Quick-access reference to all VRT sites, tools, local files, and accounts.

## Local Dashboards & HTML

| File | Path | Description |
|------|------|-------------|
| VRT Dashboard | `~/Desktop/Alon-Workspace/Docs/dashboard.html` | Phase 0 board, goals, projects, kanban |
| VRT Dashboard (live) | `https://vrt-dashboard.netlify.app` | Shareable Netlify-hosted dashboard |
| Dashboard Server | `http://localhost:3001` | Express server — chat + drag-drop + Notion sync |
| Weekly Agenda | `~/Desktop/Alon-Workspace/Docs/weekly-agenda-feb17.html` | Presentation slides (dark theme) |
| File Viewer | `http://localhost:3000` | Express app — browse workspace files |

## Notion

| Resource | Link |
|----------|------|
| Workspace - VRT | https://notion.so/30a5308b6bc580efae57e27dbfdfd1f2 |
| VRT Tracker DB | https://notion.so/30a5308b6bc58171a2c3d89200293d13 |
| Feature Board DB | https://notion.so/30a5308b6bc5814fba07d7ba33691adc |
| Tool Inventory DB | https://notion.so/3408692eca1448868143-86ceb7f979e6 |

## Domain & Email

| Item | Value |
|------|-------|
| Main site | `vrt.co.il` |
| Sender email | `noreply@vrt.co.il` |
| Support email | `support@vrt.co.il` |

## Social Media

| Platform | Handle | Status | Planned |
|----------|--------|--------|---------|
| Instagram | @virtualtechies | Not created | Feb 19 |
| TikTok | @virtualtechies | Not created | Feb 19 |
| Facebook Page | Virtual Techies - VRT | Not created | Feb 20 |
| Facebook Group | Hebrew parent community | Not created | Feb 20 |
| YouTube | Virtual Techies | Not created | Feb 21 |
| Twitter/X | @virtualtechies | Low priority | — |
| LinkedIn | VRT Company Page | Low priority | — |

## Dev & Hosting Tools

| Tool | Purpose | Status |
|------|---------|--------|
| GitHub | VRT platform repo | Setting up (Feb 24) |
| Netlify | Web hosting, auto-deploy from GitHub | Evaluating |
| Figma | PRDs, component library | Active |
| Lovable | UI prototyping, exports React+Vite | Active (CORE) |
| Claude Code | Terminal layer, automation | Active (CORE) |
| VS Code | IDE — Matan primary, Alon learning | Active |
| Midjourney | AI visual asset generation | Active |

## Payments

| Tool | Purpose | Status |
|------|---------|--------|
| Stripe | Subscriptions (Basic 55 NIS, Premium 75 NIS) | Not set up |

## Communication

| Tool | Purpose | Status |
|------|---------|--------|
| Slack | Team comms, async updates | Active |
| Notion Calendar | Schedule, time-blocking | Active |

## Automation Scripts

| Script | Command |
|--------|---------|
| Dashboard generator | `python3 ~/Desktop/Alon-Workspace/Scripts/generate-dashboard.py` |
| File viewer server | `cd ~/Desktop/Alon-Workspace/Scripts/file-viewer && npm start` |

## Visual Assets

| Folder | Contents |
|--------|----------|
| `Visuals/brand/` | VRT_LOGO.png |
| `Visuals/campaign-tree-nodes/` | Midjourney adventurer characters |
| `Visuals/ui-concepts/` | Gaming education UI concepts |
| `Visuals/PROMPTS_CLEAN.txt` | Midjourney prompt reference |

## Full Tool Inventory

**16 tools total** — synced from Notion Tool Inventory DB.
See `~/Desktop/Alon-Workspace/tools.json` for machine-readable version.

| # | Tool | Core | Integrated | Connections |
|---|------|------|------------|-------------|
| 1 | Notion | CORE | No | Slack, Calendar, Email, Sites/Web, Docs/Files, Automation |
| 2 | Claude Code | CORE | Yes | Code/Dev, Automation, Docs/Files, Notion, Claude Code |
| 3 | Figma | CORE | No | Docs/Files, Sites/Web, Design |
| 4 | Lovable | CORE | No | Sites/Web, Design, Code/Dev |
| 5 | GitHub | — | No | Code/Dev, Automation, Claude Code |
| 6 | Netlify | — | No | Sites/Web, Hosting, Automation |
| 7 | VS Code | — | No | Code/Dev, Claude Code |
| 8 | Google Drive | — | No | Docs/Files, Sites/Web |
| 9 | Slack | — | No | Slack |
| 10 | Notion Calendar | — | No | Calendar, Notion |
| 11 | Stripe | — | No | Payments, Sites/Web |
| 12 | Midjourney | — | No | AI/Generation, Design |
| 13 | YouTube | — | No | Social Media, Sites/Web |
| 14 | Instagram | — | No | Social Media |
| 15 | TikTok | — | No | Social Media |
| 16 | Facebook | — | No | Social Media, CRM |
