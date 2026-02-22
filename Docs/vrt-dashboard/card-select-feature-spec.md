# Card Select, Tree Expand & Tool Stack Sync — Feature Spec

> Breaks down the card interaction feature into atomic pieces for implementation.

---

## Overview

Every card on the dashboard (goal, project, task) gets two distinct click behaviors:
1. **Notion link** — small icon, opens Notion sidebar (existing)
2. **Card select** — clicking the card body itself selects it, enlarges it, shows a tree of related items, and updates the tool stack

---

## Piece 1: Two Click Zones Per Card

### What changes
Each card currently has one click behavior (Notion sidebar icon). Now the card gets split into two click zones:

**Zone A — Notion icon (top-right corner)**
- Existing behavior, no change
- Small button, appears on hover
- Opens the Notion sidebar panel

**Zone B — Card body (everything else)**
- NEW behavior
- Clicking the card body selects/deselects the card
- The card itself acts as a button (cursor: pointer)
- Visual feedback: card gets a "selected" state (distinct border/outline)

### Implementation atoms
1. Add `onclick` handler to card body (`.gc`, `.pc`, `.tk`)
2. Prevent the click from bubbling when Notion icon is clicked (stopPropagation)
3. Add `.selected` CSS class for selected state
4. Only one card can be selected at a time (clicking another deselects the previous)
5. Clicking outside any card (on the page background) deselects
6. Pressing Escape key deselects

---

## Piece 2: Card Enlargement (3x)

### What changes
When a card is selected, it enlarges to approximately 3x its normal size, in-place.

### Behavior details
- The card expands **in-place** (not a modal, not a popup — it grows from where it sits)
- It pushes surrounding content down/aside as needed
- Animation: smooth CSS transition (~0.3s ease)
- Enlarged card shows all existing info PLUS the tree overlay (Piece 3)
- The card gets a higher z-index so it doesn't clip

### Implementation atoms
1. On select: add `.expanded` class to the card
2. CSS `.expanded`: set width/height to ~3x, position relative, z-index elevation
3. Transition: `transform: scale(1)` → `transform: scale(1)` with actual width/height change (not CSS scale — we need real space)
4. Alternative: use `grid-column: span 3` (for grid layouts) or `width: 100%` + `min-height: 400px`
5. When deselected: reverse the animation back to normal size

---

## Piece 3: Stickies Tree Overlay

### What changes
When a card is expanded, a "stickies" list appears ON the enlarged card showing the tree of related items.

### Data structure
Every item has a `parent` relation and children can be derived. The tree looks like:

```
Goal (grandparent)
  └── Project (parent)
        ├── Task A (sibling)
        ├── Task B (THIS ITEM — highlighted)
        └── Task C (sibling)
```

### Behavior details
- The stickies appear as small card-like elements (sticky notes) overlaid on the expanded card
- Each sticky shows: item name, status dot, level tag
- The selected item is highlighted/distinct from siblings
- Parent items appear above, children below, siblings alongside

### Implementation atoms
1. Read the embedded JSON sidebar data to get parent/child relationships
2. For a selected task: find its parent (project), grandparent (goal), and siblings (other tasks under same project)
3. For a selected project: find its parent (goal), and children (tasks)
4. For a selected goal: find its children (projects), and grandchildren (tasks under each project)
5. Render sticky elements as a vertical tree inside the expanded card
6. Each sticky has: name, status indicator, level badge
7. A visual connector line between parent and children (optional but nice)

---

## Piece 4: Stickies Are Clickable (Navigate to Position)

### What changes
Each sticky in the tree overlay is clickable. Clicking it:
1. Deselects the current card
2. Scrolls the page to the section where the clicked item lives
3. Selects and expands that item

### Behavior details
- Clicking a parent goal sticky → scrolls to Goals section, selects that goal card
- Clicking a sibling task sticky → scrolls to Tasks Kanban section, selects that task card
- Clicking a child project sticky → scrolls to Projects section, selects that project card
- Smooth scroll animation to the target section
- After scrolling, the target card gets the selected+expanded treatment

### Implementation atoms
1. Each sticky element gets a `data-page-id` attribute matching the Notion page ID
2. On click: call `deselectCurrent()`, then find the card in the DOM with matching page ID
3. Scroll into view: `element.scrollIntoView({ behavior: 'smooth', block: 'center' })`
4. After scroll completes (~500ms timeout): trigger the select+expand on the target card
5. If the target item isn't visible (e.g., in a different status column), still scroll to it

---

## Piece 5: Tool Stack Auto-Update

### What changes
When a card is selected, the Tool Stack section filters to show only tools relevant to that item's context.

### Matching logic
Each task/project has a `categories` array (e.g., `["UI/UX", "R&D"]`). Each tool has a `connections` array (e.g., `["Design", "Code/Dev"]`).

Category-to-connection mapping:

| Task Category | Relevant Tool Connections |
|---|---|
| UI/UX | Design, Sites/Web |
| R&D | Code/Dev, Automation |
| Content | Docs/Files, Sites/Web |
| Creative Ads | Design, AI/Generation |
| YouTube | Social Media, Sites/Web |
| Business | Docs/Files, Automation |
| Legal | Docs/Files |
| Infrastructure | Code/Dev, Automation, Hosting |

### Behavior details
- When a card is selected: filter the tool stack grid to show only matching tools
- Non-matching tools either hide or dim (opacity 0.2)
- The section title updates to show "Tools for [selected item name]"
- CORE tools always show (they're always relevant)
- When no card is selected: show all tools (default state)

### Implementation atoms
1. Build the category→connection mapping as a JS object
2. On card select: read the card's categories from the embedded JSON data
3. Map categories to relevant connection types
4. For each tool card: check if any of its connections match the relevant set
5. If match OR tool is CORE: keep fully visible
6. If no match: add `.tool-dimmed` class (opacity 0.2, pointer-events: none)
7. Update the section title text to include the selected item name
8. On deselect: remove all `.tool-dimmed` classes, restore default title

---

## Piece 6: Escape / Click-Outside to Deselect

### What changes
Global deselect behavior when the user wants to return to the default view.

### Implementation atoms
1. `document.addEventListener('keydown', e => { if (e.key === 'Escape') deselectAll(); })`
2. `document.addEventListener('click', e => { if (!e.target.closest('.gc, .pc, .tk, .tool-card, .sb')) deselectAll(); })`
3. `deselectAll()` function:
   - Remove `.selected` and `.expanded` from all cards
   - Remove the stickies overlay
   - Remove all `.tool-dimmed` classes from tool cards
   - Restore tool stack section title to default

---

## Data Requirements

All data needed is already embedded in the page as JSON (the sidebar data). Specifically:
- `window._sidebarData` — maps page IDs to item details (name, level, status, parent IDs, categories, etc.)
- Parent→child relationships can be derived from the parent field

No additional API calls needed. Everything runs client-side from embedded data.

---

## CSS Classes Summary

| Class | Element | Effect |
|---|---|---|
| `.selected` | Card | Selected visual state (border highlight) |
| `.expanded` | Card | Enlarged to 3x with extra height for stickies |
| `.sticky-tree` | Container | Overlay container for the tree stickies inside expanded card |
| `.sticky` | Individual sticky | Small card-like element in the tree |
| `.sticky.current` | The selected item's sticky | Highlighted/distinct from siblings |
| `.sticky.parent` | Parent item sticky | Slightly larger/elevated |
| `.tree-line` | SVG/CSS line | Visual connector between parent and children |
| `.tool-dimmed` | Tool card | Dimmed when not relevant to selected item |

---

## Interaction Flow (User Story)

1. User sees the Tasks Kanban. Clicks on "Auth prototype" task card.
2. The card enlarges in-place to 3x size.
3. Inside the enlarged card, stickies appear:
   - **Goal:** "Ship MVP Platform" (grandparent)
   - **Project:** "MVP Platform Development" (parent)
   - **Tasks:** Auth system research, Database schema setup, **Auth prototype** (highlighted), Project scaffolding, CI/CD pipeline setup (siblings)
4. Tool Stack section below auto-filters to show: GitHub, VS Code, Claude Code (R&D + Infrastructure categories match Code/Dev, Automation).
5. User clicks the "Database schema setup" sticky.
6. Page scrolls to Tasks Kanban, finds that card, selects and expands it.
7. The tree updates to show the same project's tasks but now "Database schema setup" is highlighted.
8. User presses Escape. Everything returns to default.

---

*Generated: 2026-02-18 | Part of VRT Dashboard feature spec*
