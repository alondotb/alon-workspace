# VRT (Virtual Techies) — Brand Brief

> **Purpose:** Source of truth for all visual design work in Figma. This document defines VRT's brand identity and unblocks D1 (Brand Identity) and all downstream design tasks (D2-D22).
> **Last updated:** 2026-02-17

---

## 1. Brand Personality & Voice

### Who We're Talking To
- **Primary:** Kids aged 10-14, Israeli, Hebrew-speaking
- **Secondary:** Their parents (who pay)
- **Tertiary:** Educators who may recommend us

### Brand Personality
VRT is the **cool older sibling** who happens to know how to code. Not a teacher, not a clown — a guide who makes hard things feel achievable and fun.

| Trait | What it means | What it's NOT |
|-------|--------------|---------------|
| **Confident** | "You can do this" energy. The UI feels polished, not amateur. | Arrogant, intimidating |
| **Playful** | Celebrates wins, uses humor, feels like a game | Childish, babyish, patronizing |
| **Real** | Teaches actual Python, not toy code. Kids feel like developers. | Corporate, dry, textbook |
| **Warm** | Encouraging, never punishing mistakes. "Try again!" not "Wrong." | Soft, hand-holding, overprotective |
| **Hebrew-native** | Not a translated product. Hebrew feels natural, not forced. | Stilted, formal Hebrew |

### Voice Guidelines (Hebrew)
- **Tone:** Casual, direct, encouraging. Like texting a friend who's good at coding.
- **Use:** שפה פשוטה, מילים קצרות, הסברים עם דוגמאות מהחיים (משחקים, בית ספר, טיקטוק)
- **Avoid:** Academic Hebrew, overly formal language, condescending explanations
- **Error messages:** "אופס! משהו לא עבד — בוא ננסה שוב" (not "שגיאה: קלט לא תקין")
- **Celebrations:** "!אלוף! פתרת את זה" / "!אש! רצף של 5" / "!מטורף! השלמת את כל האתגרים"

---

## 2. Color Palette

### Primary Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Primary** | Deep Violet | `#6C3AED` | CTAs, active states, navigation accents, brand identity |
| **Primary Light** | Soft Violet | `#8B5CF6` | Hover states, secondary buttons, backgrounds |
| **Primary Dark** | Dark Violet | `#5B21B6` | Pressed states, dark text on light backgrounds |
| **Background** | Off White | `#FAFAFA` | Main page background |
| **Surface** | White | `#FFFFFF` | Cards, modals, elevated surfaces |
| **Surface Alt** | Light Gray | `#F3F4F6` | Secondary backgrounds, code output panels |

### Accent Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Success** | Emerald Green | `#22C55E` | Correct answers, completed lessons, pass states |
| **Warning** | Amber | `#F59E0B` | Hints, streak warnings, medium difficulty |
| **Error** | Red | `#EF4444` | Wrong answers, errors, failed states |
| **XP/Level** | Gold | `#EAB308` | XP bars, level badges, achievement glow |
| **Coins** | Warm Amber | `#D97706` | TechCoin balance, purchase indicators |
| **Info** | Sky Blue | `#0EA5E9` | Tooltips, informational badges, links |

### Game Accent Colors

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| **Easy** | Mint Green | `#34D399` | Easy difficulty badge, beginner content |
| **Medium** | Yellow | `#FBBF24` | Medium difficulty badge |
| **Hard** | Orange | `#F97316` | Hard difficulty badge |
| **Challenge** | Hot Pink | `#EC4899` | Challenge difficulty badge, rare items |
| **Streak Fire** | Flame Orange | `#FF6B35` | Streak animations, multiplier indicators |

### Rationale
- **Violet as primary:** Differentiates from every major competitor. Scratch = orange. Code.org = purple/teal (institutional). CodeCombat = dark navy. Tynker = red. Our violet is vibrant, modern, and sits perfectly between "playful" and "serious" — a 12-year-old won't feel it's babyish, and a 10-year-old won't find it intimidating.
- **Light theme:** Design spec mandate. Bright and vibrant for a kid-safe, inviting feel.
- **Game colors:** Difficulty tiers use a traffic-light-inspired gradient (green → yellow → orange → pink) that's instantly readable without text labels.

### Accessibility Notes
- All text on `#FAFAFA` background must meet **WCAG AA** minimum (4.5:1 contrast ratio)
- `#6C3AED` on white = **4.6:1** contrast ratio (passes AA for normal text)
- `#5B21B6` on white = **7.1:1** (passes AAA)
- Error red `#EF4444` on white = **3.9:1** — use on large text only, or pair with icons/text labels
- Success green `#22C55E` on white = **3.0:1** — always pair with icon (checkmark) for accessibility
- **For kids:** Use larger font sizes (16px+ body) to ensure readability even at lower contrast ratios
- **Code editor:** Light theme with high-contrast syntax highlighting (see D6 spec)

---

## 3. Typography System

### Hebrew (Primary)

| Role | Font | Weight | Size | Usage |
|------|------|--------|------|-------|
| **Display / H1** | **Heebo** | 700 (Bold) | 32-40px | Page titles, celebration screens |
| **H2** | Heebo | 600 (SemiBold) | 24-28px | Section headers, lesson titles |
| **H3** | Heebo | 600 | 20-22px | Card titles, feature headers |
| **Body** | Heebo | 400 (Regular) | 16-18px | Lesson text, descriptions, UI labels |
| **Small/Caption** | Heebo | 400 | 13-14px | Timestamps, secondary info, footnotes |
| **Button** | Heebo | 600 | 14-16px | CTAs, nav items |

**Why Heebo:**
- Purpose-built for Hebrew. Excellent readability at all sizes.
- Clean, modern geometric sans-serif — feels friendly, not formal.
- Available on Google Fonts (free, fast CDN delivery).
- Supports all Hebrew characters including niqqud (if ever needed).
- Works beautifully in RTL layout.

### Code (Monospace)

| Role | Font | Weight | Size | Usage |
|------|------|--------|------|-------|
| **Code Editor** | **JetBrains Mono** | 400 | 14-16px | Monaco editor, all code blocks |
| **Inline Code** | JetBrains Mono | 400 | 14px | Code references within Hebrew text |
| **Code Output** | JetBrains Mono | 400 | 13-14px | Console/terminal output |

**Why JetBrains Mono:**
- Designed specifically for reading code — excellent character differentiation (0 vs O, l vs 1, etc.)
- Ligatures available (optional, can enable for a polished feel)
- Free and open-source
- Kids using VRT will feel like they're using a real developer tool

### English (Secondary — for code keywords, UI labels where needed)

| Role | Font | Fallback |
|------|------|----------|
| **UI** | Inter | system-ui, -apple-system |
| **Code** | JetBrains Mono | Fira Code, monospace |

### Type Scale
```
xs:   13px / 1.4 line-height
sm:   14px / 1.5
base: 16px / 1.6
lg:   18px / 1.6
xl:   20px / 1.5
2xl:  24px / 1.4
3xl:  32px / 1.3
4xl:  40px / 1.2
```
All body text for kids should be **base (16px)** minimum. Lesson content should be **lg (18px)** for comfortable reading.

---

## 4. Logo Direction & Usage

### Logo Concept
The VRT logo should communicate: **code + game + kids + Israel (Hebrew)**.

### Direction A — "The Quest Node" (Recommended)
- A stylized node/diamond shape (referencing the campaign quest tree)
- Contains subtle code brackets `< >` or terminal cursor `▋` within the shape
- "VRT" or "Virtual Techies" wordmark in Heebo Bold
- The node shape becomes a recurring brand motif (quest map, achievement badges, level indicators)

### Direction B — "The Code Character"
- A mascot-based logo — a stylized character (could be a robot, animal, or abstract figure)
- Holds or interacts with code symbols
- More playful, more kid-targeted
- Risk: harder to scale to older audiences later

### Direction C — "The Terminal"
- Clean, text-based logo with a code aesthetic
- Terminal cursor or bracket motif: `>_ VRT`
- More "serious coder" feel
- Risk: may feel too grown-up for 10-year-olds

### Logo Usage Guidelines
- **Minimum size:** 32px height on screen
- **Clear space:** Minimum 1x logo height on all sides
- **On light backgrounds:** Primary (deep violet) or dark variant
- **On dark backgrounds:** White variant
- **Never:** Stretch, rotate, add effects, change colors outside palette
- **Favicon:** Simplified version (node shape only, no wordmark)

### Hebrew Branding
- Primary name display: **VRT** (Latin letters — internationally recognizable)
- Tagline in Hebrew: **"ללמוד קוד. לשחק בגדול."** (Learn code. Play big.) — or similar
- Marketing pages: Full Hebrew name **"וירטואל טקיז"** appears alongside the logo

---

## 5. Visual Style

### Illustration Style
**"Clean Game Art"** — not pixel art, not flat corporate, not 3D rendered. A distinctive 2D illustration style that feels like quality indie game art.

| Characteristic | Description |
|---------------|-------------|
| **Dimension** | 2D with subtle depth (soft shadows, layered elements) |
| **Line work** | Clean outlines, consistent stroke width (2-3px at standard size) |
| **Color** | Bold, saturated fills from the brand palette. No pastels. |
| **Characters** | Stylized proportions (slightly large heads, expressive faces). Diverse skin tones, hair styles, clothing. |
| **Backgrounds** | Simple, geometric. Gradient meshes or subtle patterns. Never photo-realistic. |
| **Icons** | Outlined style, 24px grid, 2px stroke. Rounded corners. Match illustration feel. |
| **Animations** | Snappy, juicy. Ease-out transitions. Celebrate with particle effects (confetti, sparks, fire). |

### UI Mood
- **Light and vibrant** — white/light backgrounds with violet/color accents
- **Card-based layouts** — rounded corners (12-16px radius), subtle shadows
- **Generous spacing** — kids need breathing room, don't crowd the UI
- **Large tap targets** — minimum 44x44px for all interactive elements (mobile-friendly)
- **Game-quality polish** — micro-interactions on hover, animated transitions between screens, satisfying button press feedback
- **Not "school software"** — no institutional blue, no clipart, no textbook vibes

### Icon System
- **Style:** Outlined, 2px stroke, rounded line caps
- **Grid:** 24x24px base
- **Key icons needed:**
  - Navigation: home, lessons, achievements, profile, settings, Bug Hunt
  - Game: XP star, TechCoin, streak fire, level badge, hint lightbulb
  - Learning: play (run code), reset, check, X, hint, "come back later"
  - Social: friends, leaderboard, emote reactions
  - Difficulty: 4 tier badges (easy/medium/hard/challenge)

### Animation Principles
1. **Fast feedback** — Button presses, correct/wrong answers: < 200ms
2. **Celebration moments** — Level-up, achievement unlock, streak milestone: 500-1500ms
3. **Transitions** — Page changes, modal open/close: 200-300ms
4. **Physics-based** — Ease-out curves, slight overshoot on celebrations
5. **Never blocking** — Animations should never prevent the kid from continuing

---

## 6. Competitive Visual Analysis

### Landscape Overview

| Platform | Visual Identity | Target Age | VRT Differentiation |
|----------|----------------|------------|---------------------|
| **CodeCombat** | Dark RPG, medieval pixel art, gritty | 9-16 | VRT is brighter, more vibrant, modern (not retro). Light theme vs dark. |
| **Tynker** | Generic edtech, red/teal, flat illustration, heavy IP licensing (Minecraft) | 5-18 | VRT has a sharper, owned visual identity. No borrowed IP. Focused age range. |
| **Scratch** | Orange/white, minimal, community-driven, cartoon mascot | 8-16 | VRT signals "graduation from Scratch" — text-based code, more sophisticated design. |
| **Codecademy** | Navy/gold, professional, adult SaaS aesthetic | 16+ adult | VRT bridges the gap — serious enough for real code, fun enough for kids. |
| **Code.org** | Purple/teal, institutional, photography-based, nonprofit feel | K-12 | VRT is a product you choose, not software your school assigns. Game-first, not institution-first. |

### Where VRT Wins Visually

1. **The 10-14 sweet spot is unclaimed.** No competitor designs specifically for preteens who want to feel capable and slightly grown-up. Tynker tries 5-18 and pleases no one fully. Scratch skews young. Codecademy skews adult.

2. **Original character-based illustration.** CodeCombat has sprites (genre-locked to medieval). Scratch has the Cat (associated with beginners). VRT creating diverse, mission-driven characters gives us ownable visual assets.

3. **The quest tree as visual identity.** No competitor uses learning progression as a core brand element. VRT's campaign node tree can become as iconic as Duolingo's skill tree.

4. **Vibrant violet palette.** Every competitor either uses dark themes (CodeCombat, Codecademy) or generic colors (Tynker's red, Code.org's institutional purple). Our vibrant violet with game-accent colors is distinctive and ownable.

5. **Hebrew-first design.** No competitor designs for Hebrew/RTL from the ground up. Everyone else retrofits. VRT's UI will feel native to Israeli kids.

---

## 7. Design File Checklist

Once this brand brief is approved, the following design tasks are unblocked:

- [ ] **D1:** Brand identity finalized (logo, colors, type) — in Figma
- [ ] **D2:** Design system / component library
- [ ] **D3:** Avatar characters (8-10 base)
- [ ] **D4:** Navigation & layout system
- [ ] **D5:** Quest map design
- [ ] **D6:** Code editor theme
- [ ] **D7:** Question UI (all types)
- [ ] **D8:** XP/Level/Coin UI elements
- [ ] **D9:** Achievement badge icons (30-40)
- [ ] **D10:** Project UI
- [ ] **D11:** Social screens (friends, leaderboard)
- [ ] **D12:** Parent dashboard
- [ ] **D13:** Avatar shop / customization
- [ ] **D14:** Bug Hunt mini-game UI
- [ ] **D15:** Lesson viewer (base + premium layouts)
- [ ] **D16:** Email templates
- [ ] **D17:** Landing page (final with brand)
- [ ] **D18:** Pricing page
- [ ] **D19:** Auth flows
- [ ] **D20:** Celebration animations (confetti, streak, level-up)

---

## 8. Quick Reference Card

```
Brand:        VRT / Virtual Techies / וירטואל טקיז
Tagline:      ללמוד קוד. לשחק בגדול.
Primary:      #6C3AED (Deep Violet)
Background:   #FAFAFA (Off White)
Success:      #22C55E  |  Warning: #F59E0B  |  Error: #EF4444
XP Gold:      #EAB308  |  Coins: #D97706
Hebrew Font:  Heebo (Google Fonts)
Code Font:    JetBrains Mono
Body Size:    16px min, 18px for lesson content
Radius:       12-16px cards, 8px buttons
Tap Target:   44px minimum
Theme:        Light
Direction:    RTL (code blocks LTR)
```
