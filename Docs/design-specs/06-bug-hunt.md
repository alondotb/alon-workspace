# 06 — Bug Hunt Mini-Game

> **Screens:** 4 | **User:** Child
> **Related tasks:** D14, R14, P7

---

## 1. Mode Selection

**Task IDs:** D14, R14 | **Route:** `/bughunt`

**Purpose:** Choose between 3 Bug Hunt game modes.

### Layout

```
┌──────────────────────────────────────┐
│  "🐛 ציד באגים"                       │
├──────────────────────────────────────┤
│                                       │
│  ┌──────────────────────────────┐    │
│  │  ⚡ משחק מהיר                 │    │
│  │  5 באגים. תקנו כמה שיותר     │    │
│  │  מהר!                         │    │
│  │  שיא: 1:42                    │    │
│  │  [  !שחקו  ]                  │    │
│  └──────────────────────────────┘    │
│                                       │
│  ┌──────────────────────────────┐    │
│  │  ♾️ אינסופי                    │    │
│  │  באגים לא נגמרים. כמה תשרדו? │    │
│  │  שיא: 18 באגים                │    │
│  │  [  !שחקו  ]                  │    │
│  └──────────────────────────────┘    │
│                                       │
│  ┌──────────────────────────────┐    │
│  │  📅 אתגר יומי                 │    │
│  │  באג אחד. כל היום. מי הכי    │    │
│  │  מהיר?                        │    │
│  │  ✅ הושלם היום (or: "!שחקו") │    │
│  │  [  שחקו / ראו תוצאות  ]     │    │
│  └──────────────────────────────┘    │
│                                       │
│  [ 🏆 טבלת מובילים ]                 │
│                                       │
└──────────────────────────────────────┘
```

### Mode Card States

| Mode | Not Played | Has Personal Best | Daily Completed |
|------|-----------|-------------------|-----------------|
| Quick Play | "!שחקו" | Shows best time | N/A |
| Endless | "!שחקו" | Shows most bugs fixed | N/A |
| Daily | "!שחקו" | N/A | "✅ הושלם — ראו תוצאות" |

---

## 2. Quick Play Mode

**Task IDs:** D14, R14, P7 | **Route:** `/bughunt/quick`

**Purpose:** Fix 5 bugs as fast as possible. Timed, competitive.

### Layout

```
┌──────────────────────────────────────┐
│  ⚡ מהיר   ⏱️ 0:23   באג 3/5         │
├──────────────────────────────────────┤
│                                       │
│  ┌─ Buggy Code (read-only) ──────┐   │
│  │  numbers = [1, 2, 3, 4, 5]    │   │
│  │  total = 0                     │   │
│  │  for i in range(len(numbers)): │   │
│  │      total += numbers[i + 1]   │   │
│  │  print(total)                  │   │
│  └────────────────────────────────┘   │
│                                       │
│  ┌─ Your Fix (editable) ─────────┐   │
│  │  (same code, editable)         │   │
│  └────────────────────────────────┘   │
│                                       │
│  ┌─ Output Panel ────────────────┐   │
│  │  (shows after submit)          │   │
│  └────────────────────────────────┘   │
│                                       │
│  [        🔍 בדוק תיקון        ]     │
└──────────────────────────────────────┘
```

### Header Components

| Component | Details |
|-----------|---------|
| Mode indicator | "⚡ מהיר" on the right (RTL) |
| Timer | Counts up from 0:00, center. Green while under personal best, yellow near it, red past it |
| Bug counter | "באג X/5" on the left |

### Game Flow

1. **Countdown:** "3... 2... 1... !קדימה" (3 seconds)
2. **Bug loads:** Buggy code shown + editable copy below
3. **Kid edits & submits:** Click "בדוק תיקון" or Cmd+Enter
4. **Correct:** Green output panel, "+XP/coins" popup, 1s pause → transition → next bug
5. **Incorrect:** Red output panel, "!נסו שוב", unlimited retries, timer keeps running
6. **After 5 bugs:** Game over screen

### Submit Button States

| State | Visual |
|-------|--------|
| Default | Large green: "🔍 בדוק תיקון" |
| Hover | Brighter green, shadow |
| Checking | Spinner, "...בודק", disabled |
| Disabled | Grey (editor empty) |

### Output Panel States

| State | Visual |
|-------|--------|
| Hidden | Before first submit |
| Correct | Green border, "✅ Output correct", expected output shown |
| Incorrect | Red border, "❌ Still buggy", actual vs expected output |
| Runtime error | Red border, kid-friendly Hebrew error explanation |
| Timeout | Yellow border, "⏱️ הקוד רץ יותר מדי זמן" |

### Game Over Screen

```
┌──────────────────────────────────────┐
│           ⚡ !סיימתם                  │
│                                       │
│     ⏱️ זמן: 1:38                      │
│     🐛 באגים שתוקנו: 5/5              │
│     ⭐ XP: +100                       │
│     🪙 מטבעות: +50                    │
│                                       │
│     שיא: 1:42  →  "!שיא חדש — 1:38"  │
│                                       │
│  [ 🔄 שחקו שוב ]  [ 🏠 חזרה ]        │
└──────────────────────────────────────┘
```

### Edge Cases

- Kid submits unchanged code → "הקוד עדיין לא תוקן — חפשו את הבאג!"
- Kid deletes everything → submit disabled, "הקוד ריק"
- Network failure during submit → "שגיאת תקשורת — נסו שוב" (timer pauses)
- Code execution timeout (>5s) → yellow warning, retry
- Browser close mid-game → no save, fresh start on return

---

## 3. Endless Mode

**Task IDs:** D14, R14 | **Route:** `/bughunt/endless`

**Purpose:** Bugs keep coming until the kid loses all 3 lives. Difficulty escalates.

### Header Differences from Quick Play

```
♾️ אינסופי   ⏱️ 3:42   באגים: 12   🔥 רצף: 5   ❤️❤️❤️
```

- Difficulty indicator: `רמת קושי: [████████░░] בינוני`
- Lives: 3 hearts (❤️). Lose one per wrong answer.
- Streak counter: consecutive correct fixes. Bonus XP at milestones (5, 10, 15...).
- Bug counter: total fixed (counts up, no limit).

### Difficulty Scaling

| Bugs Fixed | Difficulty | Bug Types |
|-----------|-----------|-----------|
| 1-5 | קל (Easy, green) | Simple syntax: missing colon, wrong indent |
| 6-12 | בינוני (Medium, yellow) | Logic errors, wrong operators, off-by-one |
| 13+ | קשה (Hard, red) | Multi-line issues, scope errors, complex logic |

### Life System

| Lives | Visual |
|-------|--------|
| 3 (full) | ❤️❤️❤️ |
| Life lost | Heart cracks → grey. Screen flashes red (100ms) |
| 1 remaining | Heart pulses. "!זהירות — חיים אחרונים" |
| 0 (game over) | All grey. Game over triggers. |

### Game Over

Same layout as Quick Play game over, with:
- Bugs fixed (total), max streak, elapsed time, final score
- Score formula: (bugs × 10) + (streak × 5) + difficulty bonus
- "!שיא חדש" if applicable

### Edge Cases

- Streak broken (life lost) → streak resets to 0 with shake animation
- 50+ bugs fixed → "!אלוף" special message, offer to end gracefully
- All 3 lives lost on first bug → "!לא נורא — נסו שוב" encouraging message

---

## 4. Daily Challenge

**Task IDs:** D14, R14 | **Route:** `/bughunt/daily`

**Purpose:** One shared bug per day. Everyone solves the same one. Fastest time wins.

### Key Differences from Quick Play

- **One bug only** — no bug counter
- **No hints** — keeps it fair
- **Timer counts up** — fastest time = best score
- **One attempt per day** — once solved, can't replay
- **Leaderboard overlay** after solving

### Header

```
📅 אתגר יומי   ⏱️ 0:23   17 בפברואר 2026
```

### Result Screen (after solving)

```
┌──────────────────────────────────────┐
│      📅 !סיימתם את האתגר היומי       │
│                                       │
│     ⏱️ הזמן שלכם: 0:42               │
│     🏆 דירוג: #14 מתוך 238           │
│     🪙 בונוס: +25                     │
│     ⭐ XP: +30                        │
│                                       │
│  ┌─ Leaderboard Preview ─────────┐   │
│  │  #1   נועה     0:18           │   │
│  │  #2   איתי     0:23           │   │
│  │  #3   מיכל     0:31           │   │
│  │  ...                           │   │
│  │  #14  ★ אתם ★  0:42           │   │
│  └────────────────────────────────┘   │
│                                       │
│  האתגר הבא בעוד: 14:32:07            │
│                                       │
│  [ 🏠 חזרה ]  [ 🏆 דירוג מלא ]       │
└──────────────────────────────────────┘
```

### States

| State | Visual |
|-------|--------|
| Top 3 finish | Medal animation (🥇🥈🥉), extra coins, "!נכנסתם לשלושת הראשונים" |
| First solver | "!ראשונים היום" special badge |
| Already completed today | Show cached results, "!כבר סיימתם", countdown to next |
| Challenge not ready (midnight) | "...האתגר היומי בהכנה" loading state |

### Edge Cases

- Quit mid-challenge → timer continues. Returning resumes (or counts as not completed — TBD)
- Network failure on submit → optimistic display, sync when connection returns
- Midnight rollover while on result screen → toast: "!אתגר חדש זמין"
- Ties → earlier submission wins (server uses millisecond precision)

### Hebrew RTL Notes (all Bug Hunt screens)

- Header: mode name on right, timer center, counters on left
- Code blocks: always LTR (code is LTR regardless of UI direction)
- UI labels, buttons, messages: all Hebrew RTL
- Output panel errors: Python errors in English, Hebrew explanation added below
- Timer/numbers: standard Arabic numerals, LTR display
