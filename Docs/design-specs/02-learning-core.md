# 02 — Learning Core

> **Screens:** 12 | **User:** Child
> **Related tasks:** D5, D6, D7, D15, R5, R6, R7, P3, P6

---

## 1. Quest Map / Campaign Dashboard — EXISTING DESIGN (2 screens)

**Task IDs:** D5, R5, P3 | **Route:** `/quests`

**Purpose:** The main hub. A visual campaign tree showing all 28 quests (lessons) as nodes. Kids see their progress and pick what to do next.

### Enhancement Checklist (for existing Figma)

- [ ] Linear world map with quest nodes (visually non-linear — loops, branches for aesthetics)
- [ ] **HUD (always visible):** Avatar portrait, level badge + title, animated XP bar, coin balance, streak counter
- [ ] **Quest node states:**

| State | Visual | Interaction |
|-------|--------|-------------|
| Locked | Grey/dim, lock icon | Tap → tooltip: "!השלימו את שיעור X כדי לפתוח" |
| Available | Glowing/pulsing border, bright color | Tap → quest briefing |
| In Progress | Arrow icon, progress ring showing % | Tap → resume lesson |
| Completed | Checkmark, star rating or full color | Tap → review lesson |
| Current (active) | Largest node, animated, distinct glow | Obvious next step |

- [ ] Progress bar at top: overall course progress (X/28 lessons)
- [ ] Scroll/pan behavior on the map
- [ ] Mobile: vertical scroll, nodes stack naturally
- [ ] First-time user: only quest 1 available, rest locked with visual path showing what's ahead
- [ ] Empty state (before any quest): arrow/animation pointing to quest 1

---

## 2. Quest Briefing

**Task IDs:** D5, R5 | **Route:** `/quests/:id/briefing`

**Purpose:** Short mission briefing before starting a lesson. Sets context.

### Layout

```
┌──────────────────────────────────────┐
│  Nav: ← חזרה למפה    🪙 150  ⭐ Lv7 │
├──────────────────────────────────────┤
│  Quest #7: לולאות While               │
│                                       │
│  "בשיעור הזה תלמדו לכתוב קוד שחוזר  │
│   על עצמו שוב ושוב — כל עוד תנאי     │
│   מסוים מתקיים."                      │
│                                       │
│  📋 מה תלמדו:                         │
│  • מה זה while loop                   │
│  • איך לבנות תנאי עצירה              │
│  • שימוש ב-break ו-continue          │
│                                       │
│  ⏱️ זמן משוער: ~20 דקות               │
│  📝 שאלות: 6 (5 נדרשות לפתיחת הבא)   │
│                                       │
│  [  🚀 !התחילו  ]                     │
└──────────────────────────────────────┘
```

### States

- Video exists (premium): auto-start video, auto-close when done → lesson content
- No video (basic): skip straight to lesson content on "Start" click
- Already completed: show "Review" button instead of "Start", show previous score

---

## 3. Coding Workspace / Lesson Viewer — EXISTING DESIGN

**Task IDs:** D5, D6, R5, R6, R19 | **Route:** `/quests/:id/learn`

**Purpose:** The core learning screen. Written content + interactive code blocks + video (premium).

### Enhancement Checklist

- [ ] **Video player (premium only):** Embedded at top, auto-start, play/pause/fullscreen, progress bar. Basic users see upgrade prompt or nothing.
- [ ] **Written content:** Hebrew RTL text, headings, paragraphs, images. Scrollable.
- [ ] **Interactive code blocks (5-8 per lesson):**

| Component | States |
|-----------|--------|
| Code editor (Monaco) | Pre-loaded with example code, editable, kid-friendly theme (D6) |
| Run button | Default (▶ הריצו), hover, loading (spinner, "...מריץ"), disabled during execution |
| Reset button | Default (↺ אפסו), hover, confirmation if code was modified |
| Output panel | Hidden (before first run), success (green border, output text), error (red border, kid-friendly error message), timeout ("הקוד רץ יותר מדי זמן — בדקו לולאות") |

- [ ] **Auto-save:** Every keystroke saved (debounced). No manual save button.
- [ ] **Logic-based hint system:** Yellow bubble appears after: 3+ failed runs, 2+ minutes stuck, repeated syntax errors. See hint spec in Screen 8.
- [ ] **Navigation:** Previous/Next lesson buttons. "Next" enabled when min questions met.
- [ ] **Questions tab/section:** Counter showing "5/6 שאלות נדרשות", links to question flow
- [ ] **Code execution errors:** Translated to kid-friendly Hebrew: "SyntaxError" → "שגיאת כתיבה — בדקו סוגריים ונקודותיים"
- [ ] **Mobile:** Code editor fills width, output below. Consider landscape prompt for coding.

---

## 4. Question: Code Write

**Task IDs:** D7, R7, P6 | **Route:** `/quests/:id/questions/:qid`

**Purpose:** Kid writes code from scratch to solve a prompt.

### Layout

```
┌──────────────────────────────────────┐
│  שאלה 3/6   [קשה 🟠]   🪙 150  ⭐ 7 │
├──────────────────────────────────────┤
│  כתבו פונקציה שמקבלת מספר ומחזירה    │
│  את הערך המוחלט שלו.                 │
│                                       │
│  ┌─ Code Editor ──────────────────┐  │
│  │  def absolute(num):             │  │
│  │      # כתבו כאן                 │  │
│  │                                 │  │
│  └─────────────────────────────────┘  │
│                                       │
│  [  📤 הגישו  ]                       │
│                                       │
│  [💡 רמז (5 🪙)]  [⏭️ חזרו מאוחר יותר]│
└──────────────────────────────────────┘
```

### Result States

| Result | Visual | Behavior |
|--------|--------|----------|
| Correct (1st try) | 🎉 Confetti, "!מדהים — בפעם הראשונה", +XP/coins popup | Explanation panel, "Next question" CTA |
| Correct (2nd+ try) | ✅ "!עבר — כל הכבוד על ההתמדה", +XP (reduced)/coins | Explanation panel, "Next question" CTA |
| Incorrect | ❌ "!לא בדיוק — נסו שוב", show expected vs actual output | Retry enabled, hint button highlighted |
| Timeout | ⏱️ "הקוד רץ יותר מדי זמן" | Retry enabled |
| Runtime error | 🐛 Kid-friendly error explanation in Hebrew | Retry enabled |

---

## 5. Question: Code Fix

**Task IDs:** D7, R7 | Same route pattern as above

**Purpose:** Kid finds and fixes a bug in pre-populated code.

### Layout

Same as Code Write, except:
- Prompt: "מצאו ותקנו את הבאג בקוד הבא:"
- Editor pre-filled with buggy code (editable)
- Diff highlighting optional (show changed lines after submit)

### Unique States

- Kid submits unchanged code → "הקוד עדיין לא תוקן — חפשו את הבאג!"
- Kid deletes everything → "הקוד ריק — תקנו את הבאג, לא תמחקו אותו"

---

## 6. Question: Multiple Choice

**Task IDs:** D7, R7

**Purpose:** Pick the correct answer from 4 options.

### Layout

```
┌──────────────────────────────────────┐
│  שאלה 2/6   [בינוני 🟡]              │
├──────────────────────────────────────┤
│  מה ידפיס הקוד הבא?                  │
│                                       │
│  ┌─ Code (read-only) ────────────┐   │
│  │  x = 5                         │   │
│  │  print(x * 2 + 1)             │   │
│  └────────────────────────────────┘   │
│                                       │
│  ○ 10                                 │
│  ○ 11                                 │
│  ○ 12                                 │
│  ○ 52+1                              │
│                                       │
│  [  📤 הגישו  ]                       │
└──────────────────────────────────────┘
```

### States

| Component | States |
|-----------|--------|
| Option buttons | Unselected, hover (highlight), selected (filled circle + border) |
| Submit | Disabled (no selection), enabled, loading |
| Correct option (after submit) | Green background |
| Incorrect option (selected, wrong) | Red background, correct one turns green |

---

## 7. Question: Output Predict

**Task IDs:** D7, R7

**Purpose:** Kid reads code and types what it will print.

### Layout

```
┌──────────────────────────────────────┐
│  שאלה 4/6   [קל 🟢]                  │
├──────────────────────────────────────┤
│  מה ידפיס הקוד הבא?                  │
│                                       │
│  ┌─ Code (read-only) ────────────┐   │
│  │  for i in range(3):            │   │
│  │      print(i)                  │   │
│  └────────────────────────────────┘   │
│                                       │
│  :התשובה שלכם                         │
│  [____________]                       │
│                                       │
│  [  📤 הגישו  ]                       │
└──────────────────────────────────────┘
```

### Notes

- Input field: LTR (output is code/numbers)
- Matching: trim whitespace, case-insensitive, accept "0\n1\n2" or "0 1 2" or "012"
- If multiple lines expected: show multi-line input or clarify "write each output on a new line"

---

## 8. Question: Fill in the Blank

**Task IDs:** D7, R7

**Purpose:** Complete missing code in a partially-written snippet.

### Layout

```
┌──────────────────────────────────────┐
│  שאלה 5/6   [בינוני 🟡]              │
├──────────────────────────────────────┤
│  השלימו את החלק החסר:                │
│                                       │
│  ┌─ Code with blank ─────────────┐   │
│  │  numbers = [1, 2, 3, 4, 5]    │   │
│  │  total = 0                     │   │
│  │  for n in _______:             │   │
│  │      total += n                │   │
│  └────────────────────────────────┘   │
│                                       │
│  [____________]                       │
│                                       │
│  [  📤 הגישו  ]                       │
└──────────────────────────────────────┘
```

### Notes

- Blank shown as `_______` in code (visually distinct, highlighted background)
- Input field below (or inline if technically feasible)
- Accept equivalent answers: `numbers` and `numbers[:]` both valid if they produce same result

---

## 9. Hint Tiers UI

**Task IDs:** D15, R7 | **Appears as:** Modal/drawer overlay on any question

**Purpose:** 3-tier progressive hint system. Each hint costs more coins and reveals more.

### Layout

```
┌──────────────────────────────────────┐
│  💡 רמזים                             │
├──────────────────────────────────────┤
│                                       │
│  רמז 1 — 5 🪙                        │
│  ┌────────────────────────────────┐   │
│  │ 🔒 [גלו רמז — 5 מטבעות]       │   │
│  └────────────────────────────────┘   │
│                                       │
│  רמז 2 — 15 🪙                       │
│  ┌────────────────────────────────┐   │
│  │ 🔒 (requires hint 1 first)     │   │
│  └────────────────────────────────┘   │
│                                       │
│  רמז 3 — 30 🪙                       │
│  ┌────────────────────────────────┐   │
│  │ 🔒 (requires hint 2 first)     │   │
│  └────────────────────────────────┘   │
│                                       │
│  יתרה: 150 🪙                         │
└──────────────────────────────────────┘
```

### States per Hint Tier

| State | Visual |
|-------|--------|
| Locked (can afford) | Lock icon, "גלו רמז — X מטבעות" button |
| Locked (can't afford) | Lock icon, greyed button, "אין מספיק מטבעות" |
| Locked (previous required) | Lock icon, dimmed, "גלו את רמז X קודם" |
| Purchased/Revealed | Hint text visible, no lock, checkmark |

### Hint Content Levels

1. **Hint 1 (5 coins):** Gentle nudge — "think about what range() does"
2. **Hint 2 (15 coins):** More specific — "the issue is on line 4, check the index"
3. **Hint 3 (30 coins):** Near-complete walkthrough — "change `i + 1` to `i`"

### Interactions

- Click "Reveal" → confirmation modal: "?להוציא X מטבעות על רמז" [כן / לא]
- Confirmed → coins deducted, hint text revealed with slide-down animation
- Close hints → return to question (hints stay revealed)

---

## 10. Explanation Display (After Correct Answer)

**Appears below question result**

### Layout

```
┌──────────────────────────────────────┐
│  📖 למה זה נכון:                     │
│                                       │
│  "הפונקציה range(3) מייצרת את         │
│   המספרים 0, 1, 2 — שלושה מספרים      │
│   מ-0 ועד 2 (לא כולל 3)."            │
│                                       │
│  ┌─ Related code example ─────────┐  │
│  │  >>> list(range(3))             │  │
│  │  [0, 1, 2]                      │  │
│  └─────────────────────────────────┘  │
└──────────────────────────────────────┘
```

- Always shown after correct answer (not optional)
- Collapsible if the kid wants to skip reading

---

## 11. Lesson Progress Counter

**Appears in lesson sidebar/header**

### Layout

`📝 5/6 שאלות הושלמו` with progress bar

### States

| Progress | Visual |
|----------|--------|
| 0% | Grey bar, "עוד לא ענית על שאלות" |
| Partial | Yellow fill, "X/Y שאלות הושלמו" |
| Threshold met | Green fill, "!השיעור הבא נפתח" celebration banner |
| 100% | Full green, gold star, "!כל השאלות הושלמו — מושלם" |

---

## 12. Lesson Unlocked Celebration

**Appears as overlay when threshold is met**

### Layout

```
┌──────────────────────────────────────┐
│  🎉 !כל הכבוד                        │
│                                       │
│  פתחתם את השיעור הבא:                 │
│                                       │
│  [Preview card of next lesson]        │
│  "שיעור 8: פונקציות"                  │
│                                       │
│  +30 ⭐  +20 🪙                       │
│                                       │
│  [  ← המשיכו לשיעור הבא  ]           │
│  [  🔄 חזרו לשאלות  ]                │
└──────────────────────────────────────┘
```

- Confetti animation
- XP/coin reward popup
- Auto-dismiss after 5s if no interaction
