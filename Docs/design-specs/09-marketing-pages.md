# 09 — Marketing Pages

> **Screens:** 5 | **User:** Visitor / Parent
> **Related tasks:** D17, D18, R20, R23, M4, P2, P13, CS1

---

## 1. Landing Page — EXISTING DESIGN

**Task IDs:** D17, R20, M4, P13 | **Route:** `/`

**Purpose:** Convert visitors to free trial signups. The first impression of VRT.

### Enhancement Checklist (for existing Figma)

- [ ] **Hero section:** Headline (Hebrew), sub-headline, CTA button ("!התחילו בחינם"), hero image/illustration of kid coding
- [ ] **Feature showcase:** 3-4 feature cards (interactive lessons, code editor, gamification, parent dashboard)
- [ ] **Pricing section:** Monthly/yearly toggle, Basic vs Premium comparison, prices in NIS
- [ ] **Testimonials:** 2-3 parent/kid quotes (placeholder for beta feedback)
- [ ] **FAQ accordion:** 5-8 common questions
- [ ] **Footer:** Links to ToS, privacy, contact, social media
- [ ] **States to verify:**
  - Desktop (1200px+), tablet (768px), mobile (375px) responsive
  - RTL layout throughout
  - SEO meta tags: title, description, og:image
  - CTA buttons above and below the fold
  - Pricing toggle: monthly (default) vs yearly (shows savings badge)
  - FAQ accordion: closed default, smooth expand/collapse
- [ ] **Performance:** Hero image optimized, lazy-load below-fold images, Core Web Vitals passing

---

## 2. Pricing Page

**Task IDs:** D18, R20, P2 | **Route:** `/pricing`

**Purpose:** Dedicated pricing comparison for visitors evaluating plans.

### Layout

```
┌──────────────────────────────────────┐
│  Nav: VRT Logo   [התחברו]  [הירשמו]  │
├──────────────────────────────────────┤
│                                       │
│  "בחרו את התוכנית המתאימה לכם"       │
│                                       │
│  [ חודשי ● | שנתי ○ ]                │
│  "חסכו X% בתוכנית שנתית!"            │
│                                       │
│  ┌──────────┐    ┌──────────────┐    │
│  │  בייסיק  │    │  ⭐ פרימיום   │    │
│  │          │    │  מומלץ!       │    │
│  │ XX ש"ח   │    │  XX ש"ח      │    │
│  │ /חודש    │    │  /חודש       │    │
│  │          │    │              │    │
│  │ ✅ 28 שיעורים │ ✅ 28 שיעורים │    │
│  │ ✅ 600+ שאלות │ ✅ 600+ שאלות │    │
│  │ ✅ 7 פרויקטים  │ ✅ 7 פרויקטים  │    │
│  │ ✅ הישגים      │ ✅ הישגים      │    │
│  │ ✅ באג האנט    │ ✅ באג האנט    │    │
│  │ ❌ סרטוני הדרכה│ ✅ סרטוני הדרכה│    │
│  │ ❌ תעודות      │ ✅ תעודות      │    │
│  │              │              │    │
│  │[התחילו חינם] │[התחילו חינם ⭐]│    │
│  └──────────┘    └──────────────┘    │
│                                       │
│  "7 ימי ניסיון חינם. ללא כרטיס       │
│   אשראי. ביטול בכל רגע."             │
│                                       │
│  ── שאלות נפוצות ──                  │
│  ▶ מה קורה אחרי תקופת הניסיון?      │
│  ▶ אפשר לשנות תוכנית?               │
│  ▶ יש הנחה למשפחות?                  │
│  ▶ מה אם הילד/ה לא אוהב/ת?          │
│  ▶ איך הילד/ה לומד/ת לבד?            │
│                                       │
└──────────────────────────────────────┘
```

### Components

- Monthly/yearly toggle → prices update live, savings percentage appears on yearly
- Premium card: highlighted border, "Recommended" badge
- CTA → goes to `/signup` (free trial for both plans)
- FAQ: accordion with smooth animation
- Trust signals: "7 day trial, no credit card, cancel anytime" below CTAs

---

## 3. FAQ Page

**Task IDs:** CS1 | **Route:** `/faq`

**Purpose:** 20-30 common questions answered in Hebrew.

### Layout

```
┌──────────────────────────────────────┐
│  "שאלות נפוצות"                       │
├──────────────────────────────────────┤
│                                       │
│  ── חשבון ──                         │
│  ▶ איך נרשמים?                       │
│  ▶ איך הילד/ה מתחבר/ת?              │
│  ▶ שכחתי סיסמה — מה עושים?           │
│                                       │
│  ── תשלום וחיוב ──                   │
│  ▶ כמה זה עולה?                      │
│  ▶ אפשר לבטל?                        │
│  ▶ מה קורה בסוף תקופת הניסיון?       │
│                                       │
│  ── הפלטפורמה ──                     │
│  ▶ מה הילד/ה לומד/ת?                 │
│  ▶ הילד/ה צריך/ה עזרה?               │
│  ▶ באיזה גילאים מתאים?               │
│                                       │
│  ── טכני ──                          │
│  ▶ באיזה מכשירים אפשר להשתמש?       │
│  ▶ צריך להוריד משהו?                 │
│                                       │
│  ── בטיחות ──                        │
│  ▶ איך המידע של הילד/ה מוגן?         │
│  ▶ יש צ'אט? (לא — אין צ'אט ציבורי)  │
│                                       │
│  ┌────────────────────────────────┐   │
│  │  לא מצאתם תשובה?               │   │
│  │  כתבו לנו: support@vrt.co.il  │   │
│  └────────────────────────────────┘   │
│                                       │
└──────────────────────────────────────┘
```

### Components

- Categories with section headers
- Accordion items: click to expand/collapse, smooth animation
- Search (optional for MVP): filter questions by keyword
- Contact fallback at bottom

---

## 4. Terms of Service

**Task IDs:** P13, R23 | **Route:** `/terms`

**Purpose:** Hebrew legal page. Required for compliance.

### Layout

- Clean typography, max-width ~720px for readability
- Numbered sections (1, 1.1, 1.1.1)
- Table of Contents at top (links to sections)
- "Last updated: DD/MM/YYYY" at top
- Print-friendly stylesheet
- `noindex` meta tag (legal pages don't need SEO)
- No game elements — professional, clean

### Sections

1. מבוא (Introduction)
2. הגדרות (Definitions)
3. הרשמה ויצירת חשבון (Registration)
4. חשבונות ילדים (Child accounts)
5. תנאי שימוש (Usage terms)
6. תשלום ומנויים (Payment and subscriptions)
7. קניין רוחני (Intellectual property)
8. הגבלת אחריות (Liability)
9. ביטול והחזרים (Cancellation and refunds)
10. שינויים בתנאים (Changes to terms)
11. דין חל (Governing law — Israeli)
12. יצירת קשר (Contact)

---

## 5. Privacy Policy

**Task IDs:** P13, R23 | **Route:** `/privacy`

**Purpose:** Hebrew privacy policy with special attention to children's data.

### Layout

Same as Terms of Service layout. Key sections:

1. מבוא (Introduction)
2. מידע שאנחנו אוספים (Data collected)
   - Parent: name, email, payment (via Stripe)
   - Child: display name, age, progress, code submissions
   - Automatic: IP, device, browser, analytics
3. איך אנחנו משתמשים במידע (How data is used)
4. **מידע על ילדים** (Children's data — HIGHLIGHTED SECTION)
   - Parental consent required
   - Minimal data collection
   - Children cannot purchase
   - No ads targeting children
   - No sharing with third parties for marketing
   - Parent can request deletion anytime
5. שיתוף עם צדדים שלישיים (Third-party sharing: Stripe, analytics, hosting only)
6. אבטחה (Security: encryption, access controls)
7. קוקיות (Cookies: essential + analytics only, no ads)
8. זכויות המשתמש (User rights: access, correct, delete, export)
9. שמירת מידע (Retention: active = retained, deleted = purged in 30 days)
10. שינויים (Changes)
11. יצירת קשר (Contact)

### Design Note

- Children's data section (4) gets a light highlight box background — this is what parents care most about
- Link to Terms where relevant
