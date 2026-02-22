# 10 — Email Templates

> **Templates:** 4 | **User:** Parent
> **Related tasks:** P14, D16, R12
> **Format:** HTML, Hebrew RTL, mobile-responsive (600px max-width), branded header/footer

---

## Global Email Standards

| Element | Details |
|---------|---------|
| Direction | `dir="rtl"` on body |
| Language | `lang="he"` |
| Width | 600px max, centered, responsive to 320px |
| Header | VRT logo (centered) |
| Footer | VRT name, support email, unsubscribe link |
| Font | Arial, Helvetica, sans-serif (email-safe) |
| CTA buttons | Min 44px height, brand color, white text, rounded |
| Sender | `VRT — Virtual Techies <noreply@vrt.co.il>` |
| Reply-to | `support@vrt.co.il` |
| Unsubscribe | One-click header + visible footer link |

---

## 1. Welcome Email (Day 1)

**Trigger:** Immediately after parent signup
**Subject:** `!ברוכים הבאים ל-VRT — המסע של [שם הילד] מתחיל`
**Preheader:** `.7 ימי ניסיון חינם. 5 שיעורים. הילד/ה שלכם כבר יכול/ה להתחיל`

### Content Sections

1. **Greeting:** "!היי [שם ההורה], שמחים שהצטרפתם"
2. **What to do next (numbered steps):**
   - ① Add child (if not done) — link to parent dashboard
   - ② Child logs in with code — show login code prominently (large, monospace, highlighted box)
   - ③ Start learning — first quest is ready
3. **Trial info box** (light background card):
   - Trial: 7 days
   - Lessons available: 5
   - End date: DD/MM/YYYY
   - No credit card. No commitment.
4. **Primary CTA:** `התחילו ללמוד →` → app link
5. **FAQ/Support:** link to FAQ + support email

### Edge Cases

- Multiple children → list all names and codes
- Child name not provided → use "הילד/ה שלכם"
- Plain text fallback for clients that don't render HTML

---

## 2. Trial Ending Email (Day 6)

**Trigger:** Day 6 of 7-day trial (1 day before expiry)
**Subject:** `⏳ תקופת הניסיון מסתיימת מחר — הנה מה ש[שם הילד] הספיק/ה`
**Preheader:** `.[שם הילד] כבר למד/ה X שיעורים ופתר/ה X שאלות`

### Content Sections

1. **Headline:** "תקופת הניסיון מסתיימת מחר"
2. **Progress summary card:**
   - Avatar + child's name
   - 📘 Lessons completed: X
   - ✅ Questions solved: X
   - ⭐ Current level: X
   - ⏱️ Time spent: X minutes
   - Motivational line: "[שם הילד] בדרך הנכונה!"
3. **Plan options:** Basic / Premium with monthly prices (simplified — 2 columns)
4. **Primary CTA:** `הירשמו עכשיו →` → `/parent/subscribe`
5. **Reassurance:** "Cancel anytime. No commitment."

### Edge Cases

- Child has 0 progress → skip progress card, show: "עוד לא התחילו — עוד יש זמן!"
- Trial already converted → suppress this email (backend guard)

---

## 3. Payment Failed Email

**Trigger:** Stripe `invoice.payment_failed` webhook
**Subject:** `⚠️ התשלום ל-VRT נכשל — נדרש עדכון`
**Preheader:** `.הגישה ממשיכה עד [date]. עדכנו את אמצעי התשלום`

### Content Sections

1. **Headline:** "התשלום נכשל" (clear, not alarming)
2. **Details:** "ניסינו לגבות עבור תוכנית [name] אבל התשלום לא עבר."
3. **Reassurance box** (calming blue/green background):
   - "[שם הילד] ממשיך/ה ללמוד עד DD/MM."
   - "יש לכם זמן לעדכן."
4. **Primary CTA:** `עדכנו אמצעי תשלום →` → Stripe Customer Portal
5. **Common reasons:** expired card, credit limit, temporary bank issue
6. **Support:** "?צריכים עזרה" + email link

### Edge Cases

- Multiple failures → escalate tone: "ניסינו מספר פעמים — נא לעדכן בהקדם"
- Grace period < 2 days → "הגישה תיפסק בעוד יומיים"
- Free/trial accounts → don't trigger this email

---

## 4. Weekly Parent Report

**Trigger:** Every Sunday morning (Israel time), for active children
**Subject:** `📊 הדוח השבועי של [שם הילד] ב-VRT`
**Preheader:** `.[שם הילד] השלים/ה X שיעורים והשיג/ה X הישגים השבוע`

### Content Sections

1. **Header:** VRT logo, child's name, week range (DD/MM — DD/MM)
2. **Child header:** Avatar + name + current level & title
3. **Stats grid (2×2):**
   - Lessons completed this week
   - Questions solved this week
   - Time spent learning
   - New achievements earned
4. **New achievements section:**
   - List with 🏆 icons (max 3 shown, "+X more" link)
   - None: "אין הישגים חדשים — השבוע הבא יהיה טוב יותר!"
5. **Level progress bar:**
   - HTML/CSS bar (not image)
   - Current level → next level
   - Percentage shown
6. **Primary CTA:** `צפו בדוח המלא →` → parent dashboard
7. **Trial CTA (conditional):**
   - Only for trial users
   - "נותרו X ימים" + subscribe CTA
   - Expired: "תקופת הניסיון הסתיימה — הירשמו כדי להמשיך"

### Edge Cases

- Child had no activity → modified email: "[שם] לא למד/ה השבוע. תזכורת עדינה יכולה לעזור!" (or skip sending — configurable)
- Multiple children → one email per child (recommended for clarity)
- Parent unsubscribed from reports → respect, don't send
- Stats are all zero → skip stats grid, show encouragement message
- Level at 100% progress → "!עומד/ת לעלות רמה" celebration styling
