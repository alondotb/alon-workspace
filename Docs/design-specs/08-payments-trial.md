# 08 — Payments & Trial

> **Screens:** 4 | **User:** Parent
> **Related tasks:** R3, R4, P2, D17, D18

---

## 1. Subscription Management

**Task IDs:** R3, P2 | **Route:** `/parent/subscription`

**Purpose:** Parent views and manages their subscription plan.

### Layout

```
┌──────────────────────────────────────┐
│  "ניהול מנוי"                         │
├──────────────────────────────────────┤
│                                       │
│  ┌─ Current Plan ────────────────┐   │
│  │  תוכנית נוכחית:               │   │
│  │  פרימיום חודשי — XX ש"ח/חודש   │   │
│  │  סטטוס: ✅ פעיל                │   │
│  │  חידוש: 15/03/2026             │   │
│  └────────────────────────────────┘   │
│                                       │
│  ── אפשרויות ──                      │
│                                       │
│  [  שנו תוכנית  ]                    │
│  [  עדכנו אמצעי תשלום  ] → Stripe    │
│  [  ראו היסטוריית חיובים  ] → Stripe │
│                                       │
│  ── ביטול ──                         │
│  [  בטלו מנוי  ] (red text)          │
│                                       │
│  ┌─ Plan Comparison ─────────────┐   │
│  │                                │   │
│  │  בייסיק        │  פרימיום      │   │
│  │  XX ש"ח/חודש   │  XX ש"ח/חודש  │   │
│  │  XX ש"ח/שנה    │  XX ש"ח/שנה   │   │
│  │                │               │   │
│  │  ✅ 28 שיעורים  │  ✅ 28 שיעורים │   │
│  │  ✅ שאלות       │  ✅ שאלות      │   │
│  │  ✅ פרויקטים     │  ✅ פרויקטים    │   │
│  │  ✅ הישגים       │  ✅ הישגים      │   │
│  │  ❌ סרטונים      │  ✅ סרטונים     │   │
│  │                │               │   │
│  └────────────────────────────────┘   │
│                                       │
└──────────────────────────────────────┘
```

### Plan Status States

| Status | Visual | Actions Available |
|--------|--------|-------------------|
| Active | ✅ green badge | Change plan, update payment, cancel |
| Trial | ⏳ blue badge, "X ימים נותרו" | Subscribe (upgrade), no cancel |
| Past Due | ⚠️ red badge, "תשלום נכשל" | Update payment (urgent CTA) |
| Cancelled | Grey badge, "גישה עד DD/MM" | Resubscribe |

### Interactions

- "Change plan" → shows plan options inline or modal
- "Update payment" → redirects to Stripe Customer Portal
- "View billing history" → redirects to Stripe Customer Portal
- "Cancel subscription" → confirmation modal with exit survey:
  - "?למה אתם עוזבים" (optional dropdown: too expensive, child not interested, found alternative, other)
  - Confirmation: "הגישה תמשיך עד DD/MM" → confirm

---

## 2. Trial Paywall / Subscribe

**Task IDs:** R4, P2 | **Route:** `/parent/subscribe`

**Purpose:** Shown when trial is ending or parent wants to upgrade. Convert free to paid.

### Layout

```
┌──────────────────────────────────────┐
│  ⏳ "תקופת הניסיון מסתיימת בעוד     │
│      X ימים"                          │
├──────────────────────────────────────┤
│                                       │
│  ┌─ Child Progress Summary ──────┐   │
│  │  [Avatar] נועה — רמה 8         │   │
│  │  7 שיעורים | 42 שאלות | 3 הישגים│  │
│  │  "!נועה בדרך הנכונה"           │   │
│  └────────────────────────────────┘   │
│                                       │
│  בחרו תוכנית:                         │
│                                       │
│  [ חודשי ○ | שנתי ○ ] ← Toggle       │
│                                       │
│  ┌─────────┐    ┌─────────────┐      │
│  │ בייסיק  │    │  ⭐ פרימיום  │      │
│  │          │    │             │      │
│  │ XX ש"ח  │    │  XX ש"ח     │      │
│  │ /חודש    │    │  /חודש      │      │
│  │          │    │             │      │
│  │ שיעורים  │    │ שיעורים     │      │
│  │ שאלות    │    │ שאלות       │      │
│  │ פרויקטים │    │ פרויקטים    │      │
│  │          │    │ + סרטונים   │      │
│  │          │    │             │      │
│  │ [בחרו]   │    │ [⭐ בחרו]   │      │
│  └─────────┘    └─────────────┘      │
│                                       │
│  "חיסכון של X% בתוכנית שנתית!"      │
│                                       │
│  ── שאלות נפוצות ──                  │
│  ▶ אפשר לבטל בכל רגע?               │
│  ▶ מה ההבדל בין בייסיק לפרימיום?     │
│  ▶ יש החזר כספי?                     │
│                                       │
│  אפשר לבטל בכל רגע. בלי התחייבות.    │
│                                       │
└──────────────────────────────────────┘
```

### Interactions

1. Toggle monthly/yearly → prices update, savings badge appears on yearly
2. Click "Select" → redirect to Stripe Checkout (hosted page)
3. Stripe success → redirect to `/parent/subscribe/success`
4. Stripe cancel → redirect back to this page

### Success Screen (post-Stripe)

```
┌──────────────────────────────────────┐
│  🎉 "!ברוכים הבאים לתוכנית [שם]"    │
│                                       │
│  נועה יכולה להמשיך ללמוד בלי הפסקה!  │
│                                       │
│  [  → חזרה ללוח הבקרה  ]             │
└──────────────────────────────────────┘
```

---

## 3. Payment Failed Banner

**Task IDs:** R3 | **Appears on:** Parent dashboard

**Purpose:** Alert parent that payment failed, with clear action to fix it.

### Layout

```
┌──────────────────────────────────────┐
│  ⚠️ התשלום עבור תוכנית [שם] נכשל    │
│  הגישה ממשיכה עד DD/MM/YYYY.         │
│  [  עדכנו אמצעי תשלום →  ]          │
└──────────────────────────────────────┘
```

### States

| Attempt | Tone |
|---------|------|
| First failure | Neutral: "התשלום נכשל — עדכנו את אמצעי התשלום" |
| Second failure | Urgent: "ניסינו מספר פעמים — נא לעדכן בהקדם" |
| Grace period ending | Critical: red background, "הגישה תיפסק בעוד X ימים" |

### Interactions

- Click CTA → Stripe Customer Portal (update payment method)
- Dismiss banner → reappears next login until resolved

---

## 4. Stripe Checkout Integration Notes

**Not a custom screen** — uses Stripe's hosted Checkout.

### Configuration

- **Success URL:** `/parent/subscribe/success?session_id={CHECKOUT_SESSION_ID}`
- **Cancel URL:** `/parent/subscribe`
- **Products:** 4 plans (Basic Monthly, Basic Yearly, Premium Monthly, Premium Yearly)
- **Trial:** 7 days, no card required. After trial: prompt to subscribe.
- **Customer Portal:** handles payment method updates, billing history, plan changes
- **Webhooks to handle:** `checkout.session.completed`, `invoice.payment_failed`, `customer.subscription.updated`, `customer.subscription.deleted`
- **Currency:** ILS (Israeli New Shekel, ₪)
- **Locale:** Hebrew (`he`)
