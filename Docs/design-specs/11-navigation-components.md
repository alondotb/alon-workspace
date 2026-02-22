# 11 — Navigation & Shared Components

> **Components:** ~17 | **Used across:** All screens
> **Related tasks:** D4, D8, D9, D20

---

## 1. Top Nav Bar — Child View

**Task IDs:** D4, D9 | **Appears on:** All child screens

### Layout (Desktop)

```
┌──────────────────────────────────────────────────────────┐
│  [VRT Logo]   📘 שיעור 7   │   🔥5  🪙150  ⭐████░ Lv7  [👤] │
└──────────────────────────────────────────────────────────┘
```

- **Left (RTL: right):** VRT logo → home/quest map
- **Center:** Current lesson indicator (optional, only on lesson pages)
- **Right (RTL: left):** Streak (🔥 + days), coins (🪙 + balance), XP bar + level, avatar portrait → profile

### Mobile

- Hamburger menu (☰) replaces inline links
- Essential items stay visible: logo, coins, avatar
- Streak, XP bar move into hamburger menu

### States

| Component | States |
|-----------|--------|
| Coin balance | Updates on earn (bounce animation) |
| XP bar | Fills on XP gain (smooth animation), resets on level-up |
| Level badge | Number + brief title tooltip on hover |
| Streak | Active (🔥 orange), broken/0 (grey or hidden) |
| Avatar portrait | Click → dropdown: profile, settings, logout |

---

## 2. Sidebar / Nav Drawer — Child View

**Task IDs:** D4 | **Appears on:** All child screens (mobile: drawer, desktop: optional sidebar)

### Links

```
┌──────────────────┐
│  [Avatar + Name]  │
│  רמה 7            │
├──────────────────┤
│  📘 שיעורים       │  ← Quest Map
│  🏆 הישגים        │  ← Achievements
│  👤 פרופיל        │  ← Profile
│  👥 חברים         │  ← Friends
│  📊 טבלת מובילים  │  ← Leaderboard
│  🐛 ציד באגים     │  ← Bug Hunt
│  🛍️ חנות          │  ← Avatar Shop
├──────────────────┤
│  ⚙️ הגדרות       │  ← Settings
│  🚪 התנתקו       │  ← Logout
└──────────────────┘
```

### Mobile Behavior

- Slide-in from right (RTL)
- Background overlay (click to close)
- Swipe right to close

### Active State

- Current page highlighted (background color + bold text)

---

## 3. Top Nav Bar — Parent View

**Task IDs:** D4 | **Appears on:** All parent screens

### Layout

```
┌──────────────────────────────────────────────┐
│  [VRT Logo]      [ילד: נועה ▼]   [⚙️]  [🚪] │
└──────────────────────────────────────────────┘
```

- Logo → parent dashboard
- Child selector dropdown (if multiple children)
- Settings gear icon → `/parent/settings`
- Logout icon

---

## 4. Public Nav Bar — Visitor View

**Appears on:** Landing, pricing, FAQ, legal pages

### Layout

```
┌──────────────────────────────────────────────────┐
│  [VRT Logo]   מחירים  שאלות   │  [התחברו] [הירשמו] │
└──────────────────────────────────────────────────┘
```

- Logo → landing page
- Links: pricing, FAQ
- Auth buttons: login (outlined), signup (filled/primary)

---

## 5. Loading Spinner

**Used during:** Code execution, API calls, page loads

### Variants

| Variant | Context | Visual |
|---------|---------|--------|
| Full page | Initial page load | Centered spinner + VRT logo, light background |
| Inline | Button loading state | Small spinner replaces button text |
| Code execution | Run button pressed | Spinner in output panel, "...מריץ" text |

- Keep it simple: CSS spinner (no heavy assets)
- Branded color (primary accent)

---

## 6. Toast Notifications

**Appears:** Bottom-right (RTL: bottom-left), stacks vertically

### Types

| Type | Color | Icon | Example |
|------|-------|------|---------|
| Success | Green | ✅ | "!השאלה נשמרה" |
| Error | Red | ❌ | "שגיאה — נסו שוב" |
| Info | Blue | ℹ️ | "עדכון חדש זמין" |
| Warning | Amber | ⚠️ | "!נשארו 5 דקות" (time limit) |

### Behavior

- Auto-dismiss: 4 seconds (success/info), 6 seconds (error/warning)
- Dismiss on click/swipe
- Max 3 visible at once (oldest dismissed)
- Slide-in animation from bottom

---

## 7. Modal / Confirmation Dialog

**Used for:** Purchases, deletions, quit game, important actions

### Layout

```
┌──────────────────────────────────┐
│  [Title]                          │
│                                   │
│  [Message / question text]        │
│                                   │
│  [Secondary CTA]   [Primary CTA] │
└──────────────────────────────────┘
```

### Components

- Backdrop: semi-transparent dark overlay, click to dismiss (optional)
- Card: white, rounded corners, centered
- Title: bold, 1 line
- Message: 1-3 lines
- Buttons: secondary (outlined, left in RTL) + primary (filled, right in RTL)
- Close X in top-left corner (RTL: top-right)

### Examples

| Context | Title | Message | Secondary | Primary |
|---------|-------|---------|-----------|---------|
| Buy item | "?לקנות [item]" | "עלות: 50 🪙" | "לא" | "!כן, קנו" |
| Quit game | "?לצאת מהמשחק" | "ההתקדמות לא תישמר" | "להמשיך" | "כן, לצאת" |
| Delete account | "?למחוק את החשבון" | "הפעולה בלתי הפיכה" | "ביטול" | "מחקו" (red) |

---

## 8. Difficulty Tier Badge

**Appears on:** Every question, Bug Hunt bugs

### Variants

| Tier | Color | Label |
|------|-------|-------|
| Easy | Green (#22C55E) | קל |
| Medium | Yellow (#EAB308) | בינוני |
| Hard | Orange (#F97316) | קשה |
| Challenge | Red (#EF4444) | אתגר |

### Design

- Small pill/chip: colored background, white text
- Positioned: top-right of question card
- Size: ~24px height, rounded

---

## 9. Level Badge

**Appears on:** Nav bar, profile, leaderboard, parent dashboard

### Design

- Circular or shield shape
- Level number (large, bold, centered)
- Title below or on hover tooltip
- Colors: grey (1-5), blue (6-10), purple (11-15), gold (16-20), diamond (21-30)

### Level Titles (Example)

| Levels | Title |
|--------|-------|
| 1-3 | מתחיל (Beginner) |
| 4-6 | חוקר (Explorer) |
| 7-9 | לומד (Learner) |
| 10-12 | Bug Squasher |
| 13-15 | קודר (Coder) |
| 16-18 | מפתח (Developer) |
| 19-21 | האקר (Hacker) |
| 22-25 | מאסטר (Master) |
| 26-30 | אלוף (Champion) |

---

## 10. XP Gain Animation

**Trigger:** Correct answer, achievement, project completion

### Spec

- "+20 ⭐" text appears at action point
- Gold color, bold
- Animation: scale up (0→1) → float up 50px → fade out
- Duration: 1.5 seconds
- Simultaneously: nav XP bar fills by earned amount (smooth, 0.5s)

---

## 11. Coin Gain Animation

**Trigger:** Same as XP gain

### Spec

- "+10 🪙" text, amber color
- Same float-up animation as XP
- Simultaneously: nav coin balance updates with bounce (scale 1 → 1.2 → 1)

---

## 12. Confetti Animation

**Trigger:** First-try correct answer, achievement unlock, level-up, project complete

### Spec

- Fullscreen particle burst from center
- Multi-colored (brand palette)
- Duration: 2-3 seconds
- Does NOT block interaction (decorative z-index)
- CSS or Lottie implementation
- Respect `prefers-reduced-motion` → disable

---

## 13. Streak Fire Animation

**Trigger:** Daily login, streak milestones (5, 10, 15...)

### Spec

- Flame icon in nav: brief enlarge + flicker (0.5s)
- At milestones: "!🔥 רצף של X" popup below flame, auto-dismiss 3s
- Streak broken: flame turns grey, shake animation (0.3s)

---

## 14. Empty States

**Appear when:** Lists/grids have no content yet

### Templates

| Context | Illustration | Message | CTA |
|---------|-------------|---------|-----|
| No achievements | Character with empty trophy case | "עוד לא השגתם הישגים — המשיכו ללמוד!" | "← לשיעורים" |
| No friends | Character waving | "עוד אין לכם חברים" | "חפשו בטבלת מובילים →" |
| No lessons started | Character pointing at quest map | "!המסע מתחיל כאן" | "← לשיעור הראשון" |
| Empty leaderboard (friends) | Characters together | "הוסיפו חברים כדי להתחרות!" | "→ הוסיפו חברים" |

### Design

- Character illustration (from avatar set — D2)
- Centered on page/section
- Message: friendly, encouraging, never shaming
- CTA button: links to relevant action

---

## 15. Error Pages

### 404 — Not Found

```
┌──────────────────────────────────────┐
│                                       │
│  [Character looking confused]         │
│                                       │
│  "404 — העמוד לא נמצא"               │
│  "נראה שהלכתם לאיבוד!"               │
│                                       │
│  [  ← חזרה לדף הבית  ]              │
└──────────────────────────────────────┘
```

### 500 — Server Error

```
┌──────────────────────────────────────┐
│                                       │
│  [Character fixing a broken machine]  │
│                                       │
│  "משהו השתבש אצלנו"                  │
│  "אנחנו עובדים על זה! נסו שוב       │
│   בעוד כמה דקות."                    │
│                                       │
│  📧 support@vrt.co.il                │
│                                       │
│  [  ← חזרה לדף הבית  ]              │
└──────────────────────────────────────┘
```

---

## 16. "Time's Up" Screen

See `07-parent-dashboard.md`, Screen 5. Shared component triggered by daily time limit.

---

## 17. Code Editor Shared Config

**Task IDs:** D6

All code editors across the platform share these settings:

| Setting | Value |
|---------|-------|
| Editor | Monaco Editor |
| Theme | Light, kid-friendly (custom — D6) |
| Language | Python |
| Font | Fira Code or JetBrains Mono, 14px |
| Line numbers | Yes |
| Minimap | No (too complex for kids) |
| Word wrap | On |
| Tab size | 4 spaces |
| Auto-indent | Yes |
| Direction | Always LTR (code is never RTL) |
| Run shortcut | Cmd/Ctrl + Enter |
| Reset behavior | Confirmation if code modified, restore to original |
| Output panel | Below editor, dark background, monospace font |
| Error messages | Python errors shown + kid-friendly Hebrew explanation below |
| Mobile | Full-width, toolbar with common Python symbols above keyboard |
