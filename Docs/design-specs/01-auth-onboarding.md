# 01 — Auth & Onboarding

> **Screens:** 11 | **Users:** Parent, Child, Visitor
> **Related tasks:** D4, D19, D2, R2, P8

---

## 1. Child Login Page — EXISTING DESIGN

**Task IDs:** D19, R2, P8 | **User:** Child | **Route:** `/login`

**Purpose:** The kid's entry point. Game-style "Ready to Code?" screen — fun, not corporate.

### Enhancement Checklist (for existing Figma)

- [ ] Title: "?מוכנים למשימה" / "Ready To Code?"
- [ ] Username + password fields (Hebrew labels, RTL)
- [ ] Submit button — large, vibrant, game-style
- [ ] **States to verify:**
  - Default (empty fields)
  - Focused (field highlighted)
  - Filled (both fields have content)
  - Loading (submit pressed → spinner on button)
  - Error: wrong credentials → friendly message: "!אופס, משהו לא נכון — נסו שוב"
  - Error: account locked → "נסו שוב עוד כמה דקות"
  - Error: network failure → "אין חיבור לאינטרנט"
- [ ] "Forgot password? Ask your parent" link
- [ ] Transition: game-style swoosh/fade into quest map on success
- [ ] No "sign up" link (kids don't sign up — parents do)
- [ ] Keyboard: Enter submits the form
- [ ] Mobile: fields and button fill width, large touch targets (44px+)

---

## 2. Parent Signup Page

**Task IDs:** D19, R2 | **User:** Parent | **Route:** `/signup`

**Purpose:** Parent creates their account to manage their child's learning.

### Layout

```
┌─────────────────────────────────────┐
│  VRT Logo                            │
│  "הצטרפו ל-VRT — הילד שלכם ילמד     │
│   Python בכיף"                       │
├─────────────────────────────────────┤
│  שם מלא: [____________]             │
│  אימייל: [____________]             │
│  סיסמה:  [____________] 👁          │
│                                      │
│  Password strength: ████░░ בינונית   │
│                                      │
│  [  הירשמו — חינם  ]                │
│                                      │
│  ── או ──                            │
│  [ G  המשיכו עם Google ]            │
│                                      │
│  כבר יש לכם חשבון? התחברו            │
├─────────────────────────────────────┤
│  By signing up you agree to our      │
│  Terms of Service & Privacy Policy   │
└─────────────────────────────────────┘
```

### Components & States

| Component | States |
|-----------|--------|
| Name input | Empty, focused, filled, error (required) |
| Email input | Empty, focused, filled, error (invalid format), error (already registered) |
| Password input | Empty, focused, filled, show/hide toggle (eye icon) |
| Strength indicator | Weak (red), Medium (yellow), Strong (green) |
| Submit button | Default, hover, loading (spinner), disabled (form invalid) |
| Google OAuth button | Default, hover, loading |

### Interactions

- Submit → loading state → email verification page
- Google OAuth → Google popup → redirect to "add child" page
- "Already have account?" → login page
- Validation: real-time on blur (email format, password strength)

### Edge Cases

- Email already registered → "האימייל הזה כבר רשום. התחברו או אפסו סיסמה"
- Google account already linked → auto-login instead of signup
- Network failure → toast error
- Spam prevention → rate limit signups per IP

---

## 3. Email Verification Page

**Task IDs:** R2 | **User:** Parent | **Route:** `/verify-email`

**Purpose:** Prompt parent to check inbox after signup.

### Layout

```
┌─────────────────────────────────────┐
│  VRT Logo                            │
│                                      │
│  📧 בדקו את האימייל שלכם             │
│                                      │
│  שלחנו קישור אימות ל:                │
│  example@email.com                   │
│                                      │
│  [ שלחו שוב ]  (זמין בעוד 60 שניות) │
│                                      │
│  לא מוצאים? בדקו בתיקיית הספאם       │
└─────────────────────────────────────┘
```

### States

- Default: email displayed, resend disabled (60s cooldown timer)
- Timer expired: resend button enabled
- Resend clicked: "!נשלח שוב" toast, timer resets
- Verified (user clicks email link): redirect to success page

---

## 4. Email Verification Success

**Task IDs:** R2 | **User:** Parent | **Route:** `/verify-email/success`

### Layout

```
┌─────────────────────────────────────┐
│  ✅ האימייל אומת בהצלחה!             │
│                                      │
│  עכשיו הוסיפו את הילד/ה שלכם:       │
│                                      │
│  [  הוסיפו ילד/ה  →  ]              │
└─────────────────────────────────────┘
```

- Auto-redirect to "Add Child" after 3 seconds if no click

---

## 5. Parent Login Page

**Task IDs:** D19, R2 | **User:** Parent | **Route:** `/parent/login`

**Purpose:** Separate login for parents (different from child login).

### Layout

```
┌─────────────────────────────────────┐
│  VRT Logo                            │
│  "כניסת הורים"                       │
├─────────────────────────────────────┤
│  אימייל: [____________]             │
│  סיסמה:  [____________] 👁          │
│                                      │
│  □ זכרו אותי                         │
│                                      │
│  [  התחברו  ]                        │
│                                      │
│  ── או ──                            │
│  [ G  התחברו עם Google ]             │
│                                      │
│  שכחתם סיסמה?  |  אין לכם חשבון?     │
│                    הירשמו            │
└─────────────────────────────────────┘
```

### States

| Component | States |
|-----------|--------|
| Email input | Empty, focused, filled, error (not found) |
| Password input | Empty, focused, filled, error (wrong password), show/hide |
| Remember me | Unchecked (default), checked |
| Submit | Default, hover, loading, disabled |
| Error messages | "אימייל או סיסמה שגויים", "החשבון ננעל — נסו בעוד 15 דקות" |

### Interactions

- Submit → validate → redirect to parent dashboard
- "Forgot password?" → forgot password page
- "Sign up" → parent signup page
- Max 5 failed attempts → account lock (15 min)

---

## 6. Forgot Password Page

**Task IDs:** R2 | **User:** Parent | **Route:** `/forgot-password`

### Layout

```
┌─────────────────────────────────────┐
│  VRT Logo                            │
│  "שחזור סיסמה"                       │
├─────────────────────────────────────┤
│  הכניסו את האימייל שלכם ונשלח        │
│  קישור לאיפוס סיסמה:                │
│                                      │
│  אימייל: [____________]             │
│                                      │
│  [  שלחו קישור  ]                    │
│                                      │
│  ← חזרה להתחברות                     │
└─────────────────────────────────────┘
```

### States

- Submit → "Check your email" page (same as verification flow)
- Email not found → still show success (security — don't reveal registered emails)
- Rate limit: max 3 requests per hour

---

## 7. Set New Password Page

**Task IDs:** R2 | **User:** Parent | **Route:** `/reset-password?token=xxx`

### Layout

```
┌─────────────────────────────────────┐
│  "הגדירו סיסמה חדשה"                │
├─────────────────────────────────────┤
│  סיסמה חדשה:  [____________] 👁     │
│  אימות סיסמה: [____________] 👁     │
│                                      │
│  Password strength: ████░░ בינונית   │
│                                      │
│  [  שמרו סיסמה  ]                    │
└─────────────────────────────────────┘
```

### States

- Passwords don't match → "הסיסמאות לא תואמות"
- Token expired → "הקישור פג תוקף — בקשו קישור חדש" + CTA
- Success → "!הסיסמה שונתה בהצלחה" + redirect to login

---

## 8. Add Child Form

**Task IDs:** R2, P8 | **User:** Parent | **Route:** `/parent/add-child`

**Purpose:** Parent creates a child account under their profile.

### Layout

```
┌─────────────────────────────────────┐
│  "הוסיפו את הילד/ה שלכם"            │
├─────────────────────────────────────┤
│  שם משתמש (שם הילד/ה בפלטפורמה):    │
│  [____________] ✅ זמין!             │
│                                      │
│  שנת לידה: [ 2012 ▼ ]               │
│                                      │
│  סיסמה לילד/ה: [____________] 👁    │
│  (הילד/ה ישתמש/ה בזה כדי להתחבר)    │
│                                      │
│  [  הוסיפו  ]                        │
├─────────────────────────────────────┤
│  💡 הילד/ה יתחבר/ת עם שם המשתמש     │
│  והסיסמה שבחרתם. שמרו אותם!         │
└─────────────────────────────────────┘
```

### Components & States

| Component | States |
|-----------|--------|
| Username input | Empty, checking (spinner), available (✅ green), taken (❌ "כבר תפוס"), error (profanity filter, too short/long) |
| Birth year dropdown | Default, selected. Range: 2011-2016 (ages 10-15) |
| Password input | Empty, focused, filled, show/hide. Min 4 chars for kids |
| Submit | Default, hover, loading, disabled (validation fails) |

### Validation

- Username: 3-20 chars, letters/numbers only, no profanity, must be unique
- Check availability on blur (debounced 500ms)
- Birth year: required
- Password: min 4 characters (simple for kids)

### Edge Cases

- Parent already has max children (e.g., 5) → "הגעתם למספר המקסימלי של ילדים"
- Username check fails (network) → "לא הצלחנו לבדוק — נסו שוב"

---

## 9. Child Avatar Selection (First Login)

**Task IDs:** D2, D19, R11, P8 | **User:** Child | **Route:** `/onboarding/avatar`

**Purpose:** First thing the kid sees after first login — pick their character. Sets the tone: this is a game.

### Layout

```
┌──────────────────────────────────────────┐
│  "!בחרו את הדמות שלכם"                   │
│                                           │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐          │
│  │ 🧑 │ │ 👧 │ │ 🤖 │ │ 🦊 │ │ 🐱 │          │
│  │char│ │char│ │char│ │char│ │char│          │
│  │ 1  │ │ 2  │ │ 3  │ │ 4  │ │ 5  │          │
│  └───┘ └───┘ └───┘ └───┘ └───┘          │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐          │
│  │char│ │char│ │char│ │char│ │char│          │
│  │ 6  │ │ 7  │ │ 8  │ │ 9  │ │ 10 │          │
│  └───┘ └───┘ └───┘ └───┘ └───┘          │
│                                           │
│  Selected: [Large preview of chosen char] │
│  Name: "דמות X"                           │
│                                           │
│  [  !זה אני — קדימה  ]                   │
└──────────────────────────────────────────┘
```

### Components & States

| Component | States |
|-----------|--------|
| Character card (each) | Default (normal size, no border), Hover (slight enlarge + shadow), Selected (border + checkmark + enlarge) |
| Large preview | Shows selected character full-body, animated idle |
| Confirm button | Disabled (no selection), enabled (character selected), loading |

### Interactions

1. Click character → it becomes selected (deselects previous), large preview updates
2. Confirm → loading → avatar saved → success screen
3. Can change selection before confirming
4. No "skip" — avatar selection is required

### Edge Cases

- All characters loading → skeleton grid with shimmer
- Character images fail to load → fallback colored circles with initials
- Only shown on first login. After that, avatar changes happen in the shop.

---

## 10. Avatar Selection Success

**Task IDs:** P8 | **User:** Child

**Purpose:** Brief celebration after choosing avatar, then redirect to learning.

### Layout

```
┌─────────────────────────────────────┐
│  🎉 "!בחירה מעולה"                   │
│                                      │
│  [Large avatar with celebration      │
│   animation — confetti/sparkle]      │
│                                      │
│  "?מוכנים ללמוד לתכנת"               │
│                                      │
│  [  !קדימה — לשיעור הראשון  ]        │
└─────────────────────────────────────┘
```

- Auto-redirect to quest map after 4 seconds if no click
- Confetti animation plays on load

---

## 11. Parent Account Settings

**Task IDs:** R2, R12 | **User:** Parent | **Route:** `/parent/settings`

### Layout

```
┌─────────────────────────────────────┐
│  "הגדרות חשבון"                      │
├─────────────────────────────────────┤
│  אימייל: example@email.com ✅ מאומת │
│  [שנו סיסמה]                         │
│                                      │
│  ── הגבלת זמן יומית ──               │
│  [====●========] 2 שעות ביום         │
│  הילד/ה יראה הודעה כשהזמן נגמר       │
│                                      │
│  ── התראות ──                        │
│  □ דוח שבועי באימייל                  │
│  □ התראה על סיום תקופת ניסיון        │
│                                      │
│  ── מחיקת חשבון ──                   │
│  [מחקו את החשבון שלי] (red text)     │
└─────────────────────────────────────┘
```

### Components

- Time limit slider: 30min–6hrs, default 2hrs. Shows value in real-time.
- Notification toggles: on/off switches
- Delete account: confirmation modal with "type DELETE to confirm"
- Password change: opens inline form or modal (current password + new password)
