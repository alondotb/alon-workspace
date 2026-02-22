# VRT — Market Research Plan

> **Purpose:** Structured plan for M1 (Market Research). Covers competitive analysis, parent interviews, pricing validation, and key hypotheses.
> **Owner:** Alon (Marketer role)
> **Timeline:** Phase 0 (Weeks 1-3)
> **Last updated:** 2026-02-17

---

## 1. Research Objectives

Answer these questions before writing a single line of marketing copy:

1. **Do Israeli parents of 10-14 year olds want their kids to learn coding?** (demand validation)
2. **What do they currently use, and what frustrates them?** (competitive gaps)
3. **Will they pay 55-75 NIS/month for a gamified coding platform in Hebrew?** (pricing validation)
4. **What's the "language" parents use when talking about coding education?** (messaging fuel)
5. **Do kids in this age group respond to gamification + self-paced learning?** (product-market fit signal)

---

## 2. Competitive Analysis Framework

### Who to Analyze

| Tier | Platform | Why |
|------|----------|-----|
| **Direct competitors** | CodeCombat, Tynker | Gamified coding, closest to VRT's model |
| **Adjacent competitors** | Scratch, Code.org | Free, widely used, kids start here |
| **Aspirational** | Codecademy, Brilliant | Subscription learning at scale |
| **Israeli market** | CampusIL, Codemonkey, Gvahim programs | What's actually available in Hebrew |
| **General edtech** | Duolingo, Khan Academy | Gamification + self-paced learning leaders |

### Analysis Template (Per Competitor)

For each competitor, document:

```
## [Platform Name]

### Overview
- Website:
- Target age:
- Languages taught:
- Available in Hebrew: Yes/No
- Pricing:

### Product
- Learning format: (video, interactive, text, game)
- Self-paced or teacher-led:
- Gamification elements:
- Parent features:
- Mobile app: Yes/No

### Strengths
- (3-5 bullet points)

### Weaknesses
- (3-5 bullet points)

### Pricing Details
- Free tier:
- Paid plans:
- Trial:

### Visual Identity
- Look and feel:
- Target demographic signaling:

### Market Position
- Who are they for:
- Key differentiator:

### VRT Opportunity
- What we do better:
- What we can learn from them:
```

### Key Comparison Dimensions

| Dimension | What to Compare |
|-----------|----------------|
| Hebrew support | Is content natively Hebrew or translated? UI in Hebrew? |
| Age targeting | Do they have age-specific content for 10-14? |
| Gamification depth | XP, currency, avatars, achievements — or just badges? |
| Parent involvement | Dashboard? Progress reports? Time limits? |
| Self-paced viability | Can a kid actually progress alone without a teacher? |
| Pricing (NIS) | Convert all prices to NIS for apples-to-apples comparison |
| Content quality | Engaging or boring? Game-feel or homework-feel? |
| Code execution | Browser-based? Sandbox? Download required? |

### Deliverable
A comparison table + write-up saved to `~/Desktop/Alon-Workspace/Docs/competitive-analysis.md`

---

## 3. Parent Interview Guide

### Target
- **10-20 Israeli parents** of children aged 10-14
- Mix of: parents whose kids already code + parents who are interested but haven't started
- Recruit via: personal network, parenting Facebook groups (Israeli), WhatsApp groups, local community

### Recruitment Message (Hebrew)

> שלום! אני עלון, מייסד סטארטאפ חינוכי שמלמד ילדים בגילאי 10-14 תכנות בעברית דרך משחקים. אני מחפש הורים לשיחה קצרה (15-20 דקות) כדי להבין מה חשוב לכם בחינוך טכנולוגי לילדים. אשמח לשמוע ממך! 🙏

### Interview Structure (15-20 minutes)

#### Opening (2 min)
- Thank them for their time
- Explain: "I'm building a coding education platform for kids. I want to understand what matters to parents. No sales pitch — just listening."
- Ask permission to take notes

#### Section A: Background (3 min)
1. How old is your child/children?
2. Does your child show interest in technology/computers/gaming?
3. Has your child tried learning to code before? If so, what did they use?

#### Section B: Pain Points (5 min)
4. What's the biggest challenge with your child's tech education right now?
5. If your child tried coding before — what worked? What didn't?
6. What would make you feel confident that a platform is actually teaching your child real skills?
7. How important is it that the content is in Hebrew?

#### Section C: Product Concept (5 min)
*Briefly describe VRT: "A platform where kids learn Python by playing a game — they progress through a quest map, earn XP and coins, customize an avatar, and solve coding challenges. All in Hebrew, self-paced, no teacher needed."*

8. What's your initial reaction to this?
9. Would your child be excited about this? Why or why not?
10. What would worry you about your child using this platform?
11. What would make you feel good about it?

#### Section D: Pricing (3 min)
12. Do you currently pay for any educational services for your child? (How much per month?)
13. If a platform like this existed and your child loved it — would you pay 55 NIS/month? What about 75 NIS/month for a version with video lessons?
14. How important is a free trial before paying?

#### Section E: Wrap-up (2 min)
15. Is there anything else you'd want in a coding platform for your child?
16. Would you be interested in being a beta tester when we launch?
17. Can I follow up with you in a few weeks?

### Data Collection Template

For each interview, record:

| Field | Value |
|-------|-------|
| Parent name | |
| Child age(s) | |
| Date | |
| Prior coding experience | |
| Key pain points | |
| Reaction to VRT concept | |
| Price sensitivity (55/75 NIS) | |
| Hebrew importance (1-5) | |
| Would beta test | Y/N |
| Top quote | |
| Follow-up allowed | Y/N |

### Interview Targets

| Segment | Count | Why |
|---------|-------|-----|
| Parents with coding-experienced kids | 5-7 | Understand what's broken with current options |
| Parents of gaming-interested kids (no coding) | 5-7 | Understand the untapped market |
| Parents of girls 10-14 | 3-5 specifically | Understand gender-specific concerns/interest |
| Tech-savvy parents | 3-5 | They'll have stronger opinions on product quality |
| Non-tech parents | 3-5 | Understand the "trusting a platform I can't evaluate" angle |

---

## 4. Pricing Validation Approach

### What We're Testing

| Hypothesis | How to Test |
|-----------|-------------|
| Parents will pay 55 NIS/month for Basic | Direct question in interviews + landing page test |
| Parents will pay 75 NIS/month for Premium (with video) | Direct question + follow-up "would video matter?" |
| Yearly discount (450/600 NIS) increases conversion | Ask: "Would you commit to a year if it saved 2 months?" |
| No-credit-card trial increases signup rate | Ask: "Would you try it free for 7 days?" |
| Parents compare to tutoring prices (~150-250 NIS/hr) | Ask: "What do you currently spend on educational services?" |

### Van Westendorp Price Sensitivity Method

Ask these 4 questions (in the interview or a follow-up survey):

1. **Too cheap** — "At what price would you start to question the quality of this platform?" → ___ NIS/month
2. **Cheap / good deal** — "At what price would you feel this is a great deal?" → ___ NIS/month
3. **Getting expensive** — "At what price would you start to hesitate?" → ___ NIS/month
4. **Too expensive** — "At what price would you definitely not buy it?" → ___ NIS/month

Plot the results to find the optimal price range.

### Landing Page Price Test (Optional)

- Create a "coming soon" page with pricing displayed
- A/B test two price points (e.g., 49 NIS vs 59 NIS for Basic)
- Measure: which price gets more email signups?
- This is a behavioral signal, not just stated preference

---

## 5. Key Hypotheses to Test

| # | Hypothesis | Evidence Needed | How to Test |
|---|-----------|-----------------|-------------|
| H1 | Israeli parents are willing to pay for a Hebrew coding platform for kids | 60%+ of interviewed parents say yes at 55 NIS | Parent interviews (Q12-Q13) |
| H2 | Video lessons justify a premium price | 50%+ say they'd pay more for video | Parent interviews (Q13) |
| H3 | Gamification is more appealing than traditional coding courses | Positive reaction to game elements vs neutral/negative to alternatives | Parent interviews (Q8-Q9) |
| H4 | Hebrew language is a strong differentiator | 70%+ rate Hebrew as 4-5/5 importance | Parent interviews (Q7) |
| H5 | Self-paced is preferred over teacher-led for this age group | Parents express positive reaction to "no teacher needed" | Parent interviews (Q8, Q11) |
| H6 | Parents' biggest concern is screen time, not content quality | Screen time / addiction concern appears in top 3 worries | Parent interviews (Q10) |
| H7 | Current coding options for Israeli kids are inadequate | 60%+ of "tried before" parents report dissatisfaction | Parent interviews (Q5) |
| H8 | Parents benchmark against tutoring prices, not app prices | Average current spend > 100 NIS/month on education | Parent interviews (Q12) |

### Success Criteria

| Signal | Green (Go) | Yellow (Iterate) | Red (Pivot) |
|--------|-----------|-------------------|-------------|
| Interest in concept | 80%+ positive reaction | 60-80% positive | < 60% positive |
| Willingness to pay 55 NIS | 60%+ would pay | 40-60% would pay | < 40% would pay |
| Hebrew importance | 70%+ rate 4-5/5 | 50-70% rate 4-5/5 | < 50% |
| Self-paced acceptance | 70%+ see it as positive | 50-70% | < 50% want teacher |
| Beta interest | 50%+ want to beta test | 30-50% | < 30% |

---

## 6. Research Timeline

| Week | Activity | Deliverable |
|------|----------|-------------|
| Week 1 | Competitive analysis (desk research) | `competitive-analysis.md` |
| Week 1 | Draft interview guide (this doc), recruit first 5 parents | Confirmed interview slots |
| Week 2 | Conduct 10-15 parent interviews | Interview notes |
| Week 2 | Set up "coming soon" landing page | Live page with email capture |
| Week 3 | Conduct remaining 5 interviews | Complete interview set |
| Week 3 | Synthesize findings, update hypotheses | `research-findings.md` |
| Week 3 | Validate/adjust pricing based on data | Update pricing in `product-decisions.md` if needed |

---

## 7. Tools & Channels for Recruitment

| Channel | How to Use | Expected Yield |
|---------|-----------|----------------|
| **Personal network** | Direct asks to parents you know | 3-5 interviews |
| **Facebook groups** | Israeli parenting groups (הורים של ילדים, etc.) | 5-8 interviews |
| **WhatsApp groups** | School parent groups, community groups | 3-5 interviews |
| **Local community centers** | Post flyers or talk to program coordinators | 1-3 interviews |
| **LinkedIn** | Connect with Israeli tech parents | 2-3 interviews |

### Incentive
- No monetary incentive needed for 15-20 min interviews
- Offer: "Early access to the platform when it launches"
- If needed: 25 NIS Wolt gift card per interview

---

## 8. Output Files

| Deliverable | Location | When |
|-------------|----------|------|
| Competitive Analysis | `~/Desktop/Alon-Workspace/Docs/competitive-analysis.md` | End of Week 1 |
| Interview Notes (raw) | `~/Desktop/Alon-Workspace/Docs/research/interviews/` | Ongoing |
| Research Findings Summary | `~/Desktop/Alon-Workspace/Docs/research-findings.md` | End of Week 3 |
| Pricing Validation Results | Included in research findings | End of Week 3 |
| Hypothesis Score Card | Included in research findings | End of Week 3 |
