# VRT Workspace

## About VRT

**Virtual Techies** — end to end self taught coding on the web for kids, using reecorded videos & animations and an in web ide for actual coding.

## Team

| Person | Role | Contact |
|---|---|---|
| Alon | Head of Product. Head of all visual design (for ui/ux & marketing) | alonamos.b@gmail.com|
| Matan | R&D, dep ops | matanmor9@gmail.com |
| Sahar | Marketing & sales | saharuzan51@gmail.com |

## The 3 Departments

Everything VRT does falls into one of three departments. 

1. **Marketing** — Content creation (alon) -> handoff->launch/iterate.
2. **Product** — defining the product vision, prioritizing features, writing requirements (PRDs), making business decisions
3. **UI/UX** - designing the platform based on PRD and handing off a "FIGMA PRD" to r&D"
4. **R&D** — Platform development, infrastructure, all front end and backend.

## Boundaries
- The Python course content at `~/Downloads/virtual-techies-master/` is Matan's domain. Do NOT modify actual course content, lessons, or game files there.



## GitHub Sync - This workspace is synced via GitHub so Alon can work from both Mac and PC with the same Claude Code context, scripts, and docs.
**Repo:** `alondotb/alon-workspace` (public)
**URL:** https://github.com/alondotb/alon-workspace
**What's tracked:** CLAUDE.md, .claude/, tools.json, Scripts/, VRT/, Dashboard/
**What's NOT tracked:**
- `.env` — secrets, local-only. Copy `.env.example` and fill in keys.
- `Alon - Renders/` — 2.2 GB, too large for Git. Synced via Google Drive.



## API Keys
**Keys:** stored in `~/Desktop/Alon-Workspace/.env`


**PC setup:**
```bash
git clone https://github.com/alondotb/alon-workspace.git ~/Desktop/Alon-Workspace
cd ~/Desktop/Alon-Workspace
cp .env.example .env        # then edit with your Notion API key
```

## Local workspace structure

All docs (PRDs, brand brief, product decisions, design specs, etc.) live in Notion. CLAUDE.md is the only local .md file.

```
~/Desktop/Alon-Workspace/
  CLAUDE.md              # Workspace rules (only local .md)
  .claude/               # Claude Code settings
  tools.json             # Tool stack (synced from Notion)
  .env                   # API keys — GITIGNORED
  .env.example           # Template for .env setup
  .gitignore
  .mcp.json              # MCP server config
  Scripts/
    auto-scheduler.py    # Task scheduler for April 17 launch
  VRT/
    Product/             # Product docs live in Notion
    Marketing/           # Brand assets, campaign materials
      brand/             # VRT_LOGO.png
    UI-UX/               # Design assets, mockups
      campaign-tree-nodes/
      ui-concepts/
    R&D/                 # Code lives in separate GitHub repos
  Dashboard/             # VRT dashboard (auto-generated)
  Alon - Renders/        # Large renders — GITIGNORED (Google Drive)
```

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
4. Show summary: "Rescheduled X tasks."

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

- Notion is the system of record and manage projects. Claude Code is the terminal layer.
- One source of truth — everything lives in Notion, Github & Drive
- Keep it simple. sacrifice grammer for being concise
- **ALWAYS** go to the database sources relevant to the context in the relevant tool to fetch all the information necessary and stay up to date. Never work from stale data — query Notion, read local files, check live state before acting.

## End-of-conversation: Sync Status

At the end of every conversation, output a sync status block:

```
notion: synced/not synced
calendar: synced/not synced
```
