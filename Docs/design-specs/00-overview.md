# VRT MVP — Design Specs Overview

> **Product:** VRT (Virtual Techies) — Self-paced Python coding education for kids 10-14
> **Language:** Hebrew-first (RTL), light theme
> **Feel:** Game-quality UI, fast, not "school software"
> **Total screens:** ~74 across 11 flows

---

## Design Principles

1. **Game, not school** — Every interaction should feel like playing, not studying. Console-quality feedback (animations, sounds, celebrations).
2. **Zero adult help** — A 10-year-old must be able to navigate every screen without asking a parent.
3. **Speed is a feature** — If anything takes >3s to load, kids switch tabs. Heavy caching, instant transitions.
4. **Hebrew-first RTL** — All UI right-to-left. Code blocks remain LTR. Numbers in standard Arabic numerals.
5. **Light theme** — Bright, vibrant, kid-safe colors. Not dark/intimidating.
6. **Celebrate everything** — Correct answers get confetti. Level-ups get fanfare. Streaks get fire. Make progress feel amazing.
7. **Safe by default** — No public chat, moderated "about me", parental controls, COPPA-like data handling.

---

## Color & Typography Direction

- **Background:** White/light grey (#FAFAFA)
- **Primary accent:** Vibrant blue or purple (brand TBD — see D1)
- **Success:** Green (#22C55E)
- **Warning:** Amber (#F59E0B)
- **Error:** Red (#EF4444)
- **XP/Level:** Gold (#EAB308)
- **Coins:** Amber/Gold
- **Code editor:** Light theme Monaco with kid-friendly syntax colors (see D6)
- **Typography:** Clean sans-serif, large sizes for kids. Hebrew: system fonts (Arial/Helvetica). Code: monospace (Fira Code/JetBrains Mono).

---

## Existing Figma Designs

These screens already have final designs. Specs focus on completeness (states, edge cases):

| Screen | Status | Spec File |
|--------|--------|-----------|
| Child Login | Designed | 01-auth-onboarding.md |
| Quest Map (2 screens) | Designed | 02-learning-core.md |
| Coding Workspace / IDE | Designed | 02-learning-core.md |
| Landing Page | Designed | 09-marketing-pages.md |

---

## Screen Map by Flow

| # | Flow | File | Screens | Key Task IDs |
|---|------|------|---------|--------------|
| 01 | Auth & Onboarding | `01-auth-onboarding.md` | 11 | D19, D4, R2, P8 |
| 02 | Learning Core | `02-learning-core.md` | 12 | D5, D6, D7, D15, R5, R6, R7, P3, P6 |
| 03 | Projects | `03-projects.md` | 2 | D10, R18, P3 |
| 04 | Gamification | `04-gamification.md` | 5 | D3, D8, D9, D13, R8, R9, R11, R13, P4, P5 |
| 05 | Social | `05-social.md` | 5 | D11, R15, R16, R17 |
| 06 | Bug Hunt | `06-bug-hunt.md` | 4 | D14, R14, P7 |
| 07 | Parent Dashboard | `07-parent-dashboard.md` | 5 | D12, R12, P9 |
| 08 | Payments & Trial | `08-payments-trial.md` | 4 | R3, R4, P2, D17 |
| 09 | Marketing Pages | `09-marketing-pages.md` | 5 | D17, D18, R20, R23, M4, P13 |
| 10 | Emails | `10-emails.md` | 4 | P14, D16, R12 |
| 11 | Navigation & Components | `11-navigation-components.md` | ~17 | D4, D8, D9, D20 |

---

## Reusable Component Index

These components appear across multiple screens:

| Component | Used In | Notes |
|-----------|---------|-------|
| Top Nav Bar (Child) | All child screens | Logo, level badge, XP bar, coins, avatar |
| Top Nav Bar (Parent) | All parent screens | Logo, child selector, account, logout |
| Sidebar / Nav Drawer | All child screens (mobile) | Links to all sections |
| Monaco Code Editor | Lessons, questions, projects, Bug Hunt | Run/Reset buttons, output panel |
| Difficulty Badge | Questions, Bug Hunt | Color-coded: green/yellow/orange/red |
| Level Badge | Nav, profile, leaderboards | Level # + title |
| Coin Display | Nav, shop, hints, rewards | Coin icon + balance |
| XP Bar | Nav, profile, weekly report | Progress to next level |
| Toast Notifications | All screens | Success/error/info, auto-dismiss |
| Modal / Confirmation | Shop purchases, deletions, quit game | Title, message, 2 buttons |
| Confetti Animation | Correct answers, achievements, level-up | Fullscreen burst |
| Streak Fire | Streak milestones | Flame icon animation |
| Empty State | Friends, achievements, lessons | Character illustration + CTA |
| Loading Spinner | Code execution, API calls | Centered, branded |
| CTA Button | All screens | Primary (filled), secondary (outlined) |

---

## User Types

| User | Access | Key Flows |
|------|--------|-----------|
| **Visitor** | Landing, pricing, FAQ, legal pages | Marketing → signup |
| **Parent** | Auth, dashboard, payments, settings, emails | Manage child + subscription |
| **Child** | Login, quest map, lessons, questions, projects, gamification, social, Bug Hunt | Learn + play |
| **Admin** | Admin panel (future — R24) | Manage content |

---

## RTL Implementation Notes

- `dir="rtl"` on root element
- All layouts mirror: sidebars on right, back buttons on right, etc.
- Code editors/blocks: always `dir="ltr"` (code is LTR in all languages)
- Numbers: standard Arabic numerals (1, 2, 3), not Eastern Arabic
- Mixed content (Hebrew text + code inline): use `<bdo>` or CSS `unicode-bidi` where needed
- Date format: `DD/MM/YYYY` or `DD בחודש YYYY` (Hebrew month names)
