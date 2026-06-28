# Client Relations & Operations Reference File

## Table of Contents
1. [Account Manager](#account-manager)
2. [Project Manager](#project-manager)
3. [Customer Success (CS)](#customer-success-cs)
4. [Crisis Communication](#crisis-communication)
5. [PR & Corporate Communication](#pr--corporate-communication)

---

## Account Manager

**Command:** `/account` or `/hesap`  
**Role:** Client × agency bridge. Advocate of the client inside, advocate of the agency outside.

### Modes

| Mode | Output |
|-----|-------|
| `/hesap brief-al` | 20 questions → approved written brief |
| `/hesap brief-tanitla` | Internal team brief (deliverable table + timeline + budget + risk) |
| `/hesap onay-sureci` | Presentation format + revision management |
| `/hesap toplanti --tip=kickoff/weekly/QBR` | Agenda + notes + action items template |
| `/hesap status` | Weekly status report (✅ completed / 🚧 ongoing / ⏳ waiting on you) |
| `/hesap eskalasyon` | Tier 1-4 escalation document |
| `/hesap qbr` | 90m QBR agenda + customer relationship question set |
| `/hesap fatura` | Monthly invoice summary + payment tracking |
| `/hesap genisleme` | Upsell/cross-sell pitch document |
| `/hesap yenileme` | T-3 months renewal pitch process |
| `/hesap memnuniyet` | Health score (NPS + payment + communication + revisions + team dynamics) |

### Brief Mandatory 5 Questions
1. **Why now?** (trigger)
2. **Goal — what is the quantitative target?** (measurable)
3. **Who exactly is the target audience?**
4. **How is success defined?**
5. **Who can say no?** (decision-maker)

### Revision Management
- Standard contract: 2 rounds of revisions included
- 3+: out of scope, requires written approval + extra invoice
- "Make it more modern" → **"What do you mean by modern? Which references?"** — crystallize abstract feedback

### Client Health Score
```
NPS: 0-10
Payment status: 0-10 (on time?)
Communication activity: 0-10
Approval speed: 0-10
Number of revisions: 0-10 (less = better)
Team dynamics: 0-10

Total / 6 → /10
8.5+: Green | 7-8.5: Yellow | 5-7: Orange | <5: Red
```

---

## Project Manager

**Command:** `/project` or `/proje`  
**Role:** Internal team operations — timeline, capacity, risk, task tracking. They don't say "yes", they give realistic commitments.

### Modes

| Mode | Output |
|-----|-------|
| `/proje plan` | Week-by-week phase → milestone → deliverable schedule |
| `/proje kapasite` | Team × hours allocation + overload warning |
| `/proje gorev` | SMART task cards (title + owner + deadline + acceptance criteria) |
| `/proje stand-up` | Yesterday/today/blocker format |
| `/proje risk` | Risk register (probability × impact × mitigation) |
| `/proje status` | 🟢🟡🔴 health + timeline + budget + progress report |
| `/proje retro` | Keep/Stop/Start + action items |
| `/proje porfoy` | Active projects portfolio table |

### Capacity Thresholds
- <60%: Underutilized
- 60-80%: **Ideal**
- 80-95%: Tight, pay attention
- 95-110%: Overload risk
- 110%+: Inevitable fail

### Timeline Phase Template (Campaign)
```
Weeks 1-2: Strategy + Brief
Week 3: Concept approval
Weeks 4-6: Production
Week 7: Review + Revision
Week 8: Launch
Weeks 9-12: Post-launch + Reporting
```

### Risk Score = Probability (1-5) × Impact (1-5)
- 15-25: 🔴 Critical
- 9-14: 🟠 High
- 5-8: 🟡 Medium
- 1-4: 🟢 Low

---

## Customer Success (CS)

**Command:** `/cs`  
**Role:** Existing customer/user health — onboarding tracking, churn early warning, NPS, expansion.

### Health Score Model
| Signal | Weight |
|--------|---------|
| Login/usage frequency | 15% |
| Core feature usage | 25% |
| Onboarding completion | 15% |
| Support ticket sentiment | 10% |
| Payment status | 15% |
| Latest NPS score | 10% |
| Team seats usage | 10% |

Total 0-100:
- 80+: 🟢 Healthy
- 60-79: 🟡 Under observation
- 40-59: 🟠 Risk
- <40: 🔴 Critical

### Modes

| Mode | Output |
|-----|-------|
| `/cs saglik` | Total tenant health table |
| `/cs kiraci` | Single tenant profile (history + ticket + risk hypothesis) |
| `/cs onboarding-takip` | First 30 days bottleneck points + intervention |
| `/cs churn-uyari` | Risk tier × intervention matrix |
| `/cs nps` | NPS segment + detractor follow-up |
| `/cs expansion` | Upsell candidate list (limit 80%+, strong usage, growth signal) |
| `/cs save-call` | Churn risk call brief (questions + ready answers + limits) |
| `/cs qbr` | Quarterly business review for ₺50K+ tenants |

### Churn Intervention Tiers
| Annual Value | Intervention |
|-------------|----------|
| ≥ ₺50K | Personal save call + executive sponsor |
| ₺10K-50K | Personal save call |
| ₺2K-10K | Automated save email + optional call |
| < ₺2K | Automated sequence |

---

## Crisis Communication

**Command:** `/crisis` or `/kriz`  
**Role:** Before crisis (playbook), during crisis (firefighting), after crisis (lessons learned).

### Time Standards
- **T+30 m:** Holding statement live
- **T+4 hours:** Full response statement live
- **T+1 hour:** Tier 1 stakeholders informed
- **T+7 days:** Post-mortem completed

### Risk Matrix Categories
Operational / Human-caused / Reputational / Regulatory / External factor

Score = Probability (1-5) × Impact (1-5)  
13-25: 🔴 Critical → playbook mandatory  
8-12: 🟠 High → playbook required  

### Holding Statement Template
```
Regarding the {topic} that occurred today at {time},
{Client} is currently investigating the situation.
We are reaching out directly to affected parties.
We will share more information within {timeframe}.
```

### Full Response Structure
```
1. Opening (what happened)
2. What we did (immediate actions)
3. What we are doing (ongoing actions)
4. Steps for affected parties
5. Prevention (future steps)
6. Accountability (if appropriate)
7. Next update date/time
```

### Tone Rules
✅ Transparent / Human / Empathetic / Accountable / Action-oriented  
❌ Passive voice / "Alleged" / "Some individuals" / Blaming others / Speculation

### Modes

| Mode | Output |
|-----|-------|
| `/kriz risk-haritasi` | Scenario × probability × impact matrix |
| `/kriz oyun-kitabi` | Scenario-specific T+0 → T+72 protocol |
| `/kriz simulasyon` | Tabletop exercise brief (2-3 hours) |
| `/kriz alarm` | ACTIVE CRISIS — rapid start of 3 parallel workflows |
| `/kriz holding-statement` | Temporary holding statement output within 30 mins |
| `/kriz tam-yanit` | Detailed response statement document at T+4h |
| `/kriz stakeholder-map` | Tier 1-4 notification chain |
| `/kriz medya-brief` | Spokesperson brief (core messages + Q&A + don'ts) |
| `/kriz sosyal-yanit` | Platform × response package + template replies |
| `/kriz post-mortem` | Timeline + impact + lessons learned + action items |

---

## PR & Corporate Communication

**Command:** `/pr`  
**Role:** PR workflows operate under the `/pr` command in this system. Core outputs:

### Core Modes
| Mode | Output |
|-----|-------|
| `/pr basin-listesi` | Sector journalists + publication + podcast list |
| `/pr basin-bulteni` | 5W + quote + boilerplate format |
| `/pr medya-kiti` | Company summary + assets + key facts + contact |
| `/pr sozcü-brief` | Message core + Q&A + bridging techniques |
| `/pr thought-leadership` | Editorial article + interview + speaking topics |
| `/pr kriz-pr` | Press response coordinated with Crisis Comm |

### Press Release Structure
```
Title: Action-oriented (verb + result)
Subtitle: Context
Lead paragraph: 5Ws in a single paragraph
Body: 3-4 paragraphs (details + quotes + proof points)
Boilerplate: Standard "About Company" text
Contact: Name + email + phone
```
