# VRT Dashboard — Structural Layout Brief for Lovable

> This document describes the complete layout, structure, and behavior of the VRT Dashboard.
> It contains ZERO visual design decisions — no colors, typography, spacing, shadows, or styling.
> Lovable should use this as a blueprint and apply its own visual/creative design from scratch.

---

## What This Dashboard Is

An operational dashboard for a 3-person startup (VRT — Virtual Techies). It visualizes their entire project management system pulled from Notion. The team manages goals, projects, and tasks across two "planes": Marketing and Product.

The dashboard must feel like a **real-time command center** — alive, interactive, and dense with information without feeling cluttered.

---

## Design Hierarchy (IMPORTANT)

The dashboard follows a strict top-down hierarchy that mirrors how the team thinks:

1. **GOALS first** — the top header section. Goals are the inspiration layer. They sit at the very top as the "billboard" — always visible, always motivating. The team should see their north star before anything else.
2. **PROJECTS second** — directly beneath goals. Projects are the data management and workload management layer. They break goals into actionable chunks and help the team not get overwhelmed.
3. **TASKS third** — the execution layer. Individual work items that people actually do day-to-day.

This Goal → Project → Task flow is the backbone of the page. Everything else (metrics, Phase 0, team view, tools) supports this core hierarchy.

---

## Page Structure (Top to Bottom)

The page is a single scrollable view with a fixed sidebar (off-screen by default) and a floating chat button.

```
┌─────────────────────────────────────────────────────────────┐
│                        HEADER                                │
│              Title + subtitle + last updated                 │
├─────────────────────────────────────────────────────────────┤
│                    METRICS STRIP                             │
│     [Days to Launch] [Overall %] [Tasks Done] [Overdue]     │
│     [In Progress] [Not Started] [Blocked] [Total Items]     │
├─────────────────────────────────────────────────────────────┤
│          ★ GOALS (BILLBOARD — TOP OF PAGE) ★                │
│     3 hero cards (one per goal), each with:                  │
│     - Goal name, project count, task count                   │
│     - Progress bar + percentage                              │
│     - Plane indicator (Marketing / Product)                  │
│     - Notion sidebar trigger                                 │
│     Purpose: INSPIRATION — the team's north star             │
├─────────────────────────────────────────────────────────────┤
│                  DONE FOR TODAY CARD                         │
│     Grid of completed items with checkmarks                  │
│     (drop zone — drag tasks here to mark done)              │
├─────────────────────────────────────────────────────────────┤
│              OVERDUE ALERT (conditional)                     │
│     Warning banner listing overdue items                     │
├─────────────────────────────────────────────────────────────┤
│               ★ PROJECTS (DATA LAYER) ★                     │
│     3-column board grouped by status:                        │
│     [In Progress] [Not Started] [Blocked]                    │
│     Each column lists project cards with:                    │
│     - Project name, owner, plane tag, progress bar           │
│     - Draggable between columns                              │
│     - Click to open Notion sidebar                           │
│     Purpose: DATA MANAGEMENT — break goals into chunks       │
├─────────────────────────────────────────────────────────────┤
│              ★ TASKS KANBAN (EXECUTION LAYER) ★             │
│     Auto-fit columns grouped by status:                      │
│     [In Progress] [Not Started] [Blocked]                    │
│     Each column lists task cards with:                       │
│     - Task name, owner badge, plane tag, due date            │
│     - Draggable between columns and into Done card           │
│     - Click to open Notion sidebar                           │
│     Purpose: EXECUTION — what people actually do today       │
├─────────────────────────────────────────────────────────────┤
│                   PHASE 0 BOARD                              │
│     Filter buttons: [All] [Marketing] [Product] [Alon]...   │
│     Horizontal scroll timeline: 19 day-columns (Feb 18–Mar 8)│
│     Each column has task cards sorted by date                │
├─────────────────────────────────────────────────────────────┤
│                   THIS WEEK                                   │
│     Grid of day cards (Mon–Sun + Backlog)                    │
│     Today's card is visually distinct                        │
│     Each card lists tasks assigned to that day               │
│     Shows owner initials per task                            │
├─────────────────────────────────────────────────────────────┤
│                   TEAM VIEW                                   │
│     3 cards (one per team member: Alon, Matan, Sahar)        │
│     Each shows:                                              │
│     - Name, active task count                                │
│     - List of their active tasks with status indicators      │
│     - Overdue items flagged                                  │
│     (drop zone — drag tasks to reassign owner)              │
├─────────────────────────────────────────────────────────────┤
│                   TOOL STACK                                  │
│     Grid of tool cards (17 tools)                            │
│     Each card shows:                                         │
│     - Tool name, integration status dot                      │
│     - Connection tags (what it connects to)                  │
│     - CORE badge if applicable                               │
│     - Click to open Notion sidebar with full tool details    │
│     NOTE: Tool stack dynamically updates to show relevant    │
│     tools when a task/project is selected (contextual view)  │
├─────────────────────────────────────────────────────────────┤
│                   LINKS PANEL                                │
│     Collapsible panel (click to expand/collapse)             │
│     Contains categorized links:                              │
│     - Dashboards & Sites (3 links)                           │
│     - Notion pages (5 links)                                 │
│     - Dev Tools (4 links)                                    │
│     - Communication (2 links)                                │
│     Each link has a category dot + label + external arrow    │
├─────────────────────────────────────────────────────────────┤
│                     FOOTER                                    │
│     Timestamp of last generation                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Floating Elements (Always Visible)

### Chat Button (FAB)
- Fixed position, bottom-right corner
- Opens a chat window when clicked

### Chat Window
- Fixed position, bottom-right, above the FAB
- Contains:
  - Header with title + user selector dropdown (Alon / Matan / Sahar)
  - Scrollable message area with user and bot message bubbles
  - Input field + send button
- **Behavior:** User types natural language like "done with landing page wireframe" → the server parses intent (done/started/blocked), fuzzy-matches a task, updates Notion, and replies with confirmation
- Message history persists in-memory (last 50 messages)

### Notion Sidebar
- Fixed position, right edge, full height
- Hidden by default (slides in from right)
- Opens when clicking a Notion icon on any card (goal/project/task/tool)
- Contains:
  - Header with item name + close button
  - Body with structured metadata rows:
    - Level (Goal/Project/Task)
    - Status with indicator
    - Plane with tag
    - Owner
    - Due date
    - Progress bar with percentage
    - Notes text
    - Categories (if any)
    - Tool strip (connection badges — for tool items only)
    - Children list (clickable, navigates sidebar to child item)
  - Footer with "Open in Notion" button (links to actual Notion page)
- When sidebar opens, main content shifts left to make room

---

## Interactive Behaviors

### Drag and Drop
The following items are draggable:
- Project cards (in the Projects section)
- Task cards (in the Tasks kanban)
- Phase 0 Board cards

Valid drop zones:
| Dragged From | Can Drop On | What Happens |
|---|---|---|
| Task card | Different status column | Changes task status in Notion |
| Task card | Done For Today card | Marks task as Done (100%) in Notion |
| Task card | Team member card | Changes task owner in Notion |
| Project card | Different status column | Changes project status in Notion |
| P0 card | Different day column | Changes task due date in Notion |

During drag:
- A floating badge follows the cursor showing the item name
- Valid drop zones highlight
- A thin insertion indicator appears at the drop position
- After drop: brief flash animation, toast notification, page auto-refreshes after 2.5s

### Card Click → Sidebar
Every goal card, project card, task card, and tool card has a small icon button (appears on hover). Clicking it opens the Notion sidebar with that item's details. The sidebar data is embedded as JSON in the page at generation time.

### Links Panel Toggle
Click the links panel header to expand/collapse the link grid.

### Phase 0 Board Filters
Filter buttons at the top of the Phase 0 Board section. Clicking a filter shows/hides cards based on:
- "All" — show everything
- "Marketing" / "Product" — filter by plane
- "Alon" / "Matan" / "Sahar" — filter by owner

### Auto-Refresh
- The page has a meta refresh tag (60 seconds)
- After chat messages: reloads after 2 seconds
- After drag-drop actions: reloads after 2.5 seconds

---

## Data Hierarchy

```
Goal (3 total — one per plane area)
  └── Project (multiple per goal)
        └── Task (multiple per project)
```

Each item has:
- **Name** (title)
- **Plane** — Marketing or Product
- **Level** — Goal, Project, or Task
- **Status** — Not Started, In Progress, Done, Blocked
- **Progress** — 0% to 100% (parent = average of children)
- **Due** — date
- **Owner** — Alon, Matan, or Sahar
- **Parent** — links to parent item (Task→Project→Goal)
- **Notes** — free text
- **Categories** — tags like UI/UX, R&D, Content, Business, etc.

---

## Section Details

### 1. Metrics Strip
8 compact metric blocks in a row:
1. Days to Launch (countdown to April 17, 2026)
2. Overall Progress (weighted average across all goals)
3. Done count (tasks with status = Done)
4. Overdue count (tasks past due date, not done)
5. In Progress count
6. Not Started count
7. Blocked count
8. Total item count

### 2. Goals (BILLBOARD — top of content)
3 large hero-style cards, one for each goal. Cards span full width in a 3-column grid. This is the **inspiration section** — the first thing the team sees after metrics. Each shows: goal name, progress percentage, progress bar, project count, task count, plane indicator. A colored strip at the top indicates the plane. Clicking the Notion icon opens the sidebar.

### 3. Done For Today
A card showing all items marked "Done" today (or items ahead of schedule). Each item shows a checkmark, the item name, plane tag, and a Notion link. Also acts as a drop zone — dragging a task onto it marks it as Done.

### 4. Projects Board (DATA MANAGEMENT layer)
3-column Kanban layout grouped by status (In Progress, Not Started, Blocked). Sits directly after Goals to establish the Goal → Project flow. Column headers show status name + count. Each project card shows: name, owner, plane tag, progress bar, percentage. Cards are draggable between columns. Each has a Notion sidebar trigger.

### 5. Tasks Kanban (EXECUTION layer)
Same Kanban layout as Projects but for tasks. Auto-fitting columns. Task cards show: name, owner badge, plane tag, due date, parent name. Overdue tasks have distinct styling. Cards are draggable between columns and to the Done card.

### 6. Phase 0 Board
A horizontal scrollable timeline board. 19 columns representing dates from Feb 18 to Mar 8, 2026. Today's column is visually distinct. Each column contains task cards assigned to that day. Cards show: status dot, task name, category tags, owner badge, Notion link. Cards are draggable between day columns (changes the due date).

### 7. This Week
Grid of day cards (Mon through Sun + Backlog). Today's card is highlighted. Each card lists tasks assigned to that day with owner initials.

### 8. Team View
3 cards (Alon, Matan, Sahar). Each shows: name, active task count, and a scrollable list of their active tasks with status dots. Overdue items are flagged. Team cards are drop zones — dragging a task onto a team member reassigns ownership.

### 9. Tool Stack (CONTEXTUAL)
Grid of 17 tool cards. Each card shows: tool name, integration status (integrated / not integrated), connection tags, and a CORE badge if applicable. Clicking the Notion icon opens the sidebar with full tool details (purpose, workflow, replacement options, etc.). The tool strip in the sidebar shows colored dots for each connection type. **When a task or project is selected, the tool stack filters to show only tools relevant to that item's categories** (e.g., selecting a UI/UX task highlights Figma, Lovable).

### 10. Links Panel
A collapsible section. Header shows title + link count + expand/collapse arrow. Body contains a grid of categorized links. 4 categories with 14 total links. Each link shows: colored category dot, link label, external link arrow.

### Card Selection & Expand Behavior
Every card (goal, project, task) has two click actions:
1. **Notion icon** — opens the Notion sidebar (existing behavior)
2. **Card body click** — selects the card, which:
   - Enlarges it to ~3x size in place
   - Shows a "stickies" overlay with the full tree of related items (parent → siblings → children)
   - Each sticky is clickable — clicking navigates to that item's position in the dashboard and focuses on it
   - The Tool Stack section auto-updates to show tools relevant to the selected item's categories
   - Clicking outside or pressing Escape deselects

---

## Responsive Behavior

The layout should adapt to these breakpoint ranges:
1. **Desktop** (>1024px) — full layout, sidebar pushes content
2. **Tablet** (<=1024px) — reduced padding
3. **Narrow tablet** (<=900px) — single-column for goals/projects/team, narrower sidebar
4. **Mobile** (<=640px) — 2-column grids collapse, sidebar overlays instead of pushing
5. **Small mobile** (<=480px) — single-column everything, chat window full-width

---

## Server Architecture (for reference)

The dashboard HTML is generated by a Python script that pulls data from Notion APIs. An Express.js server serves the HTML and provides these API endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Serve the dashboard HTML |
| `/api/chat` | POST | Natural language status updates |
| `/api/chat` | GET | Get chat history |
| `/api/tasks` | GET | Get active tasks (for autocomplete) |
| `/api/move` | POST | Drag-and-drop updates (status, owner, date) |
| `/api/regenerate` | POST | Force regenerate the dashboard |

The chat system parses natural language intent:
- "done with X" → marks X as Done
- "started X" → marks X as In Progress
- "blocked on X" → marks X as Blocked

It uses fuzzy matching to find the right task and filters by the selected user.

---

## What Lovable Should Do

1. Take this structural layout as the blueprint
2. Apply a fresh, modern visual design (Lovable's creative direction)
3. Keep ALL sections, interactions, and data relationships intact
4. The output should be a single-page React component or HTML that can replace the current dashboard
5. Prioritize: information density without clutter, clear visual hierarchy, smooth interactions
6. The target audience is a small startup team — it should feel professional but energetic

---

---

## Lovable → Claude Code Handoff Protocol

When Alon designs a new layout or visual iteration in Lovable:

1. **Export from Lovable** — save the HTML/CSS output to `Docs/vrt-dashboard/lovable-handoffs/`
2. **Tell Claude Code** — share the file or paste a Lovable link in chat
3. **Claude compares** — diffs the Lovable output against the current `generate-dashboard.py` output
4. **Claude merges** — applies layout/CSS/structural changes to the Python generator

### Section Mapping: Lovable Components → Python Generator

| Dashboard Section | Python Generator Block | Line Range (approx) |
|---|---|---|
| Header | `# ═══ HEADER ═══` | ~320–340 |
| Metrics Strip | `# ═══ METRICS ═══` | ~340–400 |
| Goals (Billboard) | `# ═══ TIER 1: GOALS ═══` | ~425–465 |
| Done For Today | `done_today + ahead` block | ~440–462 |
| Overdue Alert | `if overdue:` block | ~464–468 |
| Projects Board | `# ═══ TIER 2: PROJECTS ═══` | ~470–490 |
| Tasks Kanban | `# ═══ TIER 3: TASKS ═══` | ~492–525 |
| Phase 0 Board | `# ═══ PHASE 0 ═══` | ~525–620 |
| This Week | `# ═══ THIS WEEK ═══` | ~620–660 |
| Team View | `# ═══ TEAM ═══` | ~660–700 |
| Tool Stack | `# ═══ TOOL STACK ═══` | ~700–750 |
| Links Panel | `# ═══ LINKS ═══` | ~750–800 |
| CSS (all styles) | `<style>` block | ~155–270 |
| JS (all scripts) | `<script>` blocks | ~800–end |

### What Lovable Should Touch vs. Not Touch

| Lovable controls | Claude Code controls |
|---|---|
| Layout grid, spacing, section order | Notion API data fetching |
| Colors, typography, visual hierarchy | Dynamic data binding (f-strings) |
| Card designs, hover states, animations | Drag-and-drop JS logic |
| Responsive breakpoints | Chat window server integration |
| New section layouts | Sidebar data population |

### One-Click Deploy

After Claude merges changes:
```bash
bash ~/Desktop/Alon-Workspace/Scripts/deploy-dashboard.sh
```
This regenerates from Notion and deploys to https://vrt-dashboard.netlify.app.

---

*Generated: 2026-02-18 | Source: VRT Dashboard v1.0*
