# VRT Visual Identity System

> Version 1.1 — February 2026
> Status: Foundation spec. Design refinement via Lovable → GitHub pipeline.

---

## 1. Brand Positioning

**One-liner:** VRT is a premium self-paced coding platform where kids (10-14) learn real programming through a gamified campaign — no teacher needed.

**Primary audience for visuals:** Parents (decision-makers). They need to see institutional-grade credibility. Think Google Workspace meets Linear.

**Secondary audience:** Kids (10-14). They interact with the platform itself. The product UI can be warmer, but the marketing/landing page is parent-facing.

**Market position:** Premium education tech. Not a toy, not a game pretending to teach code. A real platform with real results, wrapped in a system kids actually want to use.

**Visual tone keywords:** Trustworthy, precise, premium, neo-tech, motion-rich.

**Reference DNA:**
- **Linear** — dark sophistication, surgical typography, glass/blur effects
- **Google Material 3** — bold color system, clean white space, system-level trust
- **Korean motion graphics** (Cavalry/After Effects studios) — fluid transitions, 3D depth, particle systems, kinetic typography

---

## 2. Color System

### 2.1 Primary Palette

| Role | Hex | Name | Usage |
|---|---|---|---|
| Brand Blue | `#4285F4` | VRT Blue | Primary actions, Product plane, links, CTAs |
| Brand Red | `#EA4335` | VRT Red | Marketing plane, alerts, urgency, accent |
| Brand Yellow | `#FBBC04` | VRT Gold | UI/UX plane, highlights, badges, warmth |
| Brand Green | `#34A853` | VRT Green | Success, completion, progress, Done states |

### 2.2 Neutral Scale

| Hex | Name | Usage |
|---|---|---|
| `#FFFFFF` | White | Backgrounds, cards, surfaces |
| `#F8F9FA` | Snow | Page background, subtle card fill |
| `#E8EAED` | Silver | Borders, dividers, inactive elements |
| `#5F6368` | Slate | Secondary text, labels |
| `#3C4043` | Charcoal | Body text |
| `#202124` | Night | Headings, high-emphasis text |
| `#0D0D0F` | Black | Dark mode background (landing page hero) |

### 2.3 Pastel Tints (for plane-coded cards)

| Plane | Background | Border |
|---|---|---|
| Marketing | `#FEF2F1` | `#F5C6C2` |
| Product | `#EEF3FC` | `#C6DAFC` |
| UI/UX | `#FEF9E8` | `#FDE293` |

### 2.4 Semantic Colors

| State | Color | Usage |
|---|---|---|
| In Progress | `#4285F4` | Active work indicators |
| Done | `#34A853` | Completion badges, checkmarks |
| Blocked | `#EA4335` | Blockers, errors, overdue alerts |
| Not Started | `#80868B` | Pending/idle items |

### 2.5 Gradient (Hero use only)

```css
/* Landing page hero — dark premium gradient */
background: linear-gradient(135deg, #0D0D0F 0%, #1A1A2E 50%, #16213E 100%);

/* Accent glow — behind CTAs and hero elements */
background: radial-gradient(circle, rgba(66,133,244,0.15) 0%, transparent 70%);
```

---

## 3. Typography

### 3.1 Font Stack

| Context | Font | Fallback |
|---|---|---|
| Primary (all UI) | **Inter** | -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif |
| Code/terminal (platform) | **JetBrains Mono** | 'Fira Code', 'SF Mono', monospace |
| Display/hero (landing page) | **Inter** at 900 weight | — |

### 3.2 Type Scale

| Element | Size | Weight | Line Height | Letter Spacing |
|---|---|---|---|---|
| Hero headline | 56-72px (clamp) | 900 | 1.05 | -1.5px |
| Section headline | 36-44px | 900 | 1.1 | -0.5px |
| Card title | 18-20px | 800 | 1.2 | -0.2px |
| Body | 15-16px | 400 | 1.6 | 0 |
| Label/caption | 11-12px | 700 | 1.3 | 0.5px (uppercase) |
| Overline/tag | 9-10px | 700 | 1.2 | 0.8px (uppercase) |
| Code | 13-14px | 400 | 1.5 | 0 |

### 3.3 Rules

- Headlines are always `#202124` on light or `#FFFFFF` on dark.
- Body text is `#3C4043` (light) or `#E8EAED` (dark). Never pure black on white.
- Uppercase is reserved for labels, tags, and overlines only.
- Maximum 2 font weights per component (e.g. 800 + 400, never 900 + 800 + 700 + 400).

---

## 4. Spacing & Layout

### 4.1 Base Grid

- **Base unit:** 4px
- **Content max-width:** 1140px (centered)
- **Section padding:** 80px vertical (desktop), 48px (tablet), 32px (mobile)
- **Card padding:** 20-24px
- **Card gap:** 14-16px
- **Component gap (internal):** 8-12px

### 4.2 Responsive Breakpoints

| Name | Width | Columns | Body Padding |
|---|---|---|---|
| Desktop | > 1024px | 3-column grids | 24px |
| Tablet | 640-1024px | 2 or stacked | 16px |
| Mobile | < 640px | 1-column | 12px |

### 4.3 Border Radius Scale

| Element | Radius |
|---|---|
| Page-level containers | 16px |
| Cards (goals, projects) | 12-14px |
| Inner cards (tasks) | 8px |
| Tags, badges | 12px (pill) |
| Buttons | 10px |
| Inputs | 8px |
| Avatars | 50% (circle) |

---

## 5. Component Library

### 5.1 Buttons

| Variant | Background | Text | Border | Hover | Active |
|---|---|---|---|---|---|
| Primary | `#4285F4` | `#FFFFFF` | none | `#3367D6` + shadow | `#2A56C6` |
| Secondary | `#FFFFFF` | `#4285F4` | 1px `#C6DAFC` | bg `#E8F0FE` | bg `#C6DAFC` |
| Danger | `#EA4335` | `#FFFFFF` | none | `#D93025` | `#C5221F` |
| Ghost | transparent | `#5F6368` | none | bg `#F1F3F4` | bg `#E8EAED` |

**Button sizing:**
- Large: 48px height, 16px horizontal padding, 15px font
- Default: 40px height, 14px padding, 14px font
- Small: 32px height, 10px padding, 12px font

**Hover state (all buttons):**
```css
transition: all 0.15s ease;
transform: translateY(-1px);
box-shadow: 0 2px 8px rgba(0,0,0,0.1);
```

**Active state:** Remove translateY, reduce shadow.

### 5.2 Cards

**Surface hierarchy (light mode):**
1. Page background: `#F8F9FA`
2. Group panel: `#FFFFFF` + `box-shadow: 0 1px 4px rgba(0,0,0,0.06)`
3. Inner card: `#F8F9FA` + `border: 1px solid #E8EAED`
4. Nested element: `#FFFFFF` + `border: 1px solid #E8EAED`

**Card hover:**
```css
transition: border-color 0.15s, box-shadow 0.15s;
border-color: #C5C9CF;
box-shadow: 0 4px 16px rgba(0,0,0,0.08);
```

**Card with plane color:** Apply pastel background + matching border from section 2.3.

### 5.3 Tags / Badges

| Type | Style |
|---|---|
| Plane tag | Pastel bg + darker text + 1px border (see 2.3) |
| Status badge | Colored text, no background |
| Count pill | `#E0E3E7` bg, `#3C4043` text, bold, rounded |
| Group badge | Solid color bg, white text, 20px radius |

### 5.4 Progress Bars

```css
/* Track */
height: 6px;
background: #E0E3E7;
border-radius: 3px;
overflow: hidden;

/* Fill — colored by plane */
height: 100%;
border-radius: 3px;
transition: width 0.4s ease;
```

### 5.5 Inputs

| State | Border | Background | Shadow |
|---|---|---|---|
| Default | 1px `#E8EAED` | `#FFFFFF` | none |
| Hover | 1px `#C5C9CF` | `#FFFFFF` | none |
| Focus | 2px `#4285F4` | `#FFFFFF` | `0 0 0 3px rgba(66,133,244,0.15)` |
| Error | 2px `#EA4335` | `#FEF2F1` | `0 0 0 3px rgba(234,67,53,0.15)` |

**Input sizing:** 44px height, 12px padding, 14px font, 8px radius.

### 5.6 Loading States

| Element | Loading Style |
|---|---|
| Page load | Centered VRT logo pulse (scale 0.95-1.05, opacity 0.5-1, 1.2s loop) |
| Card skeleton | `#E8EAED` shimmer (gradient sweep left-to-right, 1.5s) |
| Button loading | Replace text with 16px spinner (white circle, 2px stroke, 0.8s rotation) |
| Progress update | Smooth width transition (0.4s ease) |
| Data refresh | Subtle top-bar progress line (2px, `#4285F4`, slide left-to-right) |

**Skeleton shimmer:**
```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
background: linear-gradient(90deg, #E8EAED 25%, #F1F3F4 50%, #E8EAED 75%);
background-size: 200% 100%;
animation: shimmer 1.5s infinite;
```

---

## 6. Iconography

- **Icon set:** Lucide Icons (open source, consistent with Linear/SaaS aesthetic)
- **Icon size:** 16px (inline), 20px (buttons), 24px (section headers)
- **Icon color:** Inherits text color. Never use colored icons outside of status indicators.
- **Icon weight:** 1.5px stroke (matches Inter's visual weight at body size)

---

## 7. Motion & Animation

### 7.1 Timing

| Duration | Use |
|---|---|
| 100ms | Hover color changes |
| 150ms | Border, shadow transitions |
| 200ms | Opacity fade in/out |
| 300ms | Card slide-in, tab switches |
| 400ms | Progress bar fill |
| 600ms | Page section entrance (staggered) |

### 7.2 Easing

| Curve | Use |
|---|---|
| `ease` | General purpose |
| `cubic-bezier(0.4, 0, 0.2, 1)` | Entrances (Material standard) |
| `cubic-bezier(0, 0, 0.2, 1)` | Exits (Material decelerate) |

### 7.3 Landing Page Motion (Korean MG influence)

These are specs for the landing page hero and section transitions. To be built in Cavalry/After Effects for video, or CSS/JS for web:

- **Hero entrance:** Headline characters stagger in from bottom (30ms delay each, 400ms duration, slight overshoot). Subtext fades up 200ms after headline completes.
- **Product demo pop-out:** Large browser mockup scales from 0.85 to 1.0 with a slight rotation (-2deg to 0deg), shadow grows simultaneously. Input field types demo text char-by-char.
- **Scroll sections:** Each group panel slides up 40px + fades in as it enters viewport (IntersectionObserver, 0.15 threshold).
- **Floating particles:** Subtle background grid dots that parallax at 0.1x scroll speed.
- **Stats counter:** Numbers count up from 0 to target value over 1s on scroll-enter.

---

## 8. Landing Page — Section-by-Section Spec

### 8.1 Hero (above the fold)

**Layout:** Dark gradient background (`#0D0D0F` → `#1A1A2E`). Centered content.

| Element | Spec |
|---|---|
| Headline | "Your kid's first real coding skill." — 56-72px, 900 weight, white |
| Subtext | 1-line value prop — 18px, 400 weight, `#9AA0A6` |
| CTA | Oversized input field ("Enter your email") + blue primary button "Get Early Access" — the input field IS the hero visual |
| Trust bar | Below CTA: "Join 200+ families on the waitlist" + small logos/badges |
| Background | Subtle code particles floating, or a clean 3D render of the campaign map |

**Critical rule:** The hero must pass the 3-second parent test: "This looks like Google/Apple built it. My kid's data is safe here."

### 8.2 How It Works

**Layout:** 3-column grid on light background. Each column = one step.

1. **Pick a Quest** — icon + short description + small UI screenshot
2. **Watch & Code** — icon + description + video thumbnail
3. **Level Up** — icon + description + progress visual

Numbered with large Google-colored numbers (1=Red, 2=Blue, 3=Gold).

### 8.3 Platform Preview

**Layout:** Full-width dark section. Large browser mockup centered, slightly rotated (1-2deg perspective) with depth shadow. Shows the actual campaign map UI.

On scroll: mockup straightens and zooms to 1:1 with a smooth transition.

### 8.4 Social Proof

**Layout:** Light background. Parent testimonials in card format. Video thumbnails of kid demos. Trust badges.

### 8.5 Pricing

**Layout:** 2-3 tier cards. Primary plan highlighted with blue border + "Most Popular" badge. Clean table comparison below.

### 8.6 Footer

**Layout:** Dark (`#0D0D0F`). Logo, nav links, email signup, social links. Minimal.

---

## 9. Platform UI (In-App)

### 9.1 Overall

- **Background:** `#F8F9FA` (light mode default)
- **Sidebar:** `#FFFFFF`, 240px width, collapsible
- **Top bar:** 56px height, white, subtle bottom border
- **Content area:** max 1000px centered, 32px padding

### 9.2 Campaign Map

- **Node style:** Rounded rectangles (12px radius) with plane-colored left border
- **Node states:**
  - Locked: `#E8EAED` bg, `#80868B` text, lock icon
  - Available: White bg, `#202124` text, subtle pulse ring animation
  - In Progress: White bg, blue left border, progress bar inside
  - Completed: `#E6F4EA` bg, green checkmark, strikethrough-style
- **Connection lines:** 2px, `#E0E3E7`, curved (bezier)
- **Active path glow:** `#4285F4` at 20% opacity along the current path

### 9.3 Quest Player

- **Video area:** 16:9, dark surround, rounded corners (12px)
- **Code editor below:** JetBrains Mono, dark theme (`#1E1E1E` bg), 14px
- **Run button:** Green (`#34A853`), 44px height, icon + "Run Code"
- **Output panel:** Below code, light bg, monospace, bordered

### 9.4 Login Screen

- **Layout:** Split — left half dark gradient with VRT logo + tagline, right half white with form
- **Form:** Email + password + "Start Coding" primary button
- **OAuth:** Google sign-in button (Material spec)
- **Below form:** "New here? Start free" link in blue

---

## 10. Creative Marketing

### 10.1 YouTube Thumbnails

| Element | Spec |
|---|---|
| Background | Dark gradient or solid VRT Blue |
| Face/reaction shot | Right 40% of frame, high contrast |
| Title text | 3-5 words max, Inter 900, white or yellow |
| Logo | VRT wordmark, bottom-left corner, small |
| Border/glow | 3px colored border or outer glow matching plane |

### 10.2 Social Media

- **Instagram/TikTok:** Square/vertical. Bold headline + platform screenshot + CTA at bottom.
- **Color system:** Rotate between the 3 plane colors across posts for variety.
- **Text overlay:** Always Inter 800-900, always on a solid or gradient background panel (never directly on images).

### 10.3 Email Templates

- **Width:** 600px max
- **Header:** VRT logo on white, thin blue bottom border
- **Body:** `#F8F9FA` background, white content cards
- **CTA button:** Blue primary, centered, 44px height
- **Footer:** Dark, minimal, unsubscribe link

### 10.4 Presentation Slides

- **Background:** White or dark (not both in one deck)
- **Title slides:** Large Inter 900, left-aligned, colored accent bar on left
- **Content:** Max 3 bullets per slide, 20px font minimum
- **Data viz:** Use the Google 4-color palette only

---

## 11. Accessibility

- All text meets WCAG AA contrast (4.5:1 for body, 3:1 for large text)
- Focus rings: 2px `#4285F4` with 3px transparent offset
- All interactive elements have hover + focus + active states
- Min tap target: 44x44px on mobile
- Color is never the only indicator — always pair with icons or text

---

## 12. Design Asset Pipeline — Lovable → GitHub

### 12.1 Pipeline Overview

All visual design work follows a single canonical flow:

```
Lovable (design & iterate) → Export → GitHub repo → Deploy / Integrate
```

| Stage | Tool | What happens | Output |
|---|---|---|---|
| **Design** | Lovable | Build and iterate on UI components, pages, and layouts using the Visual Identity specs in this doc | Live preview + generated code |
| **Review** | Lovable | Alon reviews in-browser, requests changes via Lovable chat | Approved design |
| **Export** | Lovable → GitHub | Push approved code directly from Lovable to the VRT GitHub repo | Committed code in repo |
| **Integrate** | GitHub → Local | Matan pulls from GitHub, integrates into the VRT codebase | Production-ready code |
| **Sync back** | Local → Dashboard | Dashboard generator pulls updated styles/tokens if needed | Updated dashboard.html |

### 12.2 Lovable Workflow

1. **Start a project in Lovable** — paste the VRT Visual Identity brief (this document) as the design prompt
2. **Iterate** — use Lovable's chat to refine components against the specs (colors, typography, spacing, motion)
3. **Export to GitHub** — use Lovable's built-in GitHub integration to push directly to the `vrt` repo
4. **Branch strategy** — Lovable pushes to a `design/lovable-export` branch; Matan reviews and merges to `main`

### 12.3 What Lives Where

| Asset type | Source of truth | Location |
|---|---|---|
| Visual Identity spec | This document | `Docs/VRT-Visual-Identity.md` + Notion Design Specs |
| UI component code | GitHub | `vrt` repo (exported from Lovable) |
| Landing page design | Lovable → GitHub | `vrt` repo, `design/lovable-export` branch |
| Platform UI design | Lovable → GitHub | Same repo, platform-specific directories |
| Marketing assets (thumbnails, social) | Google Drive / Figma | `Marketing-Handoff/` locally |
| Dashboard HTML | Auto-generated | `Docs/dashboard.html` (from `Scripts/generate-dashboard.py`) |
| Design tokens (colors, fonts, spacing) | This document | Referenced by both Lovable prompts and the Python generator |

### 12.4 Handoff Rules

- **Lovable is the design tool** — all UI/UX iteration happens there, not in raw code
- **GitHub is the single source of code** — once exported, Lovable's output lives in the repo
- **Never edit Lovable exports locally without merging back** — if Matan modifies exported code, changes must be committed to GitHub so the next Lovable export doesn't overwrite them
- **Design tokens stay in this doc** — if Lovable produces new colors/spacing, update this doc to keep it canonical
- **Dashboard generator stays independent** — it reads from Notion, not from Lovable/GitHub; visual styles should be consistent but the generator is its own pipeline

---

## 13. File & Asset Naming

```
vrt-{type}-{context}-{variant}.{ext}

Examples:
vrt-icon-logo-blue.svg
vrt-thumb-youtube-ep01.png
vrt-screen-campaign-desktop.png
vrt-motion-hero-entrance.mp4
```

---

## 14. Summary: The 3-Second Rule

Every VRT visual must pass this test:

> A parent lands on the page. In 3 seconds, they think: "This is a real company. This looks like it was built by Google. My kid's time and my money are safe here."

Everything — from the font weight to the hover shadow to the loading spinner — serves that single goal. Trust is the product. The code education is the feature.
