# VRT Dashboard -- Functionality Specification

**Version:** 1.0
**Date:** 2026-02-18
**Author:** VRT Team
**Status:** Living document

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture](#2-architecture)
3. [Data Model](#3-data-model)
4. [API Endpoints](#4-api-endpoints)
5. [Dashboard Sections](#5-dashboard-sections)
6. [Notion Sidebar](#6-notion-sidebar)
7. [Chat Window](#7-chat-window)
8. [Drag and Drop](#8-drag-and-drop)
9. [Auto-Refresh & Regeneration](#9-auto-refresh--regeneration)
10. [Links Panel](#10-links-panel)
11. [Phase 0 Board](#11-phase-0-board)
12. [Error Handling & Edge Cases](#12-error-handling--edge-cases)

---

## 1. System Overview

### Purpose

The VRT Dashboard is a live operational dashboard for the Virtual Techies team. It visualizes the entire project management state from Notion in a single HTML page, allowing the team to monitor goals, projects, and tasks across Marketing and Product planes. It also provides interactive features: a chat interface for natural-language status updates, drag-and-drop task management, and a Notion sidebar for quick access to item details.

### Deployment

| Environment | URL | Method |
|---|---|---|
| Production | `https://vrt-dashboard.netlify.app` | Netlify CLI manual deploy |
| Local | `http://localhost:3001` | Express server (`node server.js`) |

### Tech Stack

| Component | Technology | File |
|---|---|---|
| Generator | Python 3 | `Scripts/generate-dashboard.py` |
| Server | Express.js (Node.js) | `Scripts/dashboard-server/server.js` |
| Data Source | Notion API v2022-06-28 | curl-based HTTP requests |
| Output | Static HTML5 | `Docs/dashboard.html` |
| Hosting | Netlify | Manual CLI deploy |
| Frontend | Vanilla HTML/CSS/JS | No frameworks |
| Drag & Drop | HTML5 Drag and Drop API | Event delegation in inline `<script>` |

### Data Flow

```
Notion VRT Tracker DB ──curl──> generate-dashboard.py ──write──> dashboard.html
Notion Tool Inventory DB ──curl──> generate-dashboard.py ──write──> dashboard.html
                                                                      │
                                         Express server (server.js) ──serve──> Browser
                                              │
                                         /api/chat ──curl──> Notion (read/write)
                                         /api/move ──curl──> Notion (write) ──> regenerate
                                         /api/tasks ──curl──> Notion (read)
```

---

## 2. Architecture

### Python Generator (`generate-dashboard.py`)

**Location:** `~/Desktop/Alon-Workspace/Scripts/generate-dashboard.py`
**Output:** `~/Desktop/Alon-Workspace/Docs/dashboard.html`

**Execution:**
```bash
python3 ~/Desktop/Alon-Workspace/Scripts/generate-dashboard.py
```

**Behavior:**
1. Queries Notion VRT Tracker DB (paginated, 100 items per page, follows `has_more` cursor)
2. Queries Notion Tool Inventory DB (single page)
3. Parses all items into structured dicts
4. Generates complete HTML document with embedded CSS and JS
5. Writes to output path
6. Opens the file in default browser (`open` command)

**Key Constants:**
- `API_KEY`: Notion integration token
- `TRACKER_DB`: `30a5308b-6bc5-8171-a2c3-d89200293d13`
- `TOOL_INV_DB`: `3408692e-ca14-4886-8143-86ceb7f979e6`
- `LAUNCH_DATE`: `2026-04-17`
- `OUTPUT_PATH`: `~/Desktop/Alon-Workspace/Docs/dashboard.html`

### Express Server (`server.js`)

**Location:** `~/Desktop/Alon-Workspace/Scripts/dashboard-server/server.js`
**Port:** 3001

**Dependencies:**
- `express` ^4.18.2
- `cors` ^2.8.5 (declared but not used in current code)

**Behavior:**
- Serves `dashboard.html` at root (`/`)
- Provides REST API for chat, task queries, drag-and-drop moves, and regeneration
- Uses `child_process.execSync` for Notion API calls via `curl`
- Maintains in-memory chat history (last 50 messages)
- Regenerates dashboard by calling `python3 generate-dashboard.py`

### Notion API Integration

All Notion calls use `curl` via `child_process`. The server wraps this in a helper:

```javascript
function notionRequest(method, endpoint, body) {
  // Constructs curl command with:
  // - Authorization: Bearer <API_KEY>
  // - Notion-Version: 2022-06-28
  // - Content-Type: application/json
  // Timeout: 15 seconds
}
```

---

## 3. Data Model

### VRT Tracker Item

Every item in the VRT Tracker database has this structure:

| Field | Type | Notion Property | Description |
|---|---|---|---|
| `id` | string (UUID) | Page ID | Notion page UUID |
| `name` | string | Name (title) | Item display name |
| `plane` | string | Plane (select) | `"Marketing"` or `"Product"` |
| `level` | string | Level (select) | `"Goal"`, `"Project"`, or `"Task"` |
| `status` | string | Status (select) | `"Not Started"`, `"In Progress"`, `"Done"`, `"Blocked"` |
| `progress` | number (0-1) | Progress (number) | Decimal 0.0 to 1.0 (displayed as percentage) |
| `due` | string (ISO date) | Due (date) | `"YYYY-MM-DD"` format, start date of range |
| `owner` | string | Owner (select) | `"Alon"`, `"Matan"`, or `"Sahar"` |
| `parent_ids` | string[] | Parent (self-relation) | Array of parent page UUIDs |
| `notes` | string | Notes (rich text) | Free-text notes |
| `categories` | string[] | Category (multi_select) | Tags like `"UI/UX"`, `"R&D"`, `"Content"`, etc. |

### Hierarchy

```
Goal (1 per plane)
  └── Project (multiple per goal)
        └── Task (multiple per project)
```

Parent-child relationships are encoded via the `parent_ids` field (self-relation in Notion). Progress rolls up: parent progress = average of children's progress.

### Tool Inventory Item

| Field | Type | Notion Property |
|---|---|---|
| `name` | string | Tool (title) |
| `purpose` | string | Purpose (rich text) |
| `connections` | string[] | Connections (multi_select) |
| `integrated` | boolean | Integrated (checkbox) |
| `core` | string | Core (select) |

### Computed Values

| Value | Formula |
|---|---|
| Days to launch | `LAUNCH_DATE - today` |
| Overall % | `avg(goal.progress) * 100` |
| In Progress count | Items where `status == "In Progress"` and `status != "Done"` |
| Not Started count | Items where `status == "Not Started"` |
| Overdue count | Active items where `due < today` |
| Blocked count | Active items where `status == "Blocked"` |
| This Week count | Tasks with `status != "Done"` and `due <= today + 7 days` |
| Active count | All items where `status != "Done"` |
| Done today | Items where `status == "Done"` and `due == today` |
| Ahead of schedule | Items where `status == "Done"` and `due > today` |
| Per-plane stats | Projects count, tasks count, done count, active count, avg project progress |

---

## 4. API Endpoints

### `GET /`

**Purpose:** Serve the dashboard HTML.

| Aspect | Detail |
|---|---|
| Response | `dashboard.html` file via `res.sendFile()` |
| 404 case | File does not exist: returns `"Dashboard not generated yet. Run generate-dashboard.py first."` |
| Content-Type | `text/html` |

### `POST /api/chat`

**Purpose:** Process natural-language status updates from team members.

**Request Body:**
```json
{
  "name": "Alon",
  "message": "done with market research"
}
```

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Team member name (`"Alon"`, `"Matan"`, `"Sahar"`) |
| `message` | Yes | Natural language message |

**Response:**
```json
{
  "reply": "Updated \"Market Research\" -> Done (100%). Dashboard refreshed.",
  "matched": {
    "id": "page-uuid",
    "name": "Market Research",
    "score": 0.75
  },
  "updated": true
}
```

| Field | Type | Description |
|---|---|---|
| `reply` | string | Human-readable response message |
| `matched` | object or null | The matched task (id, name, score) or null |
| `updated` | boolean | Whether a Notion update was performed |

**Processing Flow:**

1. Validate `name` and `message` are present (400 if not)
2. Store user message in chat history
3. Parse intent from message
4. Query all active tasks from Notion
5. Filter tasks by owner (unless sender is Alon, who sees all tasks)
6. Fuzzy match message against task names
7. If no intent detected: return help message
8. If no task matched: return list of user's active tasks
9. If match found:
   - Update task status in Notion
   - Update progress (Done=1.0, In Progress=max(current, 0.1), Blocked=unchanged)
   - Recalculate parent progress for all parent items
   - Regenerate dashboard HTML
   - Return success message with task name and new status
10. Store bot response in chat history

**Error response:**
```json
{
  "reply": "Error: <message>",
  "matched": null,
  "updated": false
}
```

### `GET /api/chat`

**Purpose:** Retrieve chat history.

**Response:**
```json
[
  {
    "name": "Alon",
    "message": "done with market research",
    "timestamp": "2026-02-18T10:30:00.000Z",
    "type": "user"
  },
  {
    "name": "VRT Bot",
    "message": "Updated \"Market Research\" -> Done (100%). Dashboard refreshed.",
    "timestamp": "2026-02-18T10:30:01.000Z",
    "type": "bot"
  }
]
```

**Behavior:**
- Returns last 50 messages (in-memory, not persisted)
- History resets when server restarts
- Messages ordered chronologically

### `GET /api/tasks`

**Purpose:** Get all active (non-Done) tasks for autocomplete/reference.

**Response:**
```json
[
  {
    "id": "page-uuid",
    "name": "Task name",
    "status": "In Progress",
    "owner": "Alon",
    "plane": "Marketing",
    "due": "2026-02-20",
    "progress": 0.5,
    "parentIds": ["parent-uuid"]
  }
]
```

**Filter:** Level = Task AND Status != Done

### `POST /api/move`

**Purpose:** Update item properties via drag-and-drop (or programmatic call).

**Request Body:**
```json
{
  "pageId": "notion-page-uuid",
  "updates": {
    "status": "Done",
    "owner": "Matan",
    "due": "2026-02-25",
    "progress": 1.0
  }
}
```

| Field | Required | Description |
|---|---|---|
| `pageId` | Yes | Notion page UUID to update |
| `updates` | Yes | Object with one or more fields to update |
| `updates.status` | No | New status value |
| `updates.owner` | No | New owner name |
| `updates.due` | No | New due date (ISO string) |
| `updates.progress` | No | New progress value (0-1) |

**Special behavior:**
- If `updates.status === "Done"`, progress is automatically set to `1.0`
- If status changed, parent progress is recalculated (query parent IDs from Notion, then average children)
- Dashboard regeneration is triggered asynchronously (`setTimeout 100ms`) -- does not block response

**Response:**
```json
{
  "success": true,
  "pageId": "notion-page-uuid",
  "updates": { "status": "Done" }
}
```

**Error:**
```json
{
  "error": "error message"
}
```

### `POST /api/regenerate`

**Purpose:** Manually trigger dashboard regeneration.

**Behavior:** Runs `python3 generate-dashboard.py` with 30-second timeout.

**Response:**
```json
{
  "success": true
}
```

---

## 5. Dashboard Sections

### 5.1 Header

**Purpose:** Brand identification and key context at a glance.

**Content:**
- Title: "VRT Dashboard" with brand colors (V=#6C3AED, R=#5B21B6, T=#8B5CF6)
- Subtitle: `"{Day}, {Month} {Date} -- {N} items tracked -- Launch in {N} days"`

**User flow:** Static display. No interaction.

### 5.2 Metrics Strip

**Purpose:** Single-row summary of all key numbers.

**Metrics displayed (left to right):**

| Metric | Color Class | Background | Text Color |
|---|---|---|---|
| Days to {launch date} | `m-blue` | `#e8f0fe` | `#1967d2` |
| Overall % | `m-dark` | `#e8eaed` | `#3c4043` |
| In Progress | `m-green` | `#e6f4ea` | `#137333` |
| Not Started | `m-yellow` | `#fef7e0` | `#e37400` |
| Overdue | `m-red` | `#fce8e6` | `#c5221f` |
| Blocked | `m-red` | `#fce8e6` | `#c5221f` |
| This Week | `m-blue` | `#e8f0fe` | `#1967d2` |
| Active | `m-dark` | `#e8eaed` | `#3c4043` |

**Layout:** Horizontal flex wrap. Each metric shows a large number (22px, weight 900) with a small uppercase label below.

### 5.3 Done for Today Card

**Purpose:** Celebrate completed work and provide a drag-and-drop target for marking items done.

**Content:**
- Green gradient background card
- Checkmark icon + "Done for Today" heading
- If items completed ahead of schedule: orange badge showing count + fire emoji (&#128293;) on each ahead item
- Grid of completed items, each showing: checkmark, name, plane tag, owner, level
- If nothing completed: dashed border card with "Nothing completed yet -- drop items here!" message

**Two categories of items shown:**
1. **Done today:** `status == "Done"` AND `due == today`
2. **Ahead of schedule:** `status == "Done"` AND `due > today`

**Interactions:**
- Each item has a Notion sidebar button (arrow icon, top-right)
- The entire card is a **drop zone** with `data-drop-status="Done"`
- Dragging a card here sets its status to Done

**Edge cases:**
- Empty state: dashed border, reduced opacity (0.6), placeholder text
- When items are dropped: green highlight on the card (`done-card.drag-over` style)

### 5.4 Overdue Alert

**Purpose:** Draw immediate attention to overdue items.

**Display condition:** Shown only when there are overdue items (active items with `due < today`).

**Content:** Red alert banner listing each overdue item as `"Name (Date, Owner)"`.

### 5.5 Phase 0 Board

See [Section 11: Phase 0 Board](#11-phase-0-board) for full specification.

### 5.6 Goals Section

**Purpose:** High-level view of the 2 main planes (Marketing, Product) with progress tracking.

**Layout:** Grid with `repeat(3, 1fr)` columns (though only 2 goals exist currently).

**Per goal card:**
- Plane-colored top border (5px strip): Marketing=#EA4335, Product=#4285F4
- Pastel background per plane
- Plane tag badge
- Goal name (18px, weight 800)
- Child projects listed as subtitle (up to 4, separated by " / ")
- Progress bar with percentage
- Stats row: `{N} projects`, `{N} tasks`, `{N} done`, `Due {date}`

**Interactions:**
- Hover: border darkens, shadow appears
- Notion sidebar button (top-right arrow)

### 5.7 Projects Board

**Purpose:** Kanban-style board grouped by plane.

**Layout:** Grid with `repeat(3, 1fr)` columns. One column per plane (Marketing, Product).

**Per column:**
- Header: Plane name (colored), count badge
- Bottom border on header (2px solid #e0e3e7)

**Per project card:**
- Pastel background per plane
- Project name (15px, weight 700)
- Owner badge
- Status text (colored by status)
- Due date (red if overdue)
- Task count: `{done}/{total} tasks`
- Progress percentage (colored by plane)
- Progress bar

**Interactions:**
- Draggable (`draggable="true"`)
- Hover: border darkens, shadow
- Notion sidebar button
- Sorted by due date within each column

### 5.8 Tasks Kanban

**Purpose:** Full task board for active work management.

**Layout:** Grid with `repeat(auto-fit, minmax(240px, 1fr))`.

**Columns:**
1. **In Progress** (blue: #4285F4)
2. **Not Started** (grey: #80868b)
3. **Blocked** (red: #EA4335)
4. **Done** (green: #34A853) -- collapsed, opacity 0.6, max 5 items shown

**Per task card:**
- Background: pastel per plane, or red tint if overdue (`border-color:#EA433560; background:#fce8e6`)
- Plane tag (abbreviated: "Mar" / "Pro")
- Task name (weight 600)
- Owner badge
- Parent name (truncated to 20 chars)
- Due date (red if overdue)

**Done column special behavior:**
- Reduced opacity (0.6)
- Task names have `text-decoration: line-through`
- Plane tags reduced size and opacity

**Interactions:**
- All active task cards are **draggable**
- Columns (except Done) are **drop zones** with `data-drop-status="{status}"`
- Notion sidebar button on each card
- Tasks sorted by due date within each column

### 5.9 This Week

**Purpose:** Day-by-day breakdown of upcoming tasks for the next 7 days.

**Display condition:** Only shown if there are tasks due this week.

**Layout:** Grid with `repeat(auto-fit, minmax(160px, 1fr))`.

**Per day card:**
- Day label: `{Day} {Date}` format (e.g., "Wed 19")
- Today's card highlighted: blue border (2px), blue background (#e8f0fe)
- Task entries: plane tag, task name, owner

**Data source:** Tasks where `status != "Done"` and `due <= today + 7 days`, sorted by due date, grouped by `day.strftime("%a %d")`.

### 5.10 Team View

**Purpose:** Per-person workload view.

**Layout:** Grid with `repeat(3, 1fr)` -- one card per team member.

**Team members:** Alon, Matan, Sahar.

**Per team card:**
- Member name (20px, weight 800)
- Active item count + overdue badge (red) if any
- List of active items (up to 10), sorted by due date
- Each item: plane tag, name, overdue warning icon if applicable
- Each card is a **drop zone** with `data-drop-owner="{name}"`

**Interactions:**
- Dragging a card to a team member card reassigns the owner
- Hover: border color changes

### 5.11 Tool Stack

**Purpose:** Inventory of all tools used by the VRT team.

**Display condition:** Only shown if tool data is available.

**Layout:** Grid with `repeat(auto-fill, minmax(220px, 1fr))`.

**Sections:**
- Mini metrics strip: Core count, Integrated count, Not Integrated count
- Tool cards ordered: Core tools first, then others

**Per tool card:**
- Tool name (13px, weight 700)
- Integration dot: green filled (&#9679;) if integrated, grey outline (&#9675;) if not
- Purpose text (truncated to 60 chars)
- CORE badge (if applicable): yellow background
- Connection tags: colored per connection type
- Core tools have gold border (2px solid #FBBC04), others have standard border

**Connection tag colors:**

| Connection | Background | Text |
|---|---|---|
| Notion | `#e8eaed` | `#3c4043` |
| Slack | `#e8f0fe` | `#1967d2` |
| Email | `#fef7e0` | `#e37400` |
| Calendar | `#fff3e0` | `#e65100` |
| Sites/Web | `#e6f4ea` | `#137333` |
| Payments | `#fce8e6` | `#c5221f` |
| CRM | `#f3e5f5` | `#7b1fa2` |
| Docs/Files | `#efebe9` | `#5d4037` |
| Automation | `#e8eaed` | `#3c4043` |
| Claude Code | `#fce4ec` | `#c2185b` |
| Code/Dev | `#e8f0fe` | `#1967d2` |
| Design | `#f3e5f5` | `#7b1fa2` |
| Social Media | `#fce4ec` | `#c2185b` |
| Hosting | `#e6f4ea` | `#137333` |
| AI/Generation | `#fff3e0` | `#e65100` |

### 5.12 Footer

**Content:** `"VRT Tracker -- {timestamp} -- python3 Scripts/generate-dashboard.py to refresh"`

**Style:** Centered, grey (#9aa0a6), 11px, weight 500.

---

## 6. Notion Sidebar

### Purpose

Provides quick access to full item details without leaving the dashboard. Every card (goal, project, task) has a small arrow button that opens a right-side panel showing all item properties and an "Open in Notion" link.

### Trigger

Click the Notion button (`.n-btn`) on any card. The button is hidden by default and appears on hover (transition: `opacity 0 -> 1`).

### Panel Structure

```
┌──────────────────────────┐
│  Item Name          [X]  │  <- sb-head
├──────────────────────────┤
│  [Tool strip]            │  <- sb-tools (dynamic)
├──────────────────────────┤
│  [Level] [Plane] [Status]│  <- Meta badges
│                          │
│  PROGRESS                │
│  ████████░░  75%         │
│                          │
│  OWNER                   │
│  Alon                    │
│                          │
│  DUE                     │
│  2026-03-01              │
│                          │
│  NOTES                   │
│  Free text notes...      │
│                          │
│  TASKS (3)               │  <- Children
│  ● Task 1          50%   │
│  ● Task 2          25%   │
│  ● Task 3           0%   │
├──────────────────────────┤
│  [→ Open in Notion]      │  <- sb-foot
└──────────────────────────┘
```

### Behavior

1. **Open:** `openPanel(id)` sets sidebar content and adds `sb-open` class to body
2. **Toggle:** If same item clicked again, sidebar closes
3. **Close:** Click X button, press Escape key, or click same Notion button
4. **Navigate:** Clicking a child item in the sidebar opens that item's panel
5. **Active state:** The Notion button that triggered the panel gets `active` class (blue background)
6. **Body shift:** Main content shifts left by sidebar width (`margin-right: 380px`)

### Tool Strip

When a panel opens, the sidebar dynamically shows relevant tool icons based on the item's categories:

| Category | Tools Shown |
|---|---|
| UI/UX | Figma, Lovable |
| R&D | GitHub, VS Code, Claude Code |
| Content | Google Drive, YouTube |
| YouTube | YouTube |
| Creative Ads | Midjourney, Figma |
| Business | Notion, Stripe |
| Legal | Notion, Google Drive |
| Infrastructure | GitHub, Netlify |

Fallback: If no categories, shows "Notion".

### Data Source

All items are serialized as JSON in a `<script>` tag (`var _items = {...}`) at generation time. The sidebar reads from this in-memory object -- no API call needed.

### Open in Notion Link

Constructs URL by removing hyphens from the page UUID:
```
https://notion.so/{id.replace(/-/g, '')}
```

---

## 7. Chat Window

### Purpose

Allow team members to update task statuses using natural language without opening Notion. Messages are sent to the server, parsed for intent, matched to tasks, and applied as Notion updates.

### UI Components

1. **FAB (Floating Action Button):** Fixed bottom-right, opens/closes chat window
2. **Chat Window:** Fixed position panel with header, message area, and input
3. **User Selector:** Dropdown in header to select which team member is talking

### User Flow

1. Click FAB to open chat
2. Select your name from dropdown (Alon, Matan, Sahar)
3. Type message like "done with market research"
4. Press Enter or click Send
5. User message appears in chat
6. Server processes and bot responds
7. If update was made: dashboard reloads after 2 seconds

### Chat Command Parser

#### Intent Detection

The parser checks the message (case-insensitive) against keyword lists:

| Intent | Keywords | Resulting Status |
|---|---|---|
| Done | `done`, `finished`, `completed`, `did`, `delivered`, `shipped` | `"Done"` |
| Blocked | `blocked`, `stuck`, `waiting`, `can't` | `"Blocked"` |
| In Progress | `started`, `working on`, `beginning`, `starting` | `"In Progress"` |

**Priority:** Done > Blocked > In Progress (first match wins).

#### Fuzzy Matching

After intent detection, the message is matched against task names:

1. Convert message to lowercase
2. Remove stop words: `i, my, the, a, an, for, to, with, on, today, just, now` + all intent keywords
3. Remove words shorter than 3 characters
4. For each task, count how many remaining keywords appear in the task name (case-insensitive substring match)
5. Score = `matchCount / totalKeywords`
6. Filter tasks with score > 0
7. Sort by score descending
8. Take the best match

#### Owner Filtering

- If the sender is **Alon**: searches all tasks (Alon owns all planes)
- If the sender is anyone else: searches only their owned tasks first
- If owner-filtered search yields no results: falls back to all tasks

#### Progress Updates

| Intent | Progress Rule |
|---|---|
| Done | Set to `1.0` (100%) |
| In Progress | Set to `max(current_progress, 0.1)` (at least 10%) |
| Blocked | No change to progress |

#### Parent Progress Recalculation

After any task update, all parent items have their progress recalculated:
```
parent.progress = avg(children.progress)  // rounded to 2 decimal places
```

### Chat History

- Stored in-memory as array of `{name, message, timestamp, type}` objects
- Maximum 50 messages (oldest removed when exceeded)
- `type` is `"user"` or `"bot"`
- Not persisted across server restarts
- History loaded on chat window open via `GET /api/chat`

### Response Messages

| Scenario | Response Template |
|---|---|
| No intent detected | `"Got it, {name}. I couldn't detect a status update (done/started/blocked) in your message. Try something like "done with [task name]" or "started [task name]"."` |
| No task matched | `"Couldn't find a matching task for "{message}". Your active tasks: {list of up to 5 task names}"` |
| Success | `"Updated "{task}" -> {status} ({progress}%). Dashboard refreshed."` |
| Regen failed | `"Updated "{task}" -> {status} ({progress}%). Dashboard regen failed."` |
| Error | `"Error: {message}"` |

### Post-Update Behavior

When `data.updated === true`:
- Dashboard reloads via `setTimeout(() => location.reload(), 2000)` (2-second delay to allow regeneration)

---

## 8. Drag and Drop

### Overview

The dashboard uses the HTML5 Drag and Drop API with event delegation (single set of listeners on `document`). Any card with `[data-nid][draggable]` can be dragged. Drop zones are elements with the `.drop-zone` class.

### Draggable Items

Any element with both `data-nid` and `draggable="true"` attributes:
- Phase 0 task cards (`.p0-card`)
- Project cards (`.pc`)
- Task cards (`.tk`)

### Drop Zones

| Drop Zone | Data Attribute | Effect |
|---|---|---|
| Task Kanban columns | `data-drop-status="{status}"` | Changes item status |
| Done for Today card | `data-drop-status="Done"` | Marks item as Done |
| Team member cards | `data-drop-owner="{name}"` | Reassigns owner |
| Phase 0 day columns | `data-drop-due="{YYYY-MM-DD}"` | Changes due date |

### Drag Events

#### `dragstart`
1. Find closest `[data-nid][draggable]` ancestor
2. Store `dragId` and `dragEl` references
3. Add `.dragging` class (opacity 0.4, scale 0.97)
4. Set `effectAllowed = 'move'`
5. Set data transfer text to page ID
6. Highlight all `.drop-zone` elements with dashed blue outline

#### `dragover`
1. Find closest `.drop-zone`
2. Prevent default (allow drop)
3. Set `dropEffect = 'move'`
4. Remove `.drag-over` from all other zones
5. Add `.drag-over` to current zone

#### `dragleave`
1. Remove `.drag-over` from the zone

#### `dragend`
1. Remove `.dragging` class from dragged element
2. Clear all highlights and `.drag-over` classes
3. Reset `dragId` and `dragEl`

#### `drop`
1. Prevent default
2. Find closest `.drop-zone`
3. Build `updates` object from zone's data attributes
4. **Optimistic UI:**
   - Add `.drop-flash` class (blue flash animation)
   - If status = Done: reduce opacity, add line-through
5. POST to `/api/move` with `{pageId, updates}`
6. On success: show success toast, reload after 2.5 seconds
7. On failure: show error toast
8. On network error: show "Server offline" toast

### Touch Support

Basic touch support for mobile:
1. `touchstart`: record `touchDragId` from touched card
2. `touchend`: find element at touch coordinates, check if it's a drop zone
3. If drop zone has `data-drop-status`: POST to `/api/move`
4. Reload after 2 seconds

**Limitation:** Touch drag only supports status changes, not owner or date reassignment.

### Toast Notifications

Shown after drag-and-drop operations:

| Type | Background | Text Color |
|---|---|---|
| Success | `#e6f4ea` | `#137333` |
| Error | `#fce8e6` | `#c5221f` |

**Behavior:**
- Fixed position: bottom center
- Auto-dismiss: fade out at 2s, remove at 2.5s
- Style: 14px, weight 600, 10px 24px padding, 10px border-radius

### Server-Side Move Processing

1. Validate `pageId` and `updates`
2. Build Notion properties object:
   - Status -> `{select: {name: value}}`
   - Owner -> `{select: {name: value}}`
   - Due -> `{date: {start: value}}`
   - Progress -> `{number: value}`
3. Special: if status = "Done", also set Progress = 1.0
4. PATCH to Notion
5. If status changed: query page to get parent IDs, recalculate each parent's progress
6. Trigger dashboard regeneration asynchronously (100ms delay, non-blocking)
7. Return success immediately

---

## 9. Auto-Refresh & Regeneration

### Browser Auto-Refresh

```html
<meta http-equiv="refresh" content="60">
```

The dashboard page automatically reloads every **60 seconds** via meta refresh tag.

### Post-Update Reload

| Trigger | Delay | Method |
|---|---|---|
| Chat update (`data.updated === true`) | 2,000ms | `location.reload()` |
| Drag-and-drop move (success) | 2,500ms | `location.reload()` |

### Dashboard Regeneration

Triggered by:
1. Chat updates (synchronous, blocks response)
2. Drag-and-drop moves (asynchronous, 100ms delay)
3. Manual `POST /api/regenerate`

```python
# Server runs:
python3 ~/Desktop/Alon-Workspace/Scripts/generate-dashboard.py
# Timeout: 30 seconds
```

The regeneration process:
1. Queries all items from Notion (paginated)
2. Queries tool inventory
3. Generates full HTML
4. Writes to `Docs/dashboard.html`
5. Next browser request to `/` serves the new file

---

## 10. Links Panel

### Purpose

Collapsible panel with categorized links to all VRT resources.

### Behavior

- Default state: **collapsed** (only header visible)
- Click header to toggle open/close
- Arrow indicator rotates on toggle

### Link Categories

| Category | Color | Links |
|---|---|---|
| **Dashboards & Sites** | `#6C3AED` | VRT Dashboard (live), Dashboard Server (localhost), VRT Domain |
| **Notion** | `#000` | Workspace - VRT, VRT Tracker DB, Feature Board DB, Design Specs, Tool Inventory DB |
| **Dev Tools** | `#4285F4` | GitHub, Netlify, Figma, Lovable |
| **Communication** | `#EA4335` | Slack, Notion Calendar |

### Per Link Item

- Colored dot indicator (matching category)
- Link label
- External link icon (&#8599;)
- Opens in new tab (`target="_blank"`)

---

## 11. Phase 0 Board

### Purpose

A 19-day horizontal timeline board (Feb 18 - Mar 8, 2026) showing all tasks scheduled during the Phase 0 sprint. Provides a visual overview of task distribution across days and team members.

### Date Range

- **Start:** 2026-02-18
- **End:** 2026-03-08
- **Duration:** 19 days

### Layout

Horizontal scrolling container with one column per day. Each column:
- Fixed width: min 160px, max 200px
- Unique pastel background color (19 predefined colors)
- Today's column: 3px solid blue border (#4285F4) + "TODAY" badge

### Day Colors (in order)

```python
["#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#E0F7FA",
 "#FBE9E7", "#E8EAF6", "#F1F8E9", "#FFF8E1", "#FCE4EC",
 "#E0F2F1", "#FFF9C4", "#EDE9FE", "#E1F5FE", "#EFEBE9",
 "#DBEAFE", "#D1FAE5", "#FEF3C7", "#FEE2E2"]
```

### Filter Buttons

Row of filter buttons above the board:
- **All** (default active)
- **Alon**
- **Matan**
- **Sahar**

**Behavior:** Clicking a filter shows/hides cards based on `data-owner` attribute. Active button gets blue background (#4285F4).

### Per Task Card

- Plane tag (abbreviated)
- Status dot: Done=green checkmark, In Progress=blue dot, Blocked=red dot
- Task name (13px, weight 600)
- Category tags (colored per category)
- Owner badge
- Notion sidebar button (top-right, visible on hover)

### Drop Zone

Each day column is a drop zone (`data-drop-due="{YYYY-MM-DD}"`). Dragging a card to a day column changes its due date.

### Data Source

Tasks where `due` falls within the Phase 0 date range. Sorted by owner within each day.

### Empty State

Days with no tasks show an em-dash ("--") centered in grey.

---

## 12. Error Handling & Edge Cases

### Server Not Running

- Chat sends show error: "Could not reach the server. Make sure dashboard-server is running on port 3001."
- Drag-and-drop shows toast: "Server offline -- start dashboard-server"
- Dashboard still viewable as static HTML (file can be opened directly)

### Dashboard Not Generated

- `GET /` returns 404: "Dashboard not generated yet. Run generate-dashboard.py first."

### Notion API Failures

- `notionRequest()` has 15-second timeout
- Dashboard regeneration has 30-second timeout
- Chat endpoint catches errors and returns them in reply text
- Move endpoint returns 500 with error message

### Empty Data Scenarios

| Scenario | Behavior |
|---|---|
| No goals | Goals section renders empty grid |
| No projects in a plane | Empty column in projects board |
| No tasks | Kanban shows empty columns |
| No overdue items | Alert banner not rendered |
| No done-today items | Dashed placeholder card |
| No week tasks | This Week section not rendered |
| No tools data | Tool Stack section not rendered |
| Team member with no items | Team card shows 0 active, no list |
| Item with no parent | Parent name not shown in task footer |
| Item with no due date | Treated as non-overdue, sorted last ("z") |
| Item with no owner | Grouped under "?" in team view |
| Item with no categories | No category tags shown |
| Long item names | CSS handles with line-height; no truncation |
| Long notes | Preserved with `white-space: pre-wrap` in sidebar |

### Chat Edge Cases

| Scenario | Behavior |
|---|---|
| Empty message | 400 error: "name and message required" |
| Missing name | 400 error: "name and message required" |
| No intent keywords | Help message with example syntax |
| Intent found but no task match | Lists up to 5 active tasks |
| Multiple intent keywords | First match wins (Done > Blocked > In Progress) |
| All keywords are stop words | Empty keyword list, no matches |
| Fuzzy match tie | Higher-scored item wins (if equal, order from Notion query) |

### Pagination

The generator handles Notion pagination:
```python
while data.get("has_more"):
    data = notion_query(DB, {"page_size": 100, "start_cursor": data["next_cursor"]})
    items.extend(parse_items(data))
```

The server's `queryActiveTasks()` does **not** paginate (single 100-item page). This means the chat and move features work with up to 100 active tasks.

### Concurrent Updates

- Chat updates are synchronous (one at a time due to `execSync`)
- Move regeneration is async but uses `execSync` for the Python call
- No locking mechanism; concurrent updates to the same item may conflict
- Dashboard reflects latest state on next regeneration

---

## Appendix A: File Paths

| File | Absolute Path |
|---|---|
| Generator script | `~/Desktop/Alon-Workspace/Scripts/generate-dashboard.py` |
| Server script | `~/Desktop/Alon-Workspace/Scripts/dashboard-server/server.js` |
| Package config | `~/Desktop/Alon-Workspace/Scripts/dashboard-server/package.json` |
| Dashboard output | `~/Desktop/Alon-Workspace/Docs/dashboard.html` |

## Appendix B: Notion Database IDs

| Database | ID |
|---|---|
| VRT Tracker | `30a5308b-6bc5-8171-a2c3-d89200293d13` |
| Tool Inventory | `3408692e-ca14-4886-8143-86ceb7f979e6` |

## Appendix C: Server Commands

```bash
# Start server
cd ~/Desktop/Alon-Workspace/Scripts/dashboard-server
npm start          # or: node server.js
npm run dev        # watch mode: node --watch server.js

# Regenerate dashboard
python3 ~/Desktop/Alon-Workspace/Scripts/generate-dashboard.py

# Deploy to Netlify
netlify deploy --prod --dir=~/Desktop/Alon-Workspace/Docs
```
