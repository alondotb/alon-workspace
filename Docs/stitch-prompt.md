# VRT (Virtual Techies) — Full MVP Wireframe + Visual Design

## Product Overview

A self-paced Python coding education platform for kids aged 10-14. Hebrew-first (RTL), light theme. Kids learn through a 2D campaign node tree with "quests" (video-based lessons that auto-start). No teacher needed. Game-quality UI — console-level feedback, animations, celebrations. Think Duolingo meets a 2D adventure game, but for coding.

Target launch: April 2026. Currency: Israeli New Shekel (₪). Language: Hebrew (RTL throughout, except code blocks which are always LTR).

---

## Design Principles

1. **Game, not school** — every interaction feels like gameplay. Confetti on correct answers, fanfare on level-ups, XP and coins everywhere.
2. **Zero adult help** — a 10-year-old navigates independently. Large touch targets (44px+), clear icons, simple language.
3. **Speed is a feature** — max 3s load times, instant feedback on code runs.
4. **Hebrew-first RTL** — all UI mirrored for right-to-left. Navigation flows right-to-left. Code blocks always LTR.
5. **Light theme** — bright, vibrant, kid-safe colors on white/light grey backgrounds.
6. **Celebrate everything** — confetti, floating +XP text, streak fire animations, level-up overlays.

---

## Color Palette

- **Background:** White (#FFFFFF) / Light grey (#FAFAFA)
- **Primary accent:** Vibrant purple-blue (brand TBD, suggest #6C3AED or #4F46E5)
- **Success/Correct:** Green #22C55E
- **Warning:** Amber #F59E0B
- **Error/Incorrect:** Red #EF4444
- **XP/Level:** Gold #EAB308
- **Coins:** Amber/Gold
- **Code editor:** Light theme with kid-friendly syntax highlighting
- **Text:** Dark grey #1F2937 on light backgrounds

## Typography

- Clean sans-serif (Inter, Rubik, or similar with Hebrew support)
- Large text for kids — body 16px minimum, headings 24-36px
- Code: Fira Code or JetBrains Mono, 14px, always LTR
- Hebrew system fonts for body text

---

## Four User Types

1. **Visitor** — landing page, pricing, FAQ, legal
2. **Parent** — signup, dashboard, subscription, child management
3. **Child** — the main user: quests, coding, gamification, social
4. **Admin** — future, not in MVP

---

## SCREEN-BY-SCREEN WIREFRAMES

### FLOW 1: AUTH & ONBOARDING (11 screens)

**Screen 1.1 — Child Login** `/login`
Game-style entry screen. Large "Ready to Code?" headline in Hebrew. Username field, password field (RTL), big vibrant "Login" button. VRT logo/mascot illustration. Bright, inviting, playful. Game-style swoosh transition on success.

**Screen 1.2 — Parent Signup** `/signup`
Clean form: VRT logo, "Create Account" headline, name field, email field (with validation), password field (show/hide toggle, strength indicator: weak/medium/strong), "Sign Up" primary button, Google OAuth button, Terms/Privacy links at bottom. Professional but friendly.

**Screen 1.3 — Email Verification Pending** `/verify-email`
Logo, envelope illustration, "Check your email" message showing the sent-to address, "Resend" button with 60-second cooldown timer.

**Screen 1.4 — Email Verification Success** `/verify-email/success`
Checkmark animation, "Email verified!" message, "Add your child" CTA button. Auto-redirects after 3s.

**Screen 1.5 — Parent Login** `/parent/login`
Email field, password field (show/hide), "Remember me" checkbox, "Login" button, Google OAuth, "Forgot password?" link, "Sign up" link. Separate from child login — more professional styling.

**Screen 1.6 — Forgot Password** `/forgot-password`
Email input, "Send Reset Link" button, back to login link.

**Screen 1.7 — Reset Password** `/reset-password`
New password field, confirm password field, strength indicator, "Save" button.

**Screen 1.8 — Add Child Form** `/parent/add-child`
Username input with live availability check (✅/❌ indicator, debounced), birth year dropdown (2011-2016), password input (min 4 chars). "Add Child" primary button.

**Screen 1.9 — Avatar Selection** `/onboarding/avatar`
Full-screen "Choose Your Character!" headline. Grid of 10 cartoon avatar options (colorful, diverse characters). Large preview of selected character on the side (full-body, animated idle). Hover = enlarge + shadow. Selected = border + checkmark + enlarge. "Confirm" button.

**Screen 1.10 — Avatar Selection Success**
🎉 Confetti animation, celebration message, character illustration, "Ready to learn to code?", "Go to first lesson!" CTA. Auto-redirects after 4s.

**Screen 1.11 — Parent Account Settings** `/parent/settings`
Email + verification status, password change, daily time limit slider (30min–6hrs, default 2hrs), notification toggles (weekly email, trial ending), red "Delete Account" button with confirmation modal.

---

### FLOW 2: LEARNING CORE (12 screens) — THE HEART OF THE PRODUCT

**Screen 2.1 — Quest Map / Campaign Dashboard** `/quests`
The main hub. A visual 2D campaign tree showing 28 quest nodes connected by paths, like a board game map. Always-visible HUD at top: avatar portrait, level badge + title, animated XP progress bar, coin balance (🪙), streak counter (🔥).

Quest node states:
- **Locked:** Grey, dim, lock icon
- **Available:** Glowing pulsing border, bright color
- **In Progress:** Arrow icon, circular progress ring
- **Completed:** Checkmark, star rating, full color
- **Current (active):** Largest node, animated glow, distinct

Overall progress bar ("X/28 quests"). Scrollable/pannable map. First-time user sees only quest 1 available with an arrow animation pointing to it.

**Screen 2.2 — Quest Briefing** `/quests/:id/briefing`
Back button, quest title, description paragraph, "What you'll learn" bullet list, estimated time, question count + requirement ("Pass 5 of 6 to unlock next"), big "Start" button.

**Screen 2.3 — Coding Workspace / Lesson Viewer** `/quests/:id/learn`
Split layout:
- **Top/Left:** Content area — video player (if premium, embedded, auto-start) OR written content (Hebrew RTL text, headings, images, scrollable)
- **Bottom/Right:** Interactive code blocks (5-8 per lesson):
  - Monaco code editor (light theme, pre-loaded with example code, editable)
  - "▶ Run" button (green, with loading spinner state)
  - "↺ Reset" button
  - Output panel below editor: hidden initially, green border on success, red border on error with kid-friendly Hebrew error message
- **Navigation:** Previous/Next buttons, question counter "📝 5/6 required"
- Auto-saves every keystroke. Hint system: yellow bubble appears after 3+ fails.

**Screen 2.4 — Question: Code Write** `/quests/:id/questions/:qid`
Question number/total, difficulty badge (easy/medium/hard with color), prompt text in Hebrew, empty code editor (or starter code), "Submit" button, "Hint" button, "Skip" button.
Result states:
- ✅ Correct (1st try): Confetti, "Amazing!", +XP/coins floating popup, explanation panel
- ✅ Correct (2+ tries): "Passed!", reduced XP, explanation
- ❌ Incorrect: "Not quite — try again", show expected vs actual, retry
- ⏱️ Timeout: "Code running too long"

**Screen 2.5 — Question: Code Fix**
Same layout as Code Write but prompt says "Find and fix the bug:" with pre-filled buggy code. Editor is editable.

**Screen 2.6 — Question: Multiple Choice**
Question prompt, read-only code block, 4 radio button options. Submit button. Correct = green highlight. Incorrect = red highlight + correct shown in green.

**Screen 2.7 — Question: Output Predict**
"What will this code print?" with read-only code block and a text input field (LTR, for code output). Submit + check.

**Screen 2.8 — Question: Fill in the Blank**
Code block with a highlighted `_______` blank. Input field below to fill in the missing code.

**Screen 2.9 — Hint Tiers Modal**
Overlay: "💡 Hints" title, current coin balance. 3 tiers:
- Hint 1 (5 coins): gentle nudge
- Hint 2 (15 coins): more specific
- Hint 3 (30 coins): near-complete walkthrough
Each tier: locked (with cost + "Reveal" button) or revealed (hint text visible). Can't afford = greyed button.

**Screen 2.10 — Explanation Display**
Shown after correct answer. "Why this is correct:" header, explanation text, related code example. Collapsible.

**Screen 2.11 — Lesson Progress Counter**
In-lesson header: "📝 5/6 questions completed" with progress bar. At threshold: green fill + celebration "Next lesson unlocked!" banner.

**Screen 2.12 — Lesson Unlocked Celebration**
Fullscreen overlay: 🎉 "Congratulations!", next lesson preview card, +XP/coins rewards, "Continue" button. Confetti animation.

---

### FLOW 3: PROJECTS (2 screens)

**Screen 3.1 — Project Page (Guided Steps)** `/projects/:id`
Two-column: left sidebar with vertical step list (✅ completed, → current, ○ upcoming). Right: step title, instructions, code editor, run/reset, output panel, previous/next step buttons. Linear progress bar.

**Screen 3.2 — Project Completion Certificate** `/projects/:id/certificate`
Certificate card: VRT branding, child's name, project name, date, VRT logo. +XP/coins rewards. Download PDF + print buttons. Confetti on load.

---

### FLOW 4: GAMIFICATION (5 screens)

**Screen 4.1 — Avatar Shop** `/shop`
Two-column: left = large avatar preview with equipped items. Right = shop grid of purchasable cosmetic items. Tabs: Shop / Wardrobe.
Item states: Available (coin cost + "Buy"), Can't afford (red cost, greyed), Owned ("Equip"), Equipped (green ✅ + "Remove").

**Screen 4.2 — Profile Page** `/profile`
Large avatar with outfit, stats: name, level + title, XP bar, coin balance, streak, join date. Editable "About me" (100 chars). Current lesson indicator. Achievement grid (first 12, earned = color, locked = silhouette).

**Screen 4.3 — Achievement Browser** `/achievements`
Title with count (X/40), category tabs (Questions, Projects, Streaks, Bugs). Grid of achievement badges. Earned: full color + date. In progress: silhouette + progress bar. Locked: silhouette + "???" name.

**Screen 4.4 — Level-Up Celebration**
Fullscreen overlay: dim screen, old level → animated arrow → new level (scale up + glow), new title slides in, coin reward popup, confetti burst, "Cool!" button after 2s.

**Screen 4.5 — XP/Coin Micro-Animations**
"+20 ⭐" gold text floats up from action point (1.5s). "+10 🪙" amber text same. Nav bars update simultaneously with smooth fill/bounce.

---

### FLOW 5: SOCIAL (5 screens)

**Screen 5.1 — Other User's Profile** `/profile/:username`
Same as own profile + "Add Friend +" button (or "Request Sent ⏳" or "Friends ✅").

**Screen 5.2 — Friend Requests** `/friends/requests`
Tabs: Received (X) / Sent (Y). List of friend cards with avatar, name, level, accept/decline or cancel buttons.

**Screen 5.3 — Friends List** `/friends`
Friend count, list of cards: avatar, name, level, online indicator (🟢/⚫), "View profile" button. Empty state: "No friends yet 😊".

**Screen 5.4 — Leaderboards** `/leaderboard`
Tabs: Global / Weekly / Friends. Table: rank, avatar, name, level, XP. Top 3 with medal icons (🥇🥈🥉). Current user row highlighted + pinned.

**Screen 5.5 — Bug Hunt Leaderboard** `/leaderboard/bughunt`
Tabs: All-time (bugs fixed) / Daily Challenge (solve time). Fastest solver badge.

---

### FLOW 6: BUG HUNT MINI-GAME (4 screens)

**Screen 6.1 — Mode Selection** `/bughunt`
3 mode cards: Quick Play (⚡), Endless (♾️), Daily Challenge (📅). Each shows personal best + "Play" button. Leaderboard link.

**Screen 6.2 — Quick Play** `/bughunt/quick`
Header: ⚡ mode indicator, ⏱️ timer (counts up), Bug X/5. Split code view: buggy code (read-only) above, editable fix below. Output panel. "🔍 Check Fix" button. Game over screen: time, bugs fixed, XP, coins, personal best comparison.

**Screen 6.3 — Endless Mode** `/bughunt/endless`
Same as Quick Play + ❤️❤️❤️ lives, 🔥 streak counter, difficulty indicator bar (Easy→Medium→Hard with color). Life lost = heart crack + red flash. Game over at 0 lives.

**Screen 6.4 — Daily Challenge** `/bughunt/daily`
One bug, no hints, timer, one attempt per day. Result: your time, ranking #X of Y, coin/XP bonus, leaderboard preview, countdown to next challenge.

---

### FLOW 7: PARENT DASHBOARD (5 screens)

**Screen 7.1 — Parent Dashboard Home** `/parent`
Subscription status bar (Active ✅ / Trial ⏳ / Past Due ⚠️ / Cancelled). Child card(s): avatar + name + level, current lesson X/28, time spent this week, stats grid (lessons/questions/achievements), "View full report" link. "Add child" button.

**Screen 7.2 — Child Progress Detail** `/parent/child/:id/progress`
Summary: Lessons X/28, questions solved, accuracy %, total time, level, achievements X/40.
Charts: Bar chart (weekly lessons, 8 weeks), pie/donut (question accuracy), line chart (daily time, 7 days). Latest achievements list. Projects checklist.

**Screen 7.3 — Add Child Form** (same as 1.8)

**Screen 7.4 — Parent Settings** (same as 1.11)

**Screen 7.5 — Daily Time Limit — Child View**
Fullscreen overlay when time's up: ⏰ "Time's up for today!", character illustration, motivational message, today's stats, "Goodbye" button. 5-minute warning toast beforehand.

---

### FLOW 8: PAYMENTS & TRIAL (4 screens)

**Screen 8.1 — Subscription Management** `/parent/subscription`
Current plan card (name, ₪ price/month, status badge, renewal date). Action buttons: "Change plan", "Update payment" (→ Stripe), "View billing history" (→ Stripe), "Cancel subscription" (red). Plan comparison table.

**Screen 8.2 — Trial Paywall / Subscribe** `/parent/subscribe`
Trial countdown banner "⏳ X days left". Child progress summary card (avatar, stats, motivational). Monthly/yearly toggle (savings % on yearly). Plan cards: Basic vs Premium ⭐ (highlighted, "Recommended" badge). FAQ accordion. "Cancel anytime" reassurance.

**Screen 8.3 — Payment Failed Banner**
Appears on parent dashboard: ⚠️ "Payment failed", "Access continues until DD/MM", "Update payment →" CTA. Tone escalates with repeated failures.

**Screen 8.4 — Subscription Success** `/parent/subscribe/success`
🎉 "Welcome to [plan]!", child continues learning, back to dashboard button.

---

### FLOW 9: MARKETING PAGES (5 screens)

**Screen 9.1 — Landing Page** `/`
Hero: Hebrew headline, sub-headline, "Start free!" CTA, hero illustration of kid coding. Feature showcase: 3-4 cards (interactive lessons, code editor, gamification, parent dashboard). Pricing section: toggle monthly/yearly, Basic vs Premium. Testimonials (2-3 quotes). FAQ accordion. Footer: links, social, legal.

**Screen 9.2 — Pricing Page** `/pricing`
Headline, monthly/yearly toggle, 2 plan cards (Basic, Premium ⭐ highlighted with "Recommended"), savings badge, feature comparison grid, FAQ, trust signals ("7-day trial, no credit card, cancel anytime").

**Screen 9.3 — FAQ Page** `/faq`
Categories: Account, Payment, Platform, Technical, Safety. Accordion sections. "Contact support" fallback.

**Screen 9.4 — Terms of Service** `/terms`
Clean typography, max-width 720px, numbered sections, table of contents. Hebrew.

**Screen 9.5 — Privacy Policy** `/privacy`
Same layout as Terms. Children's data section highlighted.

---

### FLOW 10: EMAIL TEMPLATES (4 templates)

**Template 10.1 — Welcome Email**
VRT logo, "Welcome! [Child]'s journey begins", 3 numbered steps (add child, login code in highlighted box, start learning), trial info card (7 days, 5 lessons), "Start Learning →" CTA. Hebrew RTL, 600px max-width.

**Template 10.2 — Trial Ending (Day 6)**
"⏳ Trial ending tomorrow", child progress card (avatar, lessons, questions, level, time), plan options (Basic/Premium), "Subscribe now →" CTA.

**Template 10.3 — Payment Failed**
"⚠️ Payment failed", reassurance box ("Access continues until..."), "Update payment →" CTA, common reasons list.

**Template 10.4 — Weekly Parent Report**
Child header (avatar, name, level), 2×2 stats grid (lessons/questions/time/achievements), achievement badges (max 3), level progress bar, "View full report →" CTA.

---

### FLOW 11: SHARED COMPONENTS (17 components)

**Child Top Nav:** [VRT Logo] 📘 Current Lesson | 🔥5 🪙150 ⭐████░ Lv7 [👤 Avatar]. RTL: logo right, stats left. Mobile: hamburger, logo + coins + avatar visible.

**Child Sidebar/Drawer:** Avatar + name + level, links: 📘 Quests, 🏆 Achievements, 👤 Profile, 👥 Friends, 📊 Leaderboard, 🐛 Bug Hunt, 🛍️ Shop, ⚙️ Settings, 🚪 Logout. Mobile: slides from right (RTL).

**Parent Top Nav:** [VRT Logo] [Child: dropdown] [⚙️] [🚪]

**Public Nav:** [VRT Logo] Pricing FAQ | [Login] [Sign Up]

**Loading Spinner:** Full-page (VRT logo + spinner), inline (button spinner), code execution ("...running").

**Toast Notifications:** Bottom-left (RTL). Success (green ✅), Error (red ❌), Info (blue ℹ️), Warning (amber ⚠️). Auto-dismiss 4-6s.

**Confirmation Modal:** Title, message, secondary + primary buttons, close X. Semi-transparent dark backdrop.

**Difficulty Badge:** Easy (green "קל"), Medium (yellow "בינוני"), Hard (orange "קשה"), Challenge (red "אתגר"). Small pill/chip.

**Level Badge:** Circular/shield shape. Colors scale: Grey 1-5, Blue 6-10, Purple 11-15, Gold 16-20, Diamond 21-30. Titles: Beginner → Explorer → Learner → Bug Squasher → Coder → Developer → Hacker → Master → Champion.

**XP/Coin Animations:** Floating "+20 ⭐" / "+10 🪙" text, scale up → float up → fade out.

**Confetti Animation:** Fullscreen colorful burst on achievements/level-ups/first-try correct.

**Streak Fire:** 🔥 flame in nav, enlarges on milestones, grey + shake when broken.

**Empty States:** Character illustration + encouraging message + CTA. Themed per context.

**Error Pages:** 404 (confused character), 500 (character fixing machine).

**Time's Up Overlay:** ⏰ blocking overlay when daily limit reached.

**Code Editor:** Monaco, light theme, Python, Fira Code 14px, line numbers, no minimap, word wrap, always LTR.

---

## Visual Design Summary

- **Feel:** Bright, gamified, playful but not childish. Think Duolingo's polish meets a coding adventure.
- **Layout:** Clean white cards on light grey background. Generous spacing. Rounded corners (12-16px).
- **Cards:** White (#FFF), subtle shadow, 12-16px border-radius, 16-24px padding.
- **Buttons:** Rounded (10-12px radius), large (44px+ height), bold text, primary = brand purple/blue, secondary = outline.
- **Icons:** Simple, line-style, 24px. Emoji used liberally for gamification (🔥⭐🪙🏆🎉💡🐛).
- **Animations:** Smooth micro-animations on everything. Confetti particles, floating XP text, progress bar fills, hover scales, page transitions.
- **RTL:** All text, layouts, and navigation flow right-to-left. Code editor always LTR.
- **Responsive:** Desktop (1200px+), tablet (768px), mobile (375px). Touch targets 44px+.
- **Accessibility:** High contrast on light bg, clear focus states, prefers-reduced-motion support.

---

## Key Screens Priority (design these first)

1. Quest Map / Campaign Dashboard (Screen 2.1) — the hero screen
2. Coding Workspace (Screen 2.3) — the core learning experience
3. Child Login (Screen 1.1) — first impression
4. Landing Page (Screen 9.1) — marketing entry
5. Question: Code Write (Screen 2.4) — the main interaction loop
6. Profile Page (Screen 4.2) — gamification showcase
7. Bug Hunt Quick Play (Screen 6.2) — the mini-game
8. Parent Dashboard (Screen 7.1) — parent value prop
