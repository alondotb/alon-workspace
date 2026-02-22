# 07 — Parent Dashboard

> **Screens:** 5 | **User:** Parent
> **Related tasks:** D12, R12, P9, P14

---

## 1. Parent Dashboard Home

**Task IDs:** D12, R12, P9 | **Route:** `/parent`

**Purpose:** The parent's main screen. See child's progress at a glance, manage subscription, add children.

### Layout

```
┌──────────────────────────────────────┐
│  Nav: VRT Logo   [ילד ▼]   [⚙️]   │
├──────────────────────────────────────┤
│                                       │
│  ┌─ Subscription Status ─────────┐   │
│  │  תוכנית: פרימיום חודשי  ✅ פעיל │   │
│  │  חידוש: 15/03/2026              │   │
│  │  [  נהלו מנוי  ]               │   │
│  └────────────────────────────────┘   │
│                                       │
│  ┌─ Child Card ──────────────────┐   │
│  │                                │   │
│  │  [Avatar]  נועה                │   │
│  │            רמה 12: Bug Squasher│   │
│  │            📘 שיעור 7/28        │   │
│  │            ⏱️ 3.5 שעות השבוע    │   │
│  │                                │   │
│  │  Quick Stats:                  │   │
│  │  ┌─────┐ ┌─────┐ ┌──────┐    │   │
│  │  │  7  │ │ 42  │ │  3   │    │   │
│  │  │שיעו-│ │שאלות│ │הישגים│    │   │
│  │  │ רים │ │     │ │חדשים │    │   │
│  │  └─────┘ └─────┘ └──────┘    │   │
│  │                                │   │
│  │  🏆 הישג אחרון: "פותר על 10"  │   │
│  │                                │   │
│  │  [  ראו דוח מלא →  ]          │   │
│  └────────────────────────────────┘   │
│                                       │
│  [  + הוסיפו ילד/ה  ]                │
│                                       │
└──────────────────────────────────────┘
```

### Subscription Status Bar States

| State | Visual |
|-------|--------|
| Active | Green badge "✅ פעיל", plan name, renewal date |
| Trial | Blue badge "⏳ ניסיון", "X ימים נותרו", upgrade CTA |
| Past Due | Red badge "⚠️ תשלום נכשל", "Update payment" CTA |
| Cancelled | Grey badge "מבוטל", "Access until DD/MM", resubscribe CTA |

### Child Card Components

- Avatar + name + level/title
- Current lesson progress (X/28)
- Time spent this week
- Quick stats grid: lessons completed, questions solved, new achievements
- Latest achievement
- "View full report" link

### Multiple Children

- If parent has 2+ children: child selector dropdown in nav, or multiple child cards stacked
- "Add child" button always visible

### Edge Cases

- No children added yet → show "Add your first child" prominent CTA, skip stats
- Child hasn't started learning → "נועה עוד לא התחילה — הזמינו אותה להתחבר!" with login code reminder
- Trial expired, no subscription → red banner: "תקופת הניסיון הסתיימה" + subscribe CTA

---

## 2. Child Progress Detail

**Task IDs:** D12, R12 | **Route:** `/parent/child/:id/progress`

**Purpose:** Deep dive into a child's learning data.

### Layout

```
┌──────────────────────────────────────┐
│  "ההתקדמות של נועה"   ← חזרה         │
├──────────────────────────────────────┤
│                                       │
│  ── סיכום כללי ──                    │
│  📘 שיעורים: 7/28                     │
│  ✅ שאלות: 42 נפתרו (87% נכון)       │
│  ⏱️ זמן כולל: 12.5 שעות              │
│  ⭐ רמה: 12                           │
│  🏅 הישגים: 12/40                     │
│                                       │
│  ── שיעורים שהושלמו ──               │
│  ┌────────────────────────────────┐   │
│  │  [Bar chart: lessons over time] │   │
│  │  Jan  Feb  (weekly bars)        │   │
│  └────────────────────────────────┘   │
│                                       │
│  ── דיוק בשאלות ──                   │
│  ┌────────────────────────────────┐   │
│  │  [Pie/donut: correct/incorrect] │   │
│  │  87% נכון | 13% שגוי           │   │
│  └────────────────────────────────┘   │
│                                       │
│  ── זמן למידה יומי ──               │
│  ┌────────────────────────────────┐   │
│  │  [Line chart: minutes per day]  │   │
│  │  Mon Tue Wed Thu Fri Sat Sun    │   │
│  └────────────────────────────────┘   │
│                                       │
│  ── הישגים אחרונים ──               │
│  🏅 First Answer — 01/15            │
│  🏅 10 Questions — 01/20            │
│  🏅 Streak of 5 — 02/01            │
│                                       │
│  ── פרויקטים ──                      │
│  ✅ מחשבון טרמינל                     │
│  ○ משחק ניחוש (לא התחיל)             │
│                                       │
└──────────────────────────────────────┘
```

### Charts

- Simple, clean charts (no complex interactivity needed)
- Bar chart: weekly lesson completion (last 8 weeks)
- Pie/donut: question accuracy (correct vs incorrect)
- Line chart: daily learning time (last 7 days)
- All charts: Hebrew labels, RTL axis where applicable

### Edge Cases

- Child has no data → "נועה עוד לא התחילה ללמוד" with encouragement
- Very little data (1-2 days) → show data points without trend lines
- Charts on mobile → full width, stacked vertically

---

## 3. Add Child Form

**Task IDs:** R2, P8 | **Route:** `/parent/add-child`

Same as `01-auth-onboarding.md`, Screen 8. Accessible from parent dashboard.

---

## 4. Parent Account Settings

**Task IDs:** R12 | **Route:** `/parent/settings`

Same as `01-auth-onboarding.md`, Screen 11. Includes:
- Email management
- Password change
- Daily time limit slider
- Notification preferences
- Account deletion

---

## 5. Daily Time Limit — Child View

**Task IDs:** R12, P9 | **Appears as:** Overlay on all child screens

**Purpose:** When the parent's daily time limit is reached, the child sees a friendly "time's up" screen.

### Layout

```
┌──────────────────────────────────────┐
│                                       │
│           ⏰ !הזמן נגמר להיום        │
│                                       │
│     [Character illustration —         │
│      avatar waving goodbye]           │
│                                       │
│     "עשית עבודה מדהימה היום!          │
│      נתראה מחר לעוד הרפתקאות 🚀"     │
│                                       │
│     היום למדת:                         │
│     📘 2 שיעורים  ✅ 8 שאלות          │
│                                       │
│     [  👋 להתראות  ]                  │
│                                       │
└──────────────────────────────────────┘
```

### Behavior

- Blocks all learning content (lessons, questions, projects, Bug Hunt)
- Profile and settings still accessible
- Clicking "Goodbye" → redirects to login page (logged out) or simple "see you tomorrow" static screen
- Resets at midnight (local time)
- 5-minute warning toast before time runs out: "!נשארו 5 דקות"

### Edge Cases

- Child is mid-question when time runs out → allow finishing current question, then show overlay
- Time limit changed by parent mid-session → applies immediately (grace: finish current activity)
- No time limit set → this screen never appears
