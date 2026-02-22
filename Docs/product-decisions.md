# VRT — Product Decision Log

> **Purpose:** Clean reference of all confirmed product decisions extracted from mvp.md. Use this as the quick-access source of truth — no need to re-read the full MVP doc for specifics.
> **Source:** `~/Downloads/virtual-techies-master/Vision/mvp/mvp.md`
> **Last updated:** 2026-02-17

---

## P2: Pricing Tiers — CONFIRMED

### Subscription Plans

| Plan | Monthly | Yearly | Savings |
|------|---------|--------|---------|
| **Basic** | 55 NIS/month (~$15) | 450 NIS/year | ~210 NIS (2 months free) |
| **Premium** | 75 NIS/month (~$20) | 600 NIS/year | ~300 NIS (2 months free) |

### What's Included

| Feature | Basic | Premium |
|---------|-------|---------|
| Written lessons + interactive code blocks | Yes | Yes |
| ~20 practice questions per lesson | Yes | Yes |
| XP, TechCoins, leveling | Yes | Yes |
| Avatar + customization shop | Yes | Yes |
| Achievements (30-40) | Yes | Yes |
| Bug Hunt mini-game | Yes | Yes |
| Friends + leaderboard | Yes | Yes |
| Parent dashboard + weekly email | Yes | Yes |
| Weekly office hours (live) | Yes | Yes |
| **Video lessons embedded in lesson page** | **No** | **Yes** |

### Trial
- **7-day free trial** for all new users
- **Limited to 5 lessons** — enough to experience the game loop
- Trial includes **premium features** (video) so kids experience the full product
- **No credit card required** — this is the acquisition funnel
- After trial: user must choose Basic or Premium to continue

### Payment
- **Stripe** (cards, Apple Pay, Google Pay) — works in Israel
- **Cancellation:** Self-serve, immediate. Access continues until end of billing period.

---

## P3: Curriculum Structure — CONFIRMED

### 28 Lessons, Python Only

| # | Lesson | Questions | Min to Advance | Project |
|---|--------|-----------|----------------|---------|
| 1 | Variables & Print | 20 | 5 | — |
| 2 | Input & Strings | 20 | 5 | — |
| 3 | Numbers & Math | 20 | 6 | — |
| 4 | Booleans & Comparisons | 20 | 6 | — |
| 5 | If / Else | 20 | 6 | — |
| 6 | Elif & Nested Conditions | 20 | 6 | Terminal Calculator |
| 7 | While Loops | 20 | 7 | — |
| 8 | For Loops | 20 | 7 | — |
| 9 | Lists | 20 | 7 | — |
| 10 | List Methods | 20 | 7 | To-Do List App |
| 11 | Tuples | 15 | 5 | — |
| 12 | Dictionaries | 20 | 7 | — |
| 13 | Sets | 15 | 5 | Contact Book |
| 14 | Functions (Basics) | 20 | 7 | — |
| 15 | Functions (Parameters & Return) | 20 | 7 | — |
| 16 | Functions (Advanced) | 20 | 8 | Number Guessing Game |
| 17 | String Methods | 20 | 7 | — |
| 18 | File Reading | 15 | 5 | — |
| 19 | File Writing | 15 | 5 | Personal Diary |
| 20 | Error Handling (try/except) | 15 | 5 | — |
| 21 | Imports & Modules | 15 | 5 | — |
| 22 | OOP: Classes & Objects | 20 | 8 | — |
| 23 | OOP: Methods | 20 | 8 | — |
| 24 | OOP: Inheritance | 20 | 8 | Pet Virtual Tamagotchi |
| 25 | List Comprehensions | 15 | 5 | — |
| 26 | Lambda Functions | 15 | 5 | — |
| 27 | Working with JSON | 15 | 5 | Quiz Game Engine |
| 28 | Final Project: Choose Your Own | — | — | Student-proposed |

### Content Totals

| Type | Count |
|------|-------|
| Lessons | 28 |
| Lesson questions | ~550-600 |
| Mini-game questions (Bug Hunt) | ~200 |
| **Total question bank** | **~750-800** |
| Projects | 7 (+1 final) |
| In-lesson videos (premium) | ~28 |

### Question Design

| Tier | Questions | Difficulty | XP Reward | Coin Reward |
|------|-----------|-----------|-----------|-------------|
| Easy | 1-5 | Direct application | 10 | 5 |
| Medium | 6-10 | Combine with prior learning | 20 | 10 |
| Hard | 11-15 | Multi-step problem solving | 30 | 15 |
| Challenge | 16-20 | Creative, edge-case-heavy | 50 | 20 |

### Question Types
- `code_write` — Write code from scratch
- `code_fix` — Fix buggy code
- `multiple_choice` — Choose correct answer
- `output_predict` — Predict what code outputs
- `fill_blank` — Complete missing code

### Hint System
- Hint 1: 5 TechCoins (gentle nudge)
- Hint 2: 15 TechCoins (more specific)
- Hint 3: 30 TechCoins (near-complete walkthrough)

---

## P4: Gamification Rules — CONFIRMED

### XP & Leveling

| Level Range | Title | XP Range |
|-------------|-------|----------|
| 1-5 | Code Newbie | Beginner |
| 6-10 | Bug Squasher | Early intermediate |
| 11-15 | Script Kiddo | Intermediate |
| 16-20 | Function Master | Upper intermediate |
| 21-25 | Class Builder | Advanced |
| 26-30 | Pythonist | Expert |

### TechCoin Economy

**Earning:**

| Action | Coins |
|--------|-------|
| Correct answer (Easy) | 5 |
| Correct answer (Medium) | 10 |
| Correct answer (Hard) | 15 |
| Correct answer (Challenge) | 20 |
| Complete lesson (min required questions) | 50 |
| Complete ALL questions in a lesson | 200 bonus |
| Complete a project | 150 |
| Daily login | 10 |
| 7-day login streak | 2x daily login |
| 30-day login streak | 5x daily login |
| Bug Hunt session | 5-30 (based on performance) |
| Achievement unlock | 25-200 (based on rarity) |

**Spending:**

| Item | Cost |
|------|------|
| Hint 1 | 5 coins |
| Hint 2 | 15 coins |
| Hint 3 | 30 coins |
| Avatar outfits | Varies |
| Profile backgrounds | Varies |
| Profile badges | Varies |

**Difficulty tier completion bonuses:**

| Tier Completed | Bonus |
|---------------|-------|
| All Easy (1-5) | "Warm-Up Champion" + 25 coins |
| All Medium (6-10) | "Getting Serious!" + 50 coins |
| All Hard (11-15) | "Problem Solver" + 100 coins |
| All Challenge (16-20) | "Master of [Topic]" badge + 200 coins + rare avatar item |

### Streak System
- 3 correct in a row: fire streak animation + 2x coin multiplier
- 5 correct in a row: 3x multiplier
- 10 correct in a row: "On Fire!" badge

### Achievements (~30-40 total)

**Question achievements:**
- First Blood — Solve first question
- On Fire! — 10 correct in a row
- Hundred Club — 100 questions total
- Completionist — All 20 questions in a lesson
- Master of [Topic] — All Challenge-tier for a topic
- Speed Demon — Hard question in < 60 seconds
- No Hints Needed — Full lesson without hints
- Comeback Kid — Solve a previously failed question

**Project achievements:**
- Builder — Complete first project
- Full Stack Kid — All projects done
- Certified Pythonist — Earn Python certificate

**Streak & engagement:**
- First Steps — Complete lesson 1
- Streak Master — 7-day login streak
- Dedicated — 30-day login streak
- Night Owl — Solve question after 10pm
- Early Bird — Solve question before 7am

**Mini-game:**
- Bug Squasher — Fix 10 bugs
- Exterminator — Fix 50 bugs
- Daily Champion — Top Daily Challenge leaderboard
- Flawless — 5 in a row in Endless Mode

### Avatar System
- 8-10 pre-designed characters
- 3-4 outfit variations each (purchasable with TechCoins)
- Displayed on: profile, leaderboard, lesson completion screens
- No open world in MVP — avatar is a profile representation

### Bug Hunt Mini-Game
- **Quick Play:** 5 bugs, 60 seconds each
- **Endless Mode:** Increasing difficulty, survival-based
- **Daily Challenge:** One curated bug/day, global leaderboard
- Draws from separate ~200 question pool
- Difficulty adapts to player's learned topics

---

## P8: Onboarding Flow — CONFIRMED

### Step-by-Step

1. **Parent lands on marketing page** → CTA: "Start free trial"
2. **Parent creates account** — Email + password (or Google sign-in). Email verification sent.
3. **Parent adds child** — Child's name, username (unique), birth year
4. **Child login created** — Separate login for the child (under parent account)
5. **Child logs in** → Avatar selection screen (choose from 8-10 characters)
6. **Quick tour** — 3-4 screens explaining: quest map, XP/coins, Bug Hunt
7. **Drop into Lesson 1** — "Variables & Print" auto-starts
8. **Trial begins** — 7 days, 5 lessons, premium features included

### Key Design Decisions
- Parent and child have **separate login flows**
- No credit card required for trial
- Avatar selection is the first "fun" moment — before any learning
- The tour is skippable but short enough that most kids will watch
- Trial limitation (5 lessons) shown clearly but not aggressively

---

## P13: Legal Requirements — CONFIRMED

### Required for Israeli Market + Kids' Data

| Requirement | Status | Priority |
|------------|--------|----------|
| **Terms of Service** | Needs drafting | Must-have for launch |
| **Privacy Policy** | Needs drafting | Must-have for launch |
| **COPPA-like compliance** | Must implement | Critical — kids' data |
| **Israeli Privacy Law (PPPA)** | Must comply | Critical |
| **Parental consent flow** | Built into onboarding (parent creates account) | Critical |
| **Data minimization** | Collect only what's needed | Best practice |
| **PII encryption** | Encrypt all personally identifiable information | Critical |
| **Cookie consent** | Implement banner/notice | Required |
| **Right to deletion** | Parent can request data deletion | Israeli law |
| **No public chat** | Enforced in MVP | Safety requirement |
| **Moderated "about me"** | Content filter on free-text field | Safety requirement |

### COPPA-Like Principles (No COPPA in Israel, but follow spirit)
- Parent creates account, not child
- Parent provides consent implicitly by creating child's account
- Minimal data collected from children (username, birth year, progress data)
- No free-text chat between children
- No targeted advertising to children
- Parent can view all child data
- Parent can request deletion of child's account and data

### What Needs to Be Produced
1. **Terms of Service** — Hebrew, covering subscription terms, cancellation, age requirements
2. **Privacy Policy** — Hebrew, covering data collection, storage, sharing, deletion rights
3. **Cookie Policy** — Hebrew, explaining analytics/essential cookies
4. **Parent consent mechanism** — Built into signup flow (parent email verification = consent)

---

## P14: Email Communication Plan — CONFIRMED

### 4 Email Templates

| Email | Trigger | Timing | Content |
|-------|---------|--------|---------|
| **Welcome** | Parent creates account | Immediate | Welcome message, what to expect, how to help child get started, trial details |
| **Weekly Progress Report** | Automated (cron) | Every Sunday | Lessons completed, questions solved, time spent, XP earned, achievements unlocked, encouragement |
| **Trial Ending** | Trial day 5 | 2 days before trial ends | Reminder of progress so far, what they'll lose, conversion CTA (choose Basic or Premium) |
| **Win-Back / Re-engagement** | Child inactive 7+ days | After 7 days of no activity | "Your Python skills miss you!" — show progress so far, encourage return |

### Email Specifications
- **Sender:** VRT / Virtual Techies
- **Language:** Hebrew (RTL layout)
- **Service:** Resend or SendGrid
- **Design:** Branded template matching VRT visual identity (see brand brief)
- **Parent-facing:** All emails go to parent's email address
- **Tone:** Warm, encouraging, data-driven (show specific numbers)

### Weekly Progress Report Contents
- Child's avatar + name + level
- Lessons completed this week (count + names)
- Questions solved (total + breakdown by difficulty)
- Time spent (hours/minutes)
- XP earned + current level
- New achievements unlocked
- Streak status
- CTA: "See full dashboard" (links to parent dashboard)

---

## Quick Decision Index

| Decision | Answer | Section |
|----------|--------|---------|
| How many subscription tiers? | 2 (Basic + Premium) | P2 |
| What does Premium add? | Video lessons in each lesson page | P2 |
| Monthly Basic price? | 55 NIS/month | P2 |
| Monthly Premium price? | 75 NIS/month | P2 |
| Free trial length? | 7 days | P2 |
| Trial lesson limit? | 5 lessons | P2 |
| Credit card for trial? | No | P2 |
| How many lessons? | 28 | P3 |
| How many questions total? | ~750-800 | P3 |
| Questions per lesson? | ~15-20 | P3 |
| Min to advance? | 5-8 (varies by lesson) | P3 |
| How many projects? | 7 (+1 final) | P3 |
| Level range? | 1-30 | P4 |
| Coin per correct answer? | 5/10/15/20 (by difficulty) | P4 |
| Hint costs? | 5/15/30 coins | P4 |
| Avatar count? | 8-10 characters | P4 |
| Mini-game? | Bug Hunt (single player) | P4 |
| Chat? | No (pre-set emotes only) | MVP scope |
| Target age? | 10-14 only | MVP scope |
| Language? | Hebrew-first | MVP scope |
| Code language? | Python only | MVP scope |
