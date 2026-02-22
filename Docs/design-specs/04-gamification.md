# 04 — Gamification

> **Screens:** 5 | **User:** Child
> **Related tasks:** D3, D8, D9, D13, R8, R9, R11, R13, P4, P5

---

## 1. Avatar Shop / Cosmetics Store

**Task IDs:** D3, R11, R9 | **Route:** `/shop`

**Purpose:** Kids spend TechCoins on cosmetic items for their avatar. The primary coin sink — motivates earning.

### Layout

```
┌──────────────────────────────────────────────────┐
│  Nav: "חנות"   יתרה: 🪙 250                       │
├──────────┬───────────────────────────────────────┤
│ Avatar   │  [ חנות | מלתחה ]  ← Tab switcher     │
│ Preview  │                                       │
│          │  ┌────┐ ┌────┐ ┌────┐ ┌────┐          │
│ [Current │  │item│ │item│ │item│ │item│          │
│  avatar  │  │ 30 │ │ 50 │ │ 75 │ │100 │          │
│  with    │  │ 🪙  │ │ 🪙  │ │ 🪙  │ │ 🪙  │          │
│  equipped│  └────┘ └────┘ └────┘ └────┘          │
│  items]  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐          │
│          │  │item│ │item│ │item│ │item│          │
│          │  │ 40 │ │ 60 │ │OWNED│ │ 80 │          │
│          │  │ 🪙  │ │ 🪙  │ │ ✅  │ │ 🪙  │          │
│          │  └────┘ └────┘ └────┘ └────┘          │
└──────────┴───────────────────────────────────────┘
```

### Tabs

- **Shop:** All items available for purchase
- **Wardrobe (מלתחה):** Items the kid already owns — equip/unequip

### Item Card States

| State | Visual |
|-------|--------|
| Available (can afford) | Item preview, coin cost, "Buy" on tap |
| Available (can't afford) | Item preview, cost in red, "Not enough coins" on tap |
| Owned (not equipped) | Item preview, "לבשו" button |
| Owned (equipped) | Item preview, green "✅ לבוש" badge, "הסירו" button |

### Interactions

1. Tap item → preview on avatar (left panel updates live)
2. Tap "Buy" → confirmation modal: "?לקנות [שם פריט] ב-X מטבעות" [כן / לא]
3. Purchase confirmed → coin balance deducted, item moves to wardrobe, auto-equip
4. Tap "Equip" → item equipped, avatar updates
5. Tap "Remove" → item unequipped, avatar returns to base

### Edge Cases

- 0 coins → can still browse, all items show "earn more coins" message
- All items owned → "!יש לכם הכל — חזרו כשנוסיף פריטים חדשים" message
- Mobile: avatar preview above shop grid (vertical layout)

---

## 2. Profile Page

**Task IDs:** D11, R15 | **Route:** `/profile` or `/profile/:username`

**Purpose:** Kid's public profile — their avatar, stats, achievements, and identity in the platform.

### Layout

```
┌──────────────────────────────────────┐
│  Nav                                  │
├──────────────────────────────────────┤
│                                       │
│  ┌─ Avatar ──┐  שם: נועה              │
│  │            │  רמה 12: Bug Squasher │
│  │  [Large    │  ⭐ 1,240 / 2,000 XP  │
│  │   avatar]  │  ████████░░░░         │
│  │            │  🪙 250 מטבעות        │
│  └────────────┘  🔥 רצף: 5 ימים       │
│                  📅 הצטרפה: 01/2026    │
│                                       │
│  ── על עצמי ──                        │
│  "אני אוהבת Python ומשחקי מחשב!"     │
│  [✏️ ערכו]                            │
│                                       │
│  ── שיעור נוכחי ──                    │
│  📘 שיעור 7: לולאות While             │
│                                       │
│  ── הישגים (12/40) ──                 │
│  [🏅][🏅][🏅][🏅][🏅][🏅]            │
│  [🏅][🏅][🏅][🏅][🏅][🏅]            │
│  [  ראו את כל ההישגים →  ]           │
│                                       │
└──────────────────────────────────────┘
```

### Components

| Component | Details |
|-----------|---------|
| Avatar | Large display with equipped outfit |
| Level badge | Level number + title (from level titles list) |
| XP bar | Visual progress to next level, fraction shown |
| Coin balance | Current TechCoins |
| Streak counter | Flame icon + days (0 = hidden or "Start a streak!") |
| Join date | Month/year |
| About me | Editable text (max 100 chars), moderated for safety |
| Current lesson | Name + number |
| Achievement grid | First 12 shown (earned = color, locked = silhouette), "see all" link |

### States

- Own profile: edit button on "about me", link to avatar shop
- Other's profile: "Add friend" button (see 05-social.md)
- No achievements yet: "עוד לא השגתם הישגים — המשיכו ללמוד!" empty state

---

## 3. Achievement Browser

**Task IDs:** D13, R13, P5 | **Route:** `/achievements`

**Purpose:** View all achievements, track progress toward locked ones.

### Layout

```
┌──────────────────────────────────────┐
│  "הישגים"   12/40 🏅                  │
├──────────────────────────────────────┤
│  [שאלות] [פרויקטים] [רצפים] [באגים]  │
│          ← Category tabs              │
├──────────────────────────────────────┤
│                                       │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐         │
│  │ 🏅 │ │ 🏅 │ │ 🔒 │ │ 🔒 │         │
│  │First│ │10  │ │50  │ │100 │         │
│  │ Ans │ │Qs  │ │Qs  │ │Qs  │         │
│  │01/26│ │01/26│ │32/50│ │32/ │         │
│  │     │ │     │ │████░│ │100 │         │
│  └────┘ └────┘ └────┘ └────┘         │
│                                       │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐         │
│  │ 🔒 │ │ 🔒 │ │ 🔒 │ │ 🔒 │         │
│  │??? │ │??? │ │??? │ │??? │         │
│  └────┘ └────┘ └────┘ └────┘         │
│                                       │
└──────────────────────────────────────┘
```

### Achievement Card States

| State | Visual |
|-------|--------|
| Earned | Full-color badge, name, date unlocked |
| In progress (visible) | Silhouette, name visible, progress bar (32/50) |
| Locked (hidden) | Silhouette, "???" name, "Keep playing to discover!" |

### Interaction

- Tap earned badge → detail modal: badge large, description, date earned, coin reward received
- Tap in-progress → detail modal: what's needed, current progress
- Tap locked → "!המשיכו ללמוד כדי לגלות"

---

## 4. Level-Up Celebration

**Task IDs:** D8, R8 | **Appears as:** Fullscreen overlay

**Purpose:** Major celebration when kid hits a new level. This is a big moment.

### Layout

```
┌──────────────────────────────────────┐
│                                       │
│          🎉 !עליתם רמה                │
│                                       │
│       [ 11 → 12 ]  (animated)        │
│                                       │
│    "!Bug Squasher — הכינוי החדש שלכם" │
│                                       │
│         +50 🪙 בונוס רמה              │
│                                       │
│     [Confetti animation everywhere]   │
│                                       │
│         [  !מגניב  ]                  │
│                                       │
└──────────────────────────────────────┘
```

### Animation Sequence

1. Screen dims
2. Old level number appears center
3. Arrow animation → new level number (scale up + glow)
4. New title text slides in
5. Coin reward pops up
6. Confetti burst
7. "Cool!" button fades in after 2s

### Edge Cases

- Multiple level-ups at once (rare) → show highest level, mention "!עליתם X רמות בבת אחת"
- Dismiss by tapping anywhere or clicking button
- Auto-dismiss after 8 seconds

---

## 5. XP/Coin Gain Micro-Animations

**Task IDs:** D8, R8, R9 | **Appears on:** Any screen where rewards are earned

**Purpose:** Quick, satisfying feedback every time the kid earns XP or coins.

### XP Gain

- "+20 ⭐" text floats up from the action point (e.g., from the question submit button)
- Gold text, scale up → float up → fade out (1.5s total)
- XP bar in nav simultaneously fills by the earned amount (animated)
- If XP bar fills completely → triggers level-up overlay (Screen 4)

### Coin Gain

- "+10 🪙" text floats up, same animation as XP but amber color
- Coin balance in nav updates with a bounce animation

### Confetti (First-Try Correct)

- Fullscreen particle burst from center
- Colorful, 2-3 second duration
- Doesn't block interaction (decorative layer)
- Triggered by: correct answer on first try, achievement unlock, project complete

### Streak Fire

- Flame icon in nav briefly enlarges + flickers
- At milestones (5, 10, 15...): "!רצף של X" popup below flame
- Streak broken: flame goes grey, brief shake

### Implementation Notes

- All animations use CSS/Lottie — no heavy JS
- Respect `prefers-reduced-motion` media query → disable particle effects
- Keep animations under 3 seconds — they shouldn't delay the kid
