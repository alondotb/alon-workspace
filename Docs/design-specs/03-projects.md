# 03 — Projects

> **Screens:** 2 | **User:** Child
> **Related tasks:** D10, R18, P3

---

## 1. Project Page (Guided Steps)

**Task IDs:** D10, R18, P3 | **Route:** `/projects/:id`

**Purpose:** Multi-step guided projects where kids build something real (calculator, game, etc). Each step has instructions + code editor + tests.

### Layout

```
┌──────────────────────────────────────────────────┐
│  Nav: ← חזרה   "מחשבון טרמינל"   🪙 150  ⭐ Lv7 │
├──────────┬───────────────────────────────────────┤
│ Steps    │                                       │
│ Sidebar  │  שלב 3 מתוך 8: קלט מהמשתמש           │
│          │                                       │
│ ✅ שלב 1 │  "בשלב הזה תוסיפו קלט מהמשתמש.       │
│ ✅ שלב 2 │   השתמשו ב-input() כדי לקבל מספר      │
│ → שלב 3  │   מהמשתמש ולשמור אותו במשתנה."        │
│ ○ שלב 4  │                                       │
│ ○ שלב 5  │  ┌─ Code Editor ────────────────────┐ │
│ ○ שלב 6  │  │  # Starter code                  │ │
│ ○ שלב 7  │  │  num1 = input("Enter number: ")  │ │
│ ○ שלב 8  │  │  # Add your code below           │ │
│          │  └──────────────────────────────────┘ │
│          │                                       │
│          │  [ ▶ הריצו ]  [ ↺ אפסו ]              │
│          │                                       │
│          │  ┌─ Output Panel ───────────────────┐ │
│          │  │                                   │ │
│          │  └──────────────────────────────────┘ │
│          │                                       │
│          │  [ ← שלב קודם ]   [ שלב הבא → ]      │
├──────────┴───────────────────────────────────────┤
│  Progress: ████████░░░░░░░░ 3/8                  │
└──────────────────────────────────────────────────┘
```

### Components & States

| Component | States |
|-----------|--------|
| Step sidebar item | Completed (✅), current (→ highlighted), upcoming (○ dimmed) |
| Step instructions | Hebrew RTL text, can include images/diagrams |
| Code editor | Same Monaco setup as lessons — Run/Reset, starter code |
| Output panel | Hidden → output → error (kid-friendly) |
| Previous button | Disabled on step 1, enabled otherwise |
| Next button | Disabled until current step passes tests, enabled after |
| Progress bar | Linear, fills as steps complete |

### Final Step (Step 8 — Submission)

- "Submit" replaces "Next step"
- Runs all test cases against the complete project
- Test results display:

```
┌─ Test Results ───────────────────┐
│  ✅ מקבל קלט מהמשתמש             │
│  ✅ מבצע חישוב נכון               │
│  ✅ מדפיס תוצאה                   │
│  ❌ מטפל בשגיאות (חלוקה ב-0)     │
│                                   │
│  3/4 עברו — תקנו את הטסט שנכשל   │
│  ונסו שוב!                        │
└───────────────────────────────────┘
```

### States

| State | Visual |
|-------|--------|
| All tests pass | Celebration overlay → certificate |
| Some tests fail | Show which failed, hint about what to fix, retry |
| Runtime error | Kid-friendly error, retry |

### Edge Cases

- Kid skips steps (clicks future step in sidebar) → locked: "!השלימו את שלב X קודם"
- Kid returns to completed step → can re-run code but can't re-submit (read-only or re-editable for practice)
- Mobile: sidebar collapses to dropdown step selector at top
- Auto-save per step (code preserved between visits)

---

## 2. Project Completion Certificate

**Task IDs:** D10, R18 | **Route:** `/projects/:id/certificate`

**Purpose:** Celebrate project completion with a shareable certificate.

### Layout

```
┌──────────────────────────────────────┐
│                                       │
│  ┌─ Certificate Card ────────────┐   │
│  │                                │   │
│  │      🏆 תעודת הצטיינות        │   │
│  │                                │   │
│  │      Virtual Techies           │   │
│  │                                │   │
│  │      [שם הילד]                 │   │
│  │                                │   │
│  │      השלים/ה בהצלחה את הפרויקט │   │
│  │      "מחשבון טרמינל"           │   │
│  │                                │   │
│  │      תאריך: DD/MM/YYYY        │   │
│  │                                │   │
│  │      [VRT Logo]                │   │
│  │                                │   │
│  └────────────────────────────────┘   │
│                                       │
│  +50 ⭐  +30 🪙                       │
│                                       │
│  [ 📥 הורידו PDF ]  [ 🖨️ הדפיסו ]   │
│                                       │
│  [  ← חזרה לפרויקטים  ]              │
└──────────────────────────────────────┘
```

### Components

- Certificate: styled card with VRT branding, child's name, project name, date
- Download: generates PDF
- Print: browser print dialog
- XP/coin reward shown below certificate
- Confetti animation on load

### Edge Cases

- Certificate viewed again later → same layout, no additional rewards
- Child's name too long → truncate or reduce font size
- PDF generation fails → fallback: "screenshot the certificate" suggestion
