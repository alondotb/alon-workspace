# VRT Full Worktree

> Complete map of all systems, files, and connections.
> Generated: 2026-02-18

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ALON'S ECOSYSTEM                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   NOTION     │  │  NETLIFY     │  │   GITHUB     │             │
│  │  (cloud)     │  │  (hosting)   │  │  (planned)   │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                 │                  │                      │
│         │ API             │ deploy           │ push                 │
│         │                 │                  │                      │
│  ┌──────┴─────────────────┴──────────────────┴───────┐             │
│  │              LOCAL MACHINE (macOS)                 │             │
│  │                                                    │             │
│  │  ┌─────────────────────────────────────────────┐  │             │
│  │  │           CLAUDE CODE (terminal)            │  │             │
│  │  │  ~/.claude/CLAUDE.md (global rules)         │  │             │
│  │  │  ~/.claude/projects/ (session memory)       │  │             │
│  │  └─────────────────┬───────────────────────────┘  │             │
│  │                    │                               │             │
│  │                    │ reads/writes                  │             │
│  │                    │                               │             │
│  │  ┌─────────────────┴───────────────────────────┐  │             │
│  │  │         ~/Desktop/Alon-Workspace/           │  │             │
│  │  │              (VRT HQ)                       │  │             │
│  │  └─────────────────────────────────────────────┘  │             │
│  │                                                    │             │
│  │  Other projects on Desktop:                        │             │
│  │  ElasticSpace, FiziVerse, MinecraftServer,         │             │
│  │  Personal, ProjectAudiocodes, Projects/            │             │
│  │                                                    │             │
│  │  Source materials:                                 │             │
│  │  ~/Downloads/virtual-techies-master/               │             │
│  └────────────────────────────────────────────────────┘             │
│                                                                     │
│  External tools:                                                    │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐          │
│  │ Figma  │ │Lovable │ │Stitch  │ │ Slack  │ │Midj.   │          │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Notion (Cloud)

```
Notion Workspace
├── Workspace (root page)
│   └── Workspace - VRT
│       ├── VRT Tracker DB          ← Goals, Projects, Tasks (70 items)
│       │   └── Views: Default, Goals, Projects, Tasks by Day
│       ├── VRT Feature Board DB    ← Granular dev tasks
│       ├── Workspace Map           ← Hierarchy doc (NEW)
│       └── (brand brief, visual identity → linked from local)
│
├── Tool Inventory DB               ← 16 tools with connections
│
└── Standalone pages
    └── "How is there not a toilet silencer?"
```

**API connection:** `ntn_222892799412...` → used by:
- `generate-dashboard.py` (pulls tracker + tools)
- `dashboard-server/server.js` (chat + drag-drop updates)

---

## Netlify (Hosting)

```
Netlify Account: alonamos-b's team
└── vrt-dashboard (site ID: 25d6a3c7-...)
    ├── URL: https://vrt-dashboard.netlify.app
    ├── Source: /tmp/vrt-dashboard-deploy/index.html
    ├── Deploys from: manual (npx netlify-cli deploy)
    └── Content: dashboard.html (regenerated from Python)
```

---

## GitHub (Planned)

```
GitHub Account: (needs auth — gh auth login)
├── vrt-landing      ← Landing page (Lovable export)
├── vrt-platform     ← Main platform (React+Vite)
├── vrt-dashboard    ← Dashboard (auto-deploy to Netlify)
└── miki-ai          ← Miki AI project
```

---

## Local File System

```
~/
├── .claude/                                    ← CLAUDE CODE CONFIG
│   ├── CLAUDE.md                              Global rules (#/update dispatch, etc.)
│   ├── settings.json
│   └── projects/
│       ├── -Users-matanmorduch/
│       │   └── memory/MEMORY.md               Session memory
│       └── -Users-matanmorduch-Desktop-Alon-Workspace/
│           └── memory/                        Workspace memory
│
├── Desktop/
│   ├── Alon-Workspace/                        ═══ VRT HQ ═══
│   │   ├── CLAUDE.md                          Workspace rules (VRT Dispatch)
│   │   ├── tools.json                         Tool stack (synced from Notion)
│   │   │
│   │   ├── Docs/                              ── Documentation ──
│   │   │   ├── workspace-map.md               File hierarchy reference
│   │   │   ├── worktree.md                    THIS FILE
│   │   │   ├── VRT-Visual-Identity.md         Brand colors/type/motion v1.1
│   │   │   ├── brand-brief.md                 Personality/voice/palette
│   │   │   ├── RnD_Feature_Breakdown.md       R&D feature specs
│   │   │   ├── links.md                       URLs & accounts
│   │   │   ├── product-decisions.md           Product choices log
│   │   │   ├── marketing-launch-plan.md       Marketing playbook
│   │   │   ├── market-research-plan.md        Research playbook
│   │   │   ├── dashboard.html                 Generated dashboard
│   │   │   ├── weekly-agenda-feb17.html       Presentation slides
│   │   │   ├── workspace-setup-log.md         Setup log
│   │   │   └── design-specs/                  Figma PRD specs (12 files)
│   │   │       ├── 00-overview.md
│   │   │       ├── 01-auth-onboarding.md
│   │   │       ├── 02-learning-core.md
│   │   │       ├── 03-projects.md
│   │   │       ├── 04-gamification.md
│   │   │       ├── 05-social.md
│   │   │       ├── 06-bug-hunt.md
│   │   │       ├── 07-parent-dashboard.md
│   │   │       ├── 08-payments-trial.md
│   │   │       ├── 09-marketing-pages.md
│   │   │       ├── 10-emails.md
│   │   │       └── 11-navigation-components.md
│   │   │
│   │   ├── Visuals/                           ── Design Assets ──
│   │   │   ├── brand/VRT_LOGO.png             Primary logo
│   │   │   ├── campaign-tree-nodes/           Character art (2 files)
│   │   │   ├── ui-concepts/                   UI mockups (4 files)
│   │   │   ├── Lesson_Terminal.png
│   │   │   ├── lesson_01.png
│   │   │   └── PROMPTS_CLEAN.txt              Midjourney prompts
│   │   │
│   │   ├── Alon - Renders/                    ── 3D Animation ──
│   │   │   ├── cubes_00.blend                 Blender project
│   │   │   ├── VIDEO-010001-0250.mp4          Rendered video
│   │   │   └── [PNG's]/                       250 render frames
│   │   │
│   │   ├── Scripts/                           ── Automation ──
│   │   │   ├── generate-dashboard.py          Dashboard generator
│   │   │   ├── dashboard-server/              Express.js server
│   │   │   │   ├── server.js                  Chat + drag-drop API
│   │   │   │   └── package.json
│   │   │   ├── file-viewer/                   Local file browser
│   │   │   │   ├── server.js
│   │   │   │   └── index.html
│   │   │   ├── push_design_specs_to_notion.py
│   │   │   ├── create_vrt_feature_board.py
│   │   │   ├── reorganize_notion.py
│   │   │   ├── rewrite_notion_workspace.py
│   │   │   └── morning-sync.md
│   │   │
│   │   └── Marketing-Handoff/                 Assets for Sahar
│   │
│   ├── Projects/                              ── Matan's projects ──
│   │   └── (25+ NestJS, Flutter, Unity, Go projects)
│   │
│   └── (ElasticSpace, FiziVerse, MinecraftServer, Personal, etc.)
│
└── Downloads/
    └── virtual-techies-master/                ═══ VRT SOURCE MATERIALS ═══
        ├── Python_Course/                     Full curriculum
        │   ├── Syllabus.md
        │   ├── Lessons_Version_1/
        │   ├── code_examples/
        │   └── (contracts, homework, pilot)
        ├── Recordings/                        Game code samples
        ├── Vision/                            Product vision docs
        ├── financial/                         Financial model
        └── Manim/                             Animation code
```

---

## Connection Map

```
generate-dashboard.py ──── reads ────→ Notion Tracker DB
         │                              Notion Tool Inventory DB
         │
         └── writes ──→ Docs/dashboard.html
                              │
                              ├── served by → dashboard-server (localhost:3001)
                              └── deployed to → Netlify (vrt-dashboard.netlify.app)

dashboard-server/server.js
  ├── serves → dashboard.html at /
  ├── POST /api/chat → parses message → updates Notion → regenerates
  ├── POST /api/move → drag-drop → updates Notion → regenerates
  └── calls → generate-dashboard.py (to rebuild HTML)

CLAUDE.md (global) → defines #/update dispatch
  └── VRT dispatch:
      1. Update Notion Tracker
      2. Update Tool Inventory
      3. Sync tools.json + links.md
      4. Run generate-dashboard.py
      5. Report

Figma ← exports from → Lovable / Google Stitch
  └── feeds into → Docs/design-specs/ → R&D (Matan)
```

---

## Data Flow

```
Team member types in Chat  ──→  Express server  ──→  Notion API
       or drags card                   │                 │
                                       │              updates
                                       │                 │
                                       ├──→  regenerate-dashboard.py
                                       │           │
                                       │        new HTML
                                       │           │
                                       └──→  serves updated page
                                              (auto-reload in 2.5s)
```
