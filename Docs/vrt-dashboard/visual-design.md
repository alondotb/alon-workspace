# VRT Dashboard -- Visual Design Specification

**Version:** 1.0
**Date:** 2026-02-18
**Author:** VRT Team
**Status:** Living document

---

## Table of Contents

1. [Design Foundations](#1-design-foundations)
2. [Color System](#2-color-system)
3. [Typography](#3-typography)
4. [Layout System](#4-layout-system)
5. [Component Catalog](#5-component-catalog)
6. [Sidebar Design](#6-sidebar-design)
7. [Chat Window Design](#7-chat-window-design)
8. [Drag and Drop Visual States](#8-drag-and-drop-visual-states)
9. [Animations and Transitions](#9-animations-and-transitions)
10. [Responsive Design](#10-responsive-design)
11. [Status Indicators](#11-status-indicators)
12. [Plane-Specific Theming](#12-plane-specific-theming)
13. [Category Tag System](#13-category-tag-system)
14. [Icon System](#14-icon-system)

---

## 1. Design Foundations

### Design Philosophy

The VRT Dashboard follows a clean, data-dense design language inspired by Google's Material Design, with a custom brand accent layer. Every element prioritizes readability, scanability, and information density while maintaining visual hierarchy through color, weight, and spacing.

### Font

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

**Google Fonts import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
```

Weights loaded: 400, 500, 600, 700, 800, 900.

### Base Reset

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Page Canvas

```css
body {
  background: #eef0f4;
  color: #202124;
  padding: 28px 48px;
  font-size: 16px;
}
```

---

## 2. Color System

### Brand Palette

| Name | Hex | Usage |
|---|---|---|
| Deep Violet (Primary) | `#6C3AED` | Brand accent, header "V", links panel badge |
| Deep Violet (Dark) | `#5B21B6` | Header "R", darker brand contexts |
| Deep Violet (Light) | `#8B5CF6` | Header "T", lighter brand contexts |

### Plane Colors

| Plane | Primary | Light Background | Border | Tag Background | Tag Text | Tag Border |
|---|---|---|---|---|---|---|
| Marketing | `#EA4335` | `#fef2f1` | `#f5c6c2` | `#fce8e6` | `#c5221f` | `#f5c6c2` |
| Product | `#4285F4` | `#eef3fc` | `#c6dafc` | `#e8f0fe` | `#1967d2` | `#c6dafc` |

### Status Colors

| Status | Primary Color | CSS Class |
|---|---|---|
| In Progress | `#4285F4` | `.s-prog` |
| Done | `#34A853` | `.s-done` |
| Blocked | `#EA4335` | `.s-block` |
| Not Started | `#80868b` | `.s-ns` |

### Metric Block Colors

| Variant | Background | Text Color | CSS Class |
|---|---|---|---|
| Blue | `#e8f0fe` | `#1967d2` | `.m-blue` |
| Green | `#e6f4ea` | `#137333` | `.m-green` |
| Yellow | `#fef7e0` | `#e37400` | `.m-yellow` |
| Red | `#fce8e6` | `#c5221f` | `.m-red` |
| Dark | `#e8eaed` | `#3c4043` | `.m-dark` |

### Semantic Colors

| Purpose | Color | Hex |
|---|---|---|
| Success / Done | Green | `#34A853` |
| Warning | Yellow | `#FBBC04` |
| Error / Blocked / Overdue | Red | `#EA4335` |
| Neutral / Inactive | Grey | `#80868b` |

### Neutral Palette

| Name | Hex | Usage |
|---|---|---|
| Near Black | `#202124` | Primary text, headings |
| Dark Grey | `#3c4043` | Secondary text, body copy |
| Medium Grey | `#5f6368` | Muted text, subtitles, meta info |
| Light Medium Grey | `#80868b` | Labels, tertiary text, parent names |
| Border Light | `#e8eaed` | Card borders, dividers |
| Border Hover | `#dadce0` | Hover state borders |
| Border Dark | `#c5c9cf` | Active hover borders |
| Border Separator | `#e0e3e7` | Column headers, progress bars, separators |
| Surface | `#f8f9fa` | Card backgrounds, column backgrounds |
| Surface Hover | `#f1f3f4` | Hover backgrounds, interactive surfaces |
| Page Background | `#eef0f4` | Body background |
| White | `#ffffff` | Group panels, card surfaces, overlays |
| Muted Text | `#9aa0a6` | Timestamps, footer text |

### Utility Color Classes

```css
.ab { color: #4285F4; }   /* Blue */
.ao { color: #EA4335; }   /* Orange/Red */
.ap { color: #FBBC04; }   /* Yellow */
.ag { color: #34A853; }   /* Green */
.ar { color: #EA4335; }   /* Red (overdue) */
```

---

## 3. Typography

### Type Scale

| Element | Size | Weight | Color | Additional |
|---|---|---|---|---|
| Dashboard title (h1) | `clamp(36px, 5vw, 56px)` | 900 | `#5B21B6` (brand) | `letter-spacing: -.5px` |
| Section title (`.group-t`) | `22px` | 900 | `#202124` | Flex with badge |
| Done card heading | `22px` | 900 | `#137333` | Flex with icon |
| Team member name (`.tn`) | `20px` | 800 | `#202124` | -- |
| Goal title (`.gc h3`) | `18px` | 800 | Plane color | `line-height: 1.3` |
| Goal percentage (`.gc-pct`) | `18px` | 800 | Plane color | -- |
| Links panel title | `18px` | 800 | `#202124` | -- |
| Header subtitle (`.hdr .sub`) | `15px` | 500 | `#5f6368` | `margin-top: 8px` |
| Chat header title | `15px` | 700 | `#fff` | -- |
| Project name (`.pc-name`) | `15px` | 700 | `#202124` | `margin-bottom: 6px` |
| Project column title | `15px` | 800 | Plane color | `text-transform: uppercase; letter-spacing: .6px` |
| Alert text | `15px` | 500 | `#c5221f` | -- |
| Done empty text | `15px` | 600 | `#34A853` | `opacity: .7` |
| Task card name (`.tk-name`) | `14px` | 600 | `#202124` | `line-height: 1.4` |
| Goal subtitle (`.gc-sub`) | `14px` | 400 | `#5f6368` | `line-height: 1.5` |
| This Week task (`.dt`) | `14px` | 400 | `#3c4043` | `line-height: 1.4` |
| Team item (`.tc .ti`) | `14px` | 400 | `#3c4043` | `line-height: 1.4` |
| Toast message | `14px` | 600 | Success/Error color | -- |
| Chat input | `14px` | 400 | -- | -- |
| Done item name | `14px` | 600 | `#202124` | -- |
| Kanban column header | `14px` | 800 | Status color | `text-transform: uppercase; letter-spacing: .6px` |
| Phase 0 card name | `13px` | 600 | `#202124` | `line-height: 1.4` |
| Phase 0 column header | `13px` | 800 | `#3c4043` | `text-align: center` |
| Project meta (`.pc-meta`) | `13px` | 400 | `#5f6368` | -- |
| Goal stats (`.gc-stats`) | `13px` | 600 | `#80868b` | -- |
| Team count (`.tcnt`) | `13px` | 600 | `#5f6368` | -- |
| Owner badge (`.own`) | `13px` | 600 | `#3c4043` | -- |
| Sidebar value (`.sb-val`) | `13px` | 500 | `#202124` | `line-height: 1.5` |
| Link item text (`.lk-item`) | `13px` | 600 | `#202124` | -- |
| Chat bubble text | `13px` | 500 | Varies | `line-height: 1.5` |
| Chat send button | `13px` | 700 | `#fff` | -- |
| Sidebar button text | `13px` | 700 | `#fff` | -- |
| Metric value (`.metric .val`) | `22px` | 900 | Varies | `line-height: 1` |
| Metric label (`.metric .lbl`) | `12px` | 700 | Varies | `text-transform: uppercase; letter-spacing: .5px; opacity: .85` |
| Section badge (`.group-badge`) | `12px` | 700 | `#fff` | `letter-spacing: .3px` |
| Column count badge | `12px` | 700 | `#5f6368` | -- |
| Filter button (`.bf`) | `12px` | 600 | `#3c4043` | -- |
| Chat user select | `12px` | 600 | `#fff` | -- |
| Drag badge | `12px` | 700 | `#fff` | -- |
| Sidebar children item | `12px` | 400 | `#3c4043` | -- |
| Task footer (`.tk-foot`) | `12px` | 500 | `#5f6368` | -- |
| Tag (`.tag`) | `11px` | 700 | Varies | `text-transform: uppercase; letter-spacing: .3px` |
| Done item meta | `11px` | 500 | `#5f6368` | -- |
| Links category label | `11px` | 700 | `#80868b` | `text-transform: uppercase; letter-spacing: .6px` |
| Tool purpose text | `11px` | 400 | `#5f6368` | `line-height: 1.4` |
| Footer timestamp (`.ts`) | `11px` | 500 | `#9aa0a6` | `text-align: center` |
| Sidebar label (`.sb-label`) | `10px` | 700 | `#80868b` | `text-transform: uppercase; letter-spacing: .6px` |
| P0 owner badge | `10px` | 600 | `#5f6368` | -- |
| Chat meta timestamp | `10px` | 500 | `#9aa0a6` | -- |
| Parent label (`.par`) | `10px` | 400 | `#80868b` | -- |
| This Week owner | `10px` | 500 | `#80868b` | -- |
| Category tag (`.cat-tag`) | `9px` | 700 | Varies | `letter-spacing: .2px` |
| P0 plane tag | `9px` | 700 | Varies | -- |
| Done item plane tag | `9px` | 700 | Varies | -- |
| CORE badge on tools | `9px` | 700 | `#e37400` | -- |
| Connection tags on tools | `9px` | 600 | Varies | -- |

### Text Patterns

**Uppercase labels:** Used for metric labels, section badges, column headers, sidebar labels, link categories, tags. Always paired with `letter-spacing` (0.3px to 0.8px).

**Line-through:** Applied to task names in the Done column: `text-decoration: line-through; color: #9aa0a6`.

---

## 4. Layout System

### Page Structure

```
<body>
  <div class="sb">            <!-- Sidebar (fixed right) -->
  <div class="dash-wrap">     <!-- Main content wrapper -->
    <div class="c">           <!-- Content container -->
      .hdr                    <!-- Header -->
      .group (metrics)        <!-- Metrics strip -->
      .done-card              <!-- Done for today -->
      .alert                  <!-- Overdue alert (conditional) -->
      .group (Phase 0)        <!-- Phase 0 board -->
      .group (Goals)          <!-- Goals section -->
      .group (Projects)       <!-- Projects board -->
      .group (Tasks)          <!-- Tasks kanban -->
      .group (This Week)      <!-- This week (conditional) -->
      .group (Team)           <!-- Team view -->
      .group (Tool Stack)     <!-- Tool stack (conditional) -->
      .links-panel            <!-- Links panel -->
      .ts                     <!-- Footer timestamp -->
    </div>
  </div>
  <button class="chat-fab">   <!-- Chat FAB (fixed) -->
  <div class="chat-win">      <!-- Chat window (fixed) -->
</body>
```

### Group Panel (Section Container)

Every major section is wrapped in `.group`:

```css
.group {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}
```

The metrics strip uses reduced padding: `padding: 16px 20px`.

### Grid Definitions

| Section | Grid | Columns | Gap |
|---|---|---|---|
| Goals | `.goals` | `repeat(3, 1fr)` | `14px` |
| Projects | `.proj-board` | `repeat(3, 1fr)` | `14px` |
| Tasks | `.task-board` | `repeat(auto-fit, minmax(240px, 1fr))` | `14px` |
| This Week | `.days` | `repeat(auto-fit, minmax(160px, 1fr))` | `10px` |
| Team | `.tg` | `repeat(3, 1fr)` | `14px` |
| Done list | `.done-list` | `repeat(auto-fill, minmax(260px, 1fr))` | `10px` |
| Tool cards | inline style | `repeat(auto-fill, minmax(220px, 1fr))` | `10px` |
| Links grid | `.links-grid` | `repeat(auto-fill, minmax(220px, 1fr))` | `8px` |
| Metrics | `.metrics` | flex-wrap | `8px` |

### Phase 0 Board Layout

```css
.phase0-board {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 12px;
  -webkit-overflow-scrolling: touch;
}

.p0-col {
  min-width: 160px;
  max-width: 200px;
  flex-shrink: 0;
}
```

Horizontal scrolling container with fixed-width columns.

---

## 5. Component Catalog

### 5.1 Metric Block

```
┌──────────────┐
│  58   DAYS   │
│       TO APR │
│       17     │
└──────────────┘
```

```css
.metric {
  border-radius: 10px;
  padding: 8px 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  border: none;
}
```

| Property | Value |
|---|---|
| Border radius | `10px` |
| Padding | `8px 14px` |
| Layout | Flex row, center-aligned |
| Gap | `8px` |
| Value size | `22px`, weight 900 |
| Label size | `12px`, weight 700, uppercase |

### 5.2 Goal Card (`.gc`)

```
┌─────────────────────────────────────┐
│▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀│  <- 5px color strip
│ [MAR]                          [→]  │  <- Plane tag + Notion btn
│ Marketing Launch Goal               │  <- Title
│ Project 1 / Project 2 / Project 3   │  <- Child projects
│ ████████████░░░░  75%               │  <- Progress bar + pct
│ 5 projects  12 tasks  3 done  Apr 1 │  <- Stats row
└─────────────────────────────────────┘
```

```css
.gc {
  background: #f8f9fa;
  border-radius: 14px;
  padding: 20px;
  position: relative;
  overflow: hidden;
  border: 1px solid #e8eaed;
  transition: border-color .15s, box-shadow .15s;
}

.gc::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  /* Color set by .gc-m or .gc-p */
}
```

| Property | Value |
|---|---|
| Background | `#f8f9fa` (plane pastel override applied via inline) |
| Border radius | `14px` |
| Padding | `20px` |
| Border | `1px solid #e8eaed` |
| Top strip | `5px` height, plane color |
| Hover border | `#dadce0` |
| Hover shadow | `0 4px 16px rgba(0, 0, 0, 0.08)` |

**Plane pastel backgrounds:**
- Marketing: `background: #fef2f1; border-color: #f5c6c2`
- Product: `background: #eef3fc; border-color: #c6dafc`

### 5.3 Project Card (`.pc`)

```
┌────────────────────────────────┐
│                           [→]  │
│ Project Name                   │
│ [Alon]    In Progress          │
│ Feb 28    3/5 tasks    60%     │
│ ████████░░░░                   │
└────────────────────────────────┘
```

```css
.pc {
  background: #fff;
  border: 1px solid #e8eaed;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 10px;
  transition: border-color .15s, box-shadow .15s;
}
```

| Property | Value |
|---|---|
| Background | `#fff` (plane pastel override via inline) |
| Border radius | `10px` |
| Padding | `16px` |
| Margin bottom | `10px` (between cards) |
| Hover border | `#c5c9cf` |
| Hover shadow | `0 2px 8px rgba(0, 0, 0, 0.06)` |

### 5.4 Task Card (`.tk`)

```
┌──────────────────────────────────┐
│                             [→]  │
│ [MAR] Task Name                  │
│ [Alon]    Project...    Feb 20   │
└──────────────────────────────────┘
```

```css
.tk {
  background: #fff;
  border: 1px solid #e8eaed;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 8px;
  font-size: 14px;
  transition: border-color .15s, box-shadow .15s;
}
```

| Property | Value |
|---|---|
| Background | `#fff` (plane pastel or overdue red via inline) |
| Border radius | `8px` |
| Padding | `14px 16px` |
| Margin bottom | `8px` |
| Hover border | `#c5c9cf` |
| Hover shadow | `0 2px 8px rgba(0, 0, 0, 0.06)` |

**Overdue task styling:**
```css
border-color: #EA433560;
background: #fce8e6;
```

### 5.5 Phase 0 Card (`.p0-card`)

```
┌─────────────────────┐
│ [MAR] ●        [→]  │
│ Task Name            │
│ [UI/UX] [Content]   │
│ [Alon]               │
└─────────────────────┘
```

```css
.p0-card {
  background: #fff;
  border: 1px solid #e0e3e7;
  border-radius: 8px;
  padding: 8px 10px;
  margin-bottom: 6px;
  transition: box-shadow .15s;
}
```

| Property | Value |
|---|---|
| Background | `#fff` |
| Border | `1px solid #e0e3e7` |
| Border radius | `8px` |
| Padding | `8px 10px` |
| Margin bottom | `6px` |
| Hover shadow | `0 2px 8px rgba(0, 0, 0, 0.1)` |

### 5.6 Day Card (`.dc`)

```
┌─────────────────┐
│ WED 19          │
│ [MAR] Task 1    │
│   Alon          │
│ [PRO] Task 2    │
│   Matan         │
└─────────────────┘
```

```css
.dc {
  background: #f8f9fa;
  border: 1px solid #e8eaed;
  border-radius: 10px;
  padding: 14px;
}

.dc.today {
  border-color: #4285F4;
  border-width: 2px;
  background: #e8f0fe;
}
```

| Property | Default | Today |
|---|---|---|
| Background | `#f8f9fa` | `#e8f0fe` |
| Border | `1px solid #e8eaed` | `2px solid #4285F4` |
| Border radius | `10px` | `10px` |
| Padding | `14px` | `14px` |

**Day label:**
```css
.dl {
  font-size: 13px;
  font-weight: 800;
  color: #4285F4;
  text-transform: uppercase;
  letter-spacing: .8px;
  margin-bottom: 10px;
}
```

### 5.7 Team Card (`.tc`)

```
┌─────────────────────┐
│ Alon                 │
│ 8 active (2 overdue) │
│ [MAR] Task 1         │
│ [PRO] Task 2         │
│ [MAR] Task 3 ⚠       │
└─────────────────────┘
```

```css
.tc {
  background: #f8f9fa;
  border: 1px solid #e8eaed;
  border-radius: 12px;
  padding: 18px;
}

.tc:hover {
  border-color: #c5c9cf;
}
```

| Property | Value |
|---|---|
| Background | `#f8f9fa` |
| Border radius | `12px` |
| Padding | `18px` |
| Hover border | `#c5c9cf` |

### 5.8 Tool Card

```
┌──────────────────────────┐
│ Notion             ●     │
│ Central workspace... CORE│
│ [Slack] [Calendar] [Docs]│
└──────────────────────────┘
```

```css
/* Inline styles in generated HTML */
background: #f8f9fa;
border: 1px solid #e8eaed;  /* or 2px solid #FBBC04 for CORE */
border-radius: 10px;
padding: 12px;
transition: box-shadow .15s;
```

| Property | Standard | CORE |
|---|---|---|
| Border | `1px solid #e8eaed` | `2px solid #FBBC04` |
| Hover shadow | `0 2px 8px rgba(0, 0, 0, 0.08)` | `0 2px 8px rgba(0, 0, 0, 0.08)` |

### 5.9 Done Item Card

```
┌────────────────────────────────────────┐
│ ✓  Task Name  🔥   [MAR] Alon · Task  │
└────────────────────────────────────────┘
```

```css
.done-item {
  background: #fff;
  border: 1px solid #34A85340;
  border-radius: 10px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: box-shadow .15s;
}

.done-item:hover {
  box-shadow: 0 2px 8px rgba(52, 168, 83, 0.15);
}
```

| Property | Value |
|---|---|
| Background | `#fff` |
| Border | `1px solid #34A85340` (green, 25% opacity) |
| Border radius | `10px` |
| Padding | `12px 16px` |
| Checkmark color | `#34A853` at 18px |
| Fire icon | 16px, shown only for ahead-of-schedule items |

### 5.10 Done for Today Container

```css
.done-card {
  background: linear-gradient(135deg, #e6f4ea 0%, #d4edda 100%);
  border: 2px solid #34A853;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
}
```

**Empty state:**
```css
border-style: dashed;
opacity: 0.6;
```

### 5.11 Link Item

```
┌─────────────────────────┐
│ ● VRT Dashboard (live) ↗│
└─────────────────────────┘
```

```css
.lk-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #e8eaed;
  text-decoration: none;
  color: #202124;
  font-size: 13px;
  font-weight: 600;
  transition: background .15s, border-color .15s;
}

.lk-item:hover {
  background: #f1f3f4;
  border-color: #dadce0;
}
```

**Dot indicator:**
```css
.lk-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}
```

### 5.12 Progress Bar

```css
.pb {
  width: 100%;
  height: 6px;
  background: #e0e3e7;
  border-radius: 3px;
  overflow: hidden;
  margin-top: 12px;
}

.pf {
  height: 100%;
  border-radius: 3px;
  /* width and background set inline per item */
}
```

| Property | Track | Fill |
|---|---|---|
| Height | `6px` | `6px` |
| Background | `#e0e3e7` | Plane color |
| Border radius | `3px` | `3px` |

**Sidebar progress bar (larger):**
```css
.sb-bar {
  width: 100%;
  height: 8px;
  background: #e0e3e7;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 6px;
}

.sb-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width .4s ease;
}
```

### 5.13 Tag (Plane Indicator)

```css
.tag {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .3px;
  vertical-align: middle;
}

.tag-m {
  background: #fce8e6;
  color: #c5221f;
  border: 1px solid #f5c6c2;
}

.tag-p {
  background: #e8f0fe;
  color: #1967d2;
  border: 1px solid #c6dafc;
}
```

Content is abbreviated plane name: "Mar" for Marketing, "Pro" for Product.

### 5.14 Owner Badge

```css
.own {
  padding: 3px 10px;
  background: #e8eaed;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #3c4043;
}
```

### 5.15 Section Badge

```css
.group-badge {
  font-size: 12px;
  font-weight: 700;
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  letter-spacing: .3px;
}
```

**Badge colors per section:**

| Section | Background |
|---|---|
| Phase 0 Board | `#4285F4` |
| Goals | `#34A853` |
| Projects | `#4285F4` |
| Tasks | `#EA4335` |
| This Week | `#FBBC04` (text: `#202124`) |
| Team | `#202124` |
| Tool Stack | `#202124` |
| Links | `#6C3AED` |

### 5.16 Filter Button (`.bf`)

```css
.bf {
  padding: 6px 16px;
  border: 1px solid #dadce0;
  border-radius: 20px;
  background: #fff;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all .15s;
  font-family: inherit;
  color: #3c4043;
}

.bf:hover {
  background: #f1f3f4;
}

.bf.active {
  background: #4285F4;
  color: #fff;
  border-color: #4285F4;
}
```

### 5.17 Alert Banner

```css
.alert {
  background: #fce8e6;
  border: 1px solid #f5c6c2;
  border-radius: 10px;
  padding: 14px 18px;
  margin-bottom: 20px;
  font-size: 15px;
  color: #c5221f;
  font-weight: 500;
}

.alert b {
  color: #EA4335;
}
```

### 5.18 Column (Kanban / Project)

**Project column:**
```css
.proj-col {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 14px;
  border: 1px solid #e8eaed;
}
```

**Task column:**
```css
.task-col {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 14px;
  border: 1px solid #e8eaed;
}
```

**Column header (shared pattern):**
```css
/* Project */
.proj-col-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e0e3e7;
}

/* Task */
.task-col-head {
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .6px;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e0e3e7;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

**Column count badge:**
```css
.col-count {
  font-size: 12px;
  font-weight: 700;
  color: #5f6368;
  background: #e0e3e7;
  padding: 2px 10px;
  border-radius: 8px;  /* task-col uses 8px, proj-col uses 10px */
}
```

### 5.19 Phase 0 Day Column

```css
.p0-col {
  min-width: 160px;
  max-width: 200px;
  flex-shrink: 0;
  border-radius: 12px;
  padding: 10px;
  border: 1px solid #e0e3e7;
  /* background: unique pastel color per day (inline) */
}
```

**Today indicator:**
```css
/* Applied inline */
border: 3px solid #4285F4;
```

**TODAY badge (inline):**
```css
background: #4285F4;
color: #fff;
padding: 1px 8px;
border-radius: 8px;
font-size: 10px;
font-weight: 700;
```

---

## 6. Sidebar Design

### Container

```css
.sb {
  position: fixed;
  top: 0;
  right: -400px;           /* Hidden by default */
  width: 380px;
  height: 100vh;
  background: #fff;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: right .3s cubic-bezier(.4, 0, .2, 1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

body.sb-open .sb {
  right: 0;
}
```

### Body Content Shift

```css
.dash-wrap {
  transition: margin-right .3s cubic-bezier(.4, 0, .2, 1);
}

body.sb-open .dash-wrap {
  margin-right: 380px;
}
```

### Sidebar Header

```css
.sb-head {
  padding: 20px 20px 16px;
  border-bottom: 1px solid #e8eaed;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-shrink: 0;
}

.sb-head h2 {
  font-size: 16px;
  font-weight: 800;
  color: #202124;
  line-height: 1.3;
  flex: 1;
  margin-right: 12px;
}
```

### Close Button

```css
.sb-close {
  width: 28px;
  height: 28px;
  border: none;
  background: #f1f3f4;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background .15s;
}

.sb-close:hover {
  background: #e0e3e7;
}
```

### Sidebar Body

```css
.sb-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}
```

### Sidebar Row

```css
.sb-row {
  margin-bottom: 14px;
}

.sb-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: .6px;
  font-weight: 700;
  color: #80868b;
  margin-bottom: 4px;
}

.sb-val {
  font-size: 13px;
  color: #202124;
  font-weight: 500;
  line-height: 1.5;
}
```

### Sidebar Children List

```css
.sb-children {
  list-style: none;
  padding: 0;
}

.sb-children li {
  font-size: 12px;
  color: #3c4043;
  padding: 6px 10px;
  border-radius: 6px;
  margin-bottom: 4px;
  border: 1px solid #e8eaed;
  cursor: pointer;
  transition: background .1s;
}

.sb-children li:hover {
  background: #f1f3f4;
}
```

### Sidebar Footer

```css
.sb-foot {
  padding: 16px 20px;
  border-top: 1px solid #e8eaed;
  flex-shrink: 0;
}
```

### Open in Notion Button

```css
.sb-notion {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 10px;
  background: #202124;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: background .15s;
  text-decoration: none;
}

.sb-notion:hover {
  background: #3c4043;
}
```

### Notion Toggle Button (on cards)

```css
.n-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  border: 1px solid #dadce0;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;               /* Hidden by default */
  transition: opacity .15s, background .1s, border-color .1s;
  z-index: 2;
}

.n-btn:hover {
  background: #f1f3f4;
  border-color: #c5c9cf;
}

.n-btn.active {
  opacity: 1;
  background: #4285F4;
  border-color: #4285F4;
}

.n-btn.active svg {
  stroke: #fff;
}

/* Show on parent hover */
*:hover > .n-btn,
*:hover .n-btn-wrap .n-btn {
  opacity: 1;
}
```

**Smaller variant (on P0 cards and done items):**
```css
/* Applied inline */
top: 4px;
right: 4px;
width: 20px;
height: 20px;
```

### Tool Strip (Dynamic)

```css
/* Created via JavaScript */
display: flex;
gap: 6px;
flex-wrap: wrap;
padding: 12px 20px 0;
border-top: 1px solid #e8eaed;
```

**Tool badge in strip:**
```css
padding: 4px 10px;
border-radius: 8px;
font-size: 11px;
font-weight: 700;
background: {toolColor}18;  /* 9% opacity */
color: {toolColor};
border: 1px solid {toolColor}30;  /* 19% opacity */
```

**Tool badge colors:**

| Tool | Color |
|---|---|
| Figma | `#A259FF` |
| Lovable | `#FF6B6B` |
| GitHub | `#333` |
| VS Code | `#007ACC` |
| Claude Code | `#D97706` |
| Google Drive | `#4285F4` |
| YouTube | `#FF0000` |
| Midjourney | `#0D1117` |
| Notion | `#000` |
| Stripe | `#635BFF` |
| Netlify | `#00C7B7` |

---

## 7. Chat Window Design

### FAB (Floating Action Button)

```css
.chat-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #4285F4;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(66, 133, 244, 0.4);
  z-index: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform .2s, box-shadow .2s;
}

.chat-fab:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 24px rgba(66, 133, 244, 0.5);
}
```

**Icon:** SVG chat bubble, 24x24, white stroke, stroke-width 2.

### Chat Window

```css
.chat-win {
  position: fixed;
  bottom: 90px;
  right: 24px;
  width: 380px;
  max-height: 500px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 900;
  display: none;
  flex-direction: column;
  overflow: hidden;
}

.chat-win.open {
  display: flex;
}
```

### Chat Header

```css
.chat-hdr {
  padding: 14px 18px;
  background: #4285F4;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-hdr h3 {
  font-size: 15px;
  font-weight: 700;
  margin: 0;
}

.chat-hdr select {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  outline: none;
}

.chat-hdr select option {
  color: #202124;
  background: #fff;
}
```

### Message Area

```css
.chat-msgs {
  flex: 1;
  overflow-y: auto;
  padding: 14px;
  max-height: 340px;
  min-height: 120px;
}
```

### Message Bubbles

```css
.chat-msg {
  margin-bottom: 10px;
  max-width: 85%;
}

.chat-msg.user {
  margin-left: auto;
}

.chat-msg.bot {
  margin-right: auto;
}

.chat-msg .chat-bubble {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.5;
  font-weight: 500;
}

/* User bubble */
.chat-msg.user .chat-bubble {
  background: #e8f0fe;
  color: #1967d2;
  border-bottom-right-radius: 4px;
}

/* Bot bubble */
.chat-msg.bot .chat-bubble {
  background: #f1f3f4;
  color: #3c4043;
  border-bottom-left-radius: 4px;
}
```

| Property | User | Bot |
|---|---|---|
| Alignment | Right (auto margin-left) | Left (auto margin-right) |
| Background | `#e8f0fe` | `#f1f3f4` |
| Text color | `#1967d2` | `#3c4043` |
| Corner exception | Bottom-right: 4px | Bottom-left: 4px |

### Message Meta

```css
.chat-msg .chat-meta {
  font-size: 10px;
  color: #9aa0a6;
  margin-top: 3px;
  font-weight: 500;
}

.chat-msg.user .chat-meta {
  text-align: right;
}
```

### Input Area

```css
.chat-input {
  display: flex;
  gap: 8px;
  padding: 12px 14px;
  border-top: 1px solid #e8eaed;
}

.chat-input input {
  flex: 1;
  border: 1px solid #dadce0;
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color .15s;
}

.chat-input input:focus {
  border-color: #4285F4;
}

.chat-input button {
  background: #4285F4;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  font-family: inherit;
  transition: background .15s;
  white-space: nowrap;
}

.chat-input button:hover {
  background: #1967d2;
}
```

---

## 8. Drag and Drop Visual States

### Draggable Elements

```css
[draggable=true] {
  cursor: grab;
  user-select: none;
}

[draggable=true]:active {
  cursor: grabbing;
}
```

### Dragging State

```css
.dragging {
  opacity: .4;
  transform: scale(.97);
  transition: opacity .15s, transform .15s;
}
```

### Drop Zone Base

```css
.drop-zone {
  transition: background .2s, border-color .2s, box-shadow .2s;
}
```

### Drop Zone Highlight (during drag)

Applied via JavaScript when any drag starts:
```css
/* All drop zones get */
outline: 2px dashed #4285F440;
outline-offset: -2px;
```

### Drop Zone Active Hover

```css
.drop-zone.drag-over {
  background: #e8f0fe !important;
  border-color: #4285F4 !important;
  box-shadow: inset 0 0 0 2px #4285F4;
}
```

### Done Card Drop Active

```css
.done-card.drag-over {
  background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%) !important;
  border-color: #2E7D32 !important;
  box-shadow: inset 0 0 0 2px #2E7D32;
}
```

### Drop Ghost (Position Indicator)

```css
.drop-ghost {
  height: 4px;
  background: #4285F4;
  border-radius: 2px;
  margin: 4px 0;
  transition: all .15s;
}
```

### Drag Badge (Floating Label)

```css
.drag-badge {
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  background: #4285F4;
  color: #fff;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
  max-width: 260px;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

### Drop Flash Animation

```css
@keyframes drop-flash {
  0%   { background: #e8f0fe; }
  100% { background: transparent; }
}

.drop-flash {
  animation: drop-flash .6s ease;
}
```

### Post-Drop Done State (Optimistic UI)

When an item is dropped on a "Done" zone:
```css
/* Applied via JavaScript */
opacity: .5;
text-decoration: line-through;
```

---

## 9. Animations and Transitions

### Transition Summary

| Element | Property | Duration | Easing |
|---|---|---|---|
| Goal card | `border-color, box-shadow` | `0.15s` | ease (default) |
| Project card | `border-color, box-shadow` | `0.15s` | ease |
| Task card | `border-color, box-shadow` | `0.15s` | ease |
| P0 card | `box-shadow` | `0.15s` | ease |
| Done item | `box-shadow` | `0.15s` | ease |
| Link item | `background, border-color` | `0.15s` | ease |
| Filter button | `all` | `0.15s` | ease |
| Notion button | `opacity, background, border-color` | `0.15s` | ease |
| Close button | `background` | `0.15s` | ease |
| Chat FAB | `transform, box-shadow` | `0.2s` | ease |
| Chat input | `border-color` | `0.15s` | ease |
| Chat send button | `background` | `0.15s` | ease |
| Notion "Open" button | `background` | `0.15s` | ease |
| Links arrow | `transform` | `0.2s` | ease |
| Drop zone | `background, border-color, box-shadow` | `0.2s` | ease |
| Dragging element | `opacity, transform` | `0.15s` | ease |
| Drop ghost | `all` | `0.15s` | ease |
| Sidebar slide | `right` | `0.3s` | `cubic-bezier(.4, 0, .2, 1)` |
| Content shift | `margin-right` | `0.3s` | `cubic-bezier(.4, 0, .2, 1)` |
| Sidebar progress fill | `width` | `0.4s` | ease |
| Sidebar children hover | `background` | `0.1s` | ease |
| Drop flash | animation | `0.6s` | ease |
| Toast opacity | `opacity` | `0.3s` | ease (implicit) |

### Keyframe Animations

**Drop Flash:**
```css
@keyframes drop-flash {
  0%   { background: #e8f0fe; }
  100% { background: transparent; }
}
```
Duration: 0.6s. Applied once on drop.

### Toast Lifecycle

1. Created: immediately visible
2. 2000ms: `opacity: 0` (fade out)
3. 2500ms: element removed from DOM

### Chat FAB Hover

```css
.chat-fab:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 24px rgba(66, 133, 244, 0.5);
}
```

### Sidebar Easing

Uses `cubic-bezier(.4, 0, .2, 1)` (Material Design standard easing) for both:
- Sidebar slide in/out
- Content margin shift

---

## 10. Responsive Design

### Breakpoints

| Breakpoint | Width | Changes |
|---|---|---|
| **Desktop** | > 1024px | Full layout, 48px padding |
| **Tablet** | <= 1024px | Reduced padding |
| **Tablet narrow** | <= 900px | Single-column goals/projects/team, sidebar narrower |
| **Mobile** | <= 640px | 2-column grids collapse, sidebar full-width |
| **Small mobile** | <= 480px | Single-column everywhere, chat repositioned |

### Breakpoint Details

#### `max-width: 1024px`

```css
body {
  padding: 20px 28px;
}

.group {
  padding: 20px;
}
```

#### `max-width: 900px`

```css
.goals,
.proj-board,
.tg {
  grid-template-columns: 1fr;
}

.gc .gc-pct {
  font-size: 28px;
}

.sb {
  width: 320px;
}

body.sb-open .dash-wrap {
  margin-right: 320px;
}
```

#### `max-width: 640px`

```css
.days,
.task-board {
  grid-template-columns: 1fr 1fr;
}

.tg {
  grid-template-columns: 1fr;
}

body {
  padding: 14px 16px;
}

.group {
  padding: 16px;
  border-radius: 12px;
}

.hdr h1 {
  font-size: 28px;
}

/* Sidebar takes full width */
.sb {
  width: 100%;
  right: -100%;
}

body.sb-open .dash-wrap {
  margin-right: 0;   /* Content stays, sidebar overlays */
}
```

#### `max-width: 480px`

```css
.task-board,
.days {
  grid-template-columns: 1fr;
}

.chat-win {
  width: calc(100% - 32px);
  right: 16px;
  bottom: 80px;
}

.chat-fab {
  bottom: 16px;
  right: 16px;
}
```

### Responsive Behavior Summary

| Component | Desktop | 1024px | 900px | 640px | 480px |
|---|---|---|---|---|---|
| Body padding | 28px 48px | 20px 28px | 20px 28px | 14px 16px | 14px 16px |
| Group padding | 24px | 20px | 20px | 16px | 16px |
| Group radius | 16px | 16px | 16px | 12px | 12px |
| Goals grid | 3 col | 3 col | 1 col | 1 col | 1 col |
| Projects grid | 3 col | 3 col | 1 col | 1 col | 1 col |
| Tasks grid | auto-fit 240px | auto-fit 240px | auto-fit 240px | 2 col | 1 col |
| This Week grid | auto-fit 160px | auto-fit 160px | auto-fit 160px | 2 col | 1 col |
| Team grid | 3 col | 3 col | 1 col | 1 col | 1 col |
| Sidebar width | 380px | 380px | 320px | 100% | 100% |
| Sidebar behavior | Push content | Push content | Push content | Overlay | Overlay |
| Chat window width | 380px | 380px | 380px | 380px | 100%-32px |
| Header h1 | clamp(36-56px) | clamp | clamp | 28px | 28px |

---

## 11. Status Indicators

### Status Text

```css
.s-prog  { color: #4285F4; font-weight: 700; }  /* In Progress */
.s-done  { color: #34A853; font-weight: 700; }  /* Done */
.s-block { color: #EA4335; font-weight: 700; }  /* Blocked */
.s-ns    { color: #80868b; font-weight: 600; }  /* Not Started */
```

### Status Dots (Phase 0 Board)

| Status | Display | Color | Size |
|---|---|---|---|
| Done | Checkmark (&#10003;) | `#34A853` | 14px |
| In Progress | Filled circle (&#9679;) | `#4285F4` | 10px |
| Blocked | Filled circle (&#9679;) | `#EA4335` | 10px |
| Not Started | None | -- | -- |

### Sidebar Status Badges

Dynamic badges in the sidebar meta row:

```css
/* Pattern */
padding: 3px 10px;
border-radius: 8px;
font-size: 11px;
font-weight: 700;
color: {statusColor};
border: 1px solid {statusColor}30;  /* 19% opacity border */
```

### Sidebar Children Dots

```css
display: inline-block;
width: 6px;
height: 6px;
border-radius: 50%;
margin-right: 6px;
background: {statusColor};
```

| Status | Color |
|---|---|
| In Progress | `#4285F4` |
| Done | `#34A853` |
| Blocked | `#EA4335` |
| Not Started | `#ccc` |

### Overdue Indicator

- Task cards: Red tinted background (`#fce8e6`) and red border (`#EA433560`)
- Text: `.ar` class applies `color: #EA4335`
- Team view: Warning icon (&#9888;) appended to item name
- Alert banner: Full-width red banner at top

### Integration Dots (Tool Stack)

```
● Integrated:     color:#34A853  (&#9679; filled circle)
○ Not integrated:  color:#dadce0  (&#9675; open circle)
```
Size: 12px.

---

## 12. Plane-Specific Theming

### Marketing (Red Plane)

| Context | Property | Value |
|---|---|---|
| Primary color | -- | `#EA4335` |
| Card background | `background` | `#fef2f1` |
| Card border | `border-color` | `#f5c6c2` |
| Tag background | `.tag-m background` | `#fce8e6` |
| Tag text | `.tag-m color` | `#c5221f` |
| Tag border | `.tag-m border` | `1px solid #f5c6c2` |
| Goal top strip | `.gc-m::before` | `#EA4335` |
| Progress bar fill | -- | `#EA4335` |
| Column header text | -- | `#EA4335` |
| Tag content | -- | "Mar" (abbreviated) |

### Product (Blue Plane)

| Context | Property | Value |
|---|---|---|
| Primary color | -- | `#4285F4` |
| Card background | `background` | `#eef3fc` |
| Card border | `border-color` | `#c6dafc` |
| Tag background | `.tag-p background` | `#e8f0fe` |
| Tag text | `.tag-p color` | `#1967d2` |
| Tag border | `.tag-p border` | `1px solid #c6dafc` |
| Goal top strip | `.gc-p::before` | `#4285F4` |
| Progress bar fill | -- | `#4285F4` |
| Column header text | -- | `#4285F4` |
| Tag content | -- | "Pro" (abbreviated) |

### Sidebar Plane Badges

```javascript
// Marketing
background: #fce8e6; color: #EA4335;

// Product
background: #e8f0fe; color: #4285F4;
```

---

## 13. Category Tag System

### Category Colors

| Category | Text Color | Background Color | CSS |
|---|---|---|---|
| UI/UX | `#9334E9` | `#F3E8FF` | Purple |
| Creative Ads | `#EC4899` | `#FCE7F3` | Pink |
| R&D | `#3B82F6` | `#DBEAFE` | Blue |
| Content | `#22C55E` | `#DCFCE7` | Green |
| YouTube | `#EF4444` | `#FEE2E2` | Red |
| Business | `#EAB308` | `#FEF9C3` | Yellow |
| Legal | `#6B7280` | `#F3F4F6` | Grey |
| Infrastructure | `#F97316` | `#FFEDD5` | Orange |

### Category Tag Styling

```css
.cat-tag {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 8px;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: .2px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  /* color and background set inline */
}
```

### Usage Context

Category tags appear only on Phase 0 Board cards. Each task can have multiple categories. Tags are displayed as inline elements with small spacing between them.

---

## 14. Icon System

The dashboard uses inline SVGs and HTML entities instead of an icon library. All icons are minimal line-art style.

### SVG Icons

**External link arrow (Notion button):**
```html
<svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="#5f6368" stroke-width="2">
  <path d="M6 2h8v8M14 2L6 10"/>
</svg>
```
Sizes: 12x12 (standard), 10x10 (compact on P0/done cards), 16x16 (sidebar footer).

**Close X (sidebar):**
```html
<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="#5f6368" stroke-width="2">
  <path d="M4 4l8 8M12 4l-8 8"/>
</svg>
```

**Chat bubble (FAB):**
```html
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2">
  <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
</svg>
```

### HTML Entities

| Entity | Display | Usage |
|---|---|---|
| `&#10003;` | Checkmark | Done status, done items |
| `&#9679;` | Filled circle | Status dot (In Progress, Blocked) |
| `&#9675;` | Open circle | Not integrated indicator |
| `&#9888;` | Warning triangle | Overdue items in team view |
| `&#128293;` | Fire emoji | Ahead of schedule items |
| `&#128279;` | Link emoji | Links panel header |
| `&middot;` | Middle dot | Separator in subtitles, meta text |
| `&#8599;` | North-east arrow | External link indicator |
| `&#9650;` | Up triangle | Links panel expanded |
| `&#9660;` | Down triangle | Links panel collapsed |
| `&mdash;` / `—` | Em dash | Empty day column placeholder |

---

## Appendix A: Complete CSS Variable Reference

The dashboard does not use CSS custom properties (variables). All values are hardcoded in the stylesheet. Below is a reference of all distinct color values used:

### Backgrounds

| Hex | Usage |
|---|---|
| `#eef0f4` | Page body |
| `#fff` / `#ffffff` | Group panels, cards, sidebar, chat window |
| `#f8f9fa` | Card backgrounds, column backgrounds |
| `#f1f3f4` | Hover backgrounds, close button, P0 owner badge |
| `#e8f0fe` | Blue metric, today card, user bubble, product tag |
| `#e6f4ea` | Green metric, done gradient start, success toast |
| `#fef7e0` | Yellow metric |
| `#fce8e6` | Red metric, alert, overdue card, marketing tag, error toast |
| `#e8eaed` | Dark metric, owner badge, level badge, count badge |
| `#e0e3e7` | Progress track, column borders |
| `#fef2f1` | Marketing card background |
| `#eef3fc` | Product card background |
| `#d4edda` | Done gradient end |
| `#4285F4` | Chat header, FAB, active filter, active notion btn |
| `#202124` | Notion open button |

### Text Colors

| Hex | Usage |
|---|---|
| `#202124` | Primary text, headings |
| `#3c4043` | Secondary text, dark metric text |
| `#5f6368` | Muted text, subtitle |
| `#80868b` | Tertiary text, labels |
| `#9aa0a6` | Footer, timestamps |
| `#c5221f` | Red metric text, alert text, marketing tag text |
| `#1967d2` | Blue metric text, product tag text, user bubble text |
| `#137333` | Green metric text, done card heading, success toast text |
| `#e37400` | Yellow metric text, CORE badge text |

### Borders

| Hex | Usage |
|---|---|
| `#e8eaed` | Default card border, sidebar dividers |
| `#dadce0` | Hover border, filter border, input border |
| `#c5c9cf` | Active hover border |
| `#e0e3e7` | Column header border, P0 card border |
| `#f5c6c2` | Marketing border, alert border |
| `#c6dafc` | Product border |
| `#34A85340` | Done item border (25% opacity green) |
| `#EA433560` | Overdue card border (38% opacity red) |
| `#FBBC04` | CORE tool border |
| `#4285F4` | Today P0 column, active filter, drop highlight |

---

## Appendix B: Z-Index Stack

| Z-Index | Element |
|---|---|
| 9999 | Drag badge (floating) |
| 9999 | Toast notifications |
| 1000 | Notion sidebar |
| 900 | Chat FAB |
| 900 | Chat window |
| 2 | Notion toggle button (`.n-btn`) |

---

## Appendix C: Shadow Reference

| Element | Shadow |
|---|---|
| Group panel | `0 1px 4px rgba(0, 0, 0, 0.06)` |
| Card hover | `0 2px 8px rgba(0, 0, 0, 0.06)` |
| Goal card hover | `0 4px 16px rgba(0, 0, 0, 0.08)` |
| P0 card hover | `0 2px 8px rgba(0, 0, 0, 0.1)` |
| Tool card hover | `0 2px 8px rgba(0, 0, 0, 0.08)` |
| Done item hover | `0 2px 8px rgba(52, 168, 83, 0.15)` |
| Sidebar | `-4px 0 24px rgba(0, 0, 0, 0.1)` |
| Chat FAB | `0 4px 16px rgba(66, 133, 244, 0.4)` |
| Chat FAB hover | `0 6px 24px rgba(66, 133, 244, 0.5)` |
| Chat window | `0 8px 32px rgba(0, 0, 0, 0.15)` |
| Drag badge | `0 4px 12px rgba(0, 0, 0, 0.2)` |
| Toast | `0 4px 16px rgba(0, 0, 0, 0.15)` |
| Drop zone active | `inset 0 0 0 2px #4285F4` |
| Done card drop active | `inset 0 0 0 2px #2E7D32` |

---

## Appendix D: Border Radius Reference

| Element | Radius |
|---|---|
| Group panel | `16px` (12px at 640px) |
| Done card | `16px` |
| Chat window | `16px` |
| Links panel | `16px` |
| Goal card | `14px` |
| Tag | `12px` |
| Project column | `12px` |
| Task column | `12px` |
| Team card | `12px` |
| Phase 0 column | `12px` |
| Chat message bubble | `12px` (one corner: `4px`) |
| Done item | `10px` |
| Metric block | `10px` |
| Alert | `10px` |
| Project card | `10px` |
| Chat input | `10px` |
| Chat send button | `10px` |
| Notion open button | `10px` |
| Tool card | `10px` |
| Toast | `10px` |
| Phase 0 card | `8px` |
| Task card | `8px` |
| Chat user select | `8px` |
| Drag badge | `8px` |
| Category tag | `8px` |
| Column count badge | `8px-10px` |
| Link item | `8px` |
| Tool strip badge | `8px` |
| Close button | `8px` |
| P0 TODAY badge | `8px` |
| Owner badge | `6px` |
| Notion toggle button | `6px` |
| Sidebar children item | `6px` |
| Connection tag | `6px` |
| CORE badge | `6px` |
| P0 owner badge | `6px` |
| Chat FAB | `50%` (circle) |
| Section badge | `20px` (pill) |
| Filter button | `20px` (pill) |
| Progress bar track | `3px` |
| Progress bar fill | `3px` |
| Sidebar progress track | `4px` |
| Sidebar progress fill | `4px` |
| Drop ghost | `2px` |
