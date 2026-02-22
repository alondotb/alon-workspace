# 05 — Social

> **Screens:** 5 | **User:** Child
> **Related tasks:** D11, R15, R16, R17

---

## 1. Other User's Profile + Friend Request

**Task IDs:** R15, R16, D11 | **Route:** `/profile/:username`

**Purpose:** View another kid's profile and send friend request.

### Layout

Same as own profile (04-gamification.md, Screen 2) with these additions:

- **No edit buttons** (not your profile)
- **Friend action button** replaces edit controls:

| State | Button |
|-------|--------|
| Not friends | "הוסיפו כחבר/ה +" — blue primary button |
| Request sent | "בקשה נשלחה ⏳" — grey, disabled |
| Already friends | "חברים ✅" — green badge, with "הסירו" option (subtle) |

### Interactions

- Click "Add friend" → sends request → button changes to "Request sent"
- Click "Remove friend" → confirmation: "?להסיר את [name] מרשימת החברים" [כן / לא]

---

## 2. Friend Request Management

**Task IDs:** R16, D11 | **Route:** `/friends/requests`

**Purpose:** View and manage incoming/outgoing friend requests.

### Layout

```
┌──────────────────────────────────────┐
│  "בקשות חברות"                        │
├──────────────────────────────────────┤
│  [ התקבלו (3) | נשלחו (1) ]          │
├──────────────────────────────────────┤
│                                       │
│  ┌────────────────────────────────┐   │
│  │ [Avatar] נועה  |  רמה 8       │   │
│  │         [ ✅ אשרו ] [ ❌ דחו ] │   │
│  └────────────────────────────────┘   │
│                                       │
│  ┌────────────────────────────────┐   │
│  │ [Avatar] איתי  |  רמה 12      │   │
│  │         [ ✅ אשרו ] [ ❌ דחו ] │   │
│  └────────────────────────────────┘   │
│                                       │
└──────────────────────────────────────┘
```

### Tab: Received

- Each entry: avatar, name, level, accept/decline buttons
- Accept → moves to friends list, toast: "!נועה נוספה לחברים שלכם"
- Decline → entry removed, no notification to requester

### Tab: Sent

- Each entry: avatar, name, level, "Cancel" button
- Cancel → "?לבטל את הבקשה" confirmation → request withdrawn

### Edge Cases

- No requests → "אין בקשות חדשות" empty state
- 50+ requests (unlikely but handle) → paginated or scrollable list

---

## 3. Friends List

**Task IDs:** R16, D11 | **Route:** `/friends`

**Purpose:** View all friends, navigate to their profiles.

### Layout

```
┌──────────────────────────────────────┐
│  "חברים (12)"                         │
├──────────────────────────────────────┤
│                                       │
│  ┌────────────────────────────────┐   │
│  │ [Avatar] נועה     רמה 8  🟢   │   │
│  │          [  צפו בפרופיל  ]    │   │
│  └────────────────────────────────┘   │
│                                       │
│  ┌────────────────────────────────┐   │
│  │ [Avatar] איתי     רמה 12 ⚫   │   │
│  │          [  צפו בפרופיל  ]    │   │
│  └────────────────────────────────┘   │
│                                       │
│  ... more friends ...                 │
│                                       │
└──────────────────────────────────────┘
```

### Components

| Component | Details |
|-----------|---------|
| Friend card | Avatar, name, level, online indicator (🟢/⚫) |
| "View profile" | Links to their profile page |
| Online status | Green dot = online now, grey = offline |

### Empty State

```
"עוד אין לכם חברים 😊"
"חפשו חברים בטבלת המובילים!"
[  → לטבלת המובילים  ]
```

---

## 4. Leaderboards (3 variants — shared layout)

**Task IDs:** R17, D11 | **Route:** `/leaderboard`

**Purpose:** Rankings that drive friendly competition. 3 tabs share one layout.

### Layout

```
┌──────────────────────────────────────┐
│  "טבלת מובילים"                       │
├──────────────────────────────────────┤
│  [ כללי | שבועי | חברים ]            │
├──────────────────────────────────────┤
│                                       │
│  #   שם          רמה      XP         │
│  ─────────────────────────────────── │
│  1   🥇 נועה      14     12,450      │
│  2   🥈 איתי      13     11,200      │
│  3   🥉 מיכל      12     10,800      │
│  4      דני       11      9,500      │
│  5      שרה       10      8,200      │
│  ...                                  │
│  ─────────────────────────────────── │
│  47  ★ אתם ★      7      2,340      │
│  ─────────────────────────────────── │
│                                       │
│  [Avatar] רמה 7 | #47 כללי           │
│                                       │
└──────────────────────────────────────┘
```

### Tabs

| Tab | Data | Reset |
|-----|------|-------|
| **Global (כללי)** | All users, total XP, all-time | Never |
| **Weekly (שבועי)** | All users, XP earned this week | Every Monday, shows "שבוע: DD/MM — DD/MM" |
| **Friends (חברים)** | Friends only, total XP | Never |

### Components

- Top 3: medal icons (🥇🥈🥉), slightly larger font
- Current user row: highlighted background (accent color), pinned at bottom if not in visible range, star markers
- Each row: rank, avatar (small), name, level, XP
- Tap any row → navigate to that user's profile

### Edge Cases

- Current user is #1 → extra celebration styling on their row
- Friends tab with 0 friends → "הוסיפו חברים כדי להתחרות!" + CTA
- Weekly tab on Monday (just reset) → "שבוע חדש התחיל! — הכל מתאפס" banner
- Thousands of users → show top 100 + "your rank: #X" pinned
- Tied XP → same rank number, ordered by who reached it first

---

## 5. Bug Hunt Leaderboard

**Task IDs:** R17, R14, D11 | **Route:** `/leaderboard/bughunt`

**Purpose:** Separate leaderboard for Bug Hunt mini-game.

### Layout

Same layout as main leaderboard, with different tabs:

```
[ כל הזמנים | אתגר יומי ]
```

### Tabs

| Tab | Data | Metric |
|-----|------|--------|
| **All-time (כל הזמנים)** | Total bugs fixed across all modes | Bugs fixed count |
| **Daily Challenge (אתגר יומי)** | Today's challenge solvers | Solve time (fastest first) |

### Daily Challenge Tab

- Shows today's date
- Metric: solve time (MM:SS format)
- Fastest solver gets "!ראשון היום" badge
- If user hasn't completed today → "שחקו באתגר היומי!" CTA at top

### Edge Cases

- No daily challenge yet today (midnight edge) → "האתגר היומי בהכנה..."
- User hasn't played Bug Hunt ever → show leaderboard normally, encourage play
