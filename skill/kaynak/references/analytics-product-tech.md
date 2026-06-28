# Analytics, Product & Tech Reference File

## Table of Contents
1. [Analytics & Reporting](#analytics--reporting)
2. [CFO / Finance](#cfo--finance)
3. [CEO / Product Manager](#ceo--product-manager)
4. [CTO / Chief Technology Officer](#cto--chief-technology-officer)
5. [Chief of Staff (CoS)](#chief-of-staff-cos)
6. [Intelligence / Intel](#intelligence--intel)
7. [Manager (Orchestrator)](#manager-orchestrator)

---

## Analytics & Reporting

**Command:** `/analytics` or `/analitik`  
**Role:** Cross-channel analytics — not just data, but decision-supporting insights.

### Modes

| Mode | Output |
|-----|-------|
| `/analitik onboard` | Tracking infrastructure setup plan |
| `/analitik kurulum` | GTM container structure + event taxonomy |
| `/analitik dashboard` | Executive / Channel / Operational dashboard templates |
| `/analitik attribution` | Last-touch vs data-driven comparison |
| `/analitik kampanya-rapor` | KPI vs target + root cause analysis + lessons learned |
| `/analitik aylik-rapor` | North Star + Tier 2 + channel + cohort + insight |
| `/analitik ab-test-analiz` | Statistical significance + p-value + decision |
| `/analitik cohort` | Retention heatmap + LTV by channel |
| `/analitik funnel` | Stage × conversion × drop-off points |
| `/analitik insight` | Hypothesis → data → validation → action |
| `/analitik denetim` | Data health score (tracking / completeness / consistency) |

### 3-Tier KPI Model
```
Tier 1 — North Star (1-3 metrics): MRR / GMV / ARR
Tier 2 — Business Health (5-10): CAC / LTV / Churn / NRR
Tier 3 — Operational (20-50): Channel × campaign metrics
```

### Attribution Models (Recommended Priority)
1. **Data-driven** (GA4 ML) — most accurate, requires 300+ conversions/month
2. **Time-decay** — default recommendation
3. **Last-touch** — for legacy comparisons
4. **First-touch** — for awareness visibility

### Monthly Report Format
```
# Monthly Report: {month}
## Executive Summary (1 paragraph, for the CEO)
## North Star
## Tier 2 KPI Table (This Month / Last Month / %Δ / Target / Status)
## Acquisition Analysis
## Channel Performance
## A/B Test Results
## Cohort Analysis
## Insights (3 key findings)
## Next Month Plan
## Risks
## ROI Summary
## Action List (owner + deadline)
```

---

## CFO / Finance

**Command:** `/cfo`  
**Role:** Financial health — MRR, unit economics, runway, pricing, billing.

### Modes

| Mode | Output |
|-----|-------|
| `/cfo mrr` | MRR movement (new/expansion/churn/contraction) + NRR |
| `/cfo birim-ekonomi` | CAC / LTV / LTV:CAC / Payback / Gross Margin |
| `/cfo runway` | Burn rate + runway + 4 scenario models |
| `/cfo fiyat-analizi` | Conversion + churn + competitor + unit economics comparison |
| `/cfo faturalandirma` | Failed payment % + dunning recovery + privacy checklist |
| `/cfo cohort` | Revenue retention heatmap + LTV by channel |
| `/cfo p-and-l` | Revenue → COGS → Gross Profit → OpEx → EBITDA |
| `/cfo board-paketi` | Investor/board financial pack |

### Unit Economics Benchmarks (SaaS)
| Metric | Poor | Acceptable | Good | Excellent |
|--------|------|------------|------|-----------|
| LTV:CAC | <1 | 1-3 | 3-5 | 5+ |
| Payback | >24m | 12-24m | 6-12m | <6m |
| Gross Margin | <50% | 50-70% | 70-80% | 80%+ |
| MRR Churn | >5%/month | 2-5% | 1-2% | <1% |

### Runway Threshold Warnings
- < 6 months: 🔴 Time for shutdown decision
- < 12 months: 🟠 Start investment round
- < 18 months: 🟡 Plan next steps
- > 18 months: 🟢 Healthy

---

## CEO / Product Manager

**Command:** `/ceo`  
**Role:** Strategic lead — from product vision to investor pitches, north stars to decision support.

### Modes

| Mode | Output |
|-----|-------|
| `/ceo brief --tip=weekly/monthly/quarterly` | Strategy brief (data from Manager + business insights) |
| `/ceo pitch --sure=1m/5m/30m --kitle=yatirimci/musteri/ekip` | Duration × audience tailored pitch |
| `/ceo karar` | 3 scenarios + trade-offs + CEO recommendation (Type 1/2 analysis) |
| `/ceo metrik` | North star + funnel + unit economics + health dashboard |
| `/ceo rakip` | Strategic competitor profile (funding + product + market + SWOT) |
| `/ceo risk` | 5 category risk register (operational/market/legal/technical/financial) |
| `/ceo roadmap` | RICE prioritized roadmap + what we won't do section |
| `/ceo paydas` | Investor/team/customer/press communication templates |
| `/ceo org` | Agentic architecture audit — execution gap + new worker suggestions |

### 5-Minute Investor Pitch Structure
```
1. Problem (45s): Who experiences it, why is it big
2. Solution (45s): Single sentence + demo screenshot
3. Market (30s): TAM + timing
4. Traction (45s): Metrics + growth
5. Business Model (30s): Cash flow + unit economics
6. Competition (30s): Positioning matrix
7. Team (15s): Why them
8. The Ask (30s): How much, for what, milestones
```

---

## CTO / Chief Technology Officer

**Command:** `/cto`  
**Role:** Technology strategy — architectural decisions, technical debt, scale plans, vendor evaluation.

### Modes

| Mode | Output |
|-----|-------|
| `/cto altyapi-saglik` | Stack version × EOL × vendor health table |
| `/cto teknik-borc` | Debt inventory (impact × urgency × est. time) + 90-day payoff plan |
| `/cto scale-plani --hedef=10x/100x` | Bottleneck analysis + step-by-step scaling path |
| `/cto api-roadmap` | Public API strategy + versioning + SDKs + docs |
| `/cto mimari-karar` | ADR (Architecture Decision Record) document |
| `/cto build-vs-buy` | Build vs buy cost + TCO + decision |
| `/cto vendor-degerlendirme` | Current vendor health + alternative comparison |
| `/cto disaster-recovery` | RTO/RPO + scenario × recovery plan |

### ADR Format
```
# ADR-{NN}: {Decision Title}
Date / Status / Authors / Affected
## Context
## Decision
## Rationale
## Alternatives Evaluated
## Consequences (good + bad/trade-offs)
## Reversibility (Type 1 / Type 2)
```

### Technical Debt Score = Impact (1-5) × Urgency (1-5)
- 20-25: Urgent (40% of sprint)
- 12-19: This quarter
- 6-11: Backlog
- 1-5: Accepted debt

---

## Chief of Staff (CoS)

**Command:** `/cos`  
**Role:** Strategic discipline layer — alignment across CEO + 5 agent decisions, inter-brain consistency, OKR risk.

### Modes

| Mode | Output |
|-----|-------|
| `/cos sync` | Inter-brain conflict report (🔴 critical / 🟠 stale / 🟡 drift) |
| `/cos roadmap-takip` | CEO roadmap × actual progress table |
| `/cos karar-takip` | Decision lifecycle (proposed → accepted → active → completed) |
| `/cos action-items` | Action item pool across all briefs (owner + deadline + status) |
| `/cos haftalik-sync` | 1-pager for CEO: weekly summary of 5 agents + manager |
| `/cos eskalasyon` | Past-due / decision-blocked / OKR risk list |
| `/cos okr-checkpoint` | Quarter OKR progress + trend + at-risk OKRs |

### CoS Authority Limits
✅ Read access to all brains  
✅ Detect and report conflicts  
✅ Establish action item pool  
❌ Do not write or change brain models  
❌ Do not make decisions (CEO does)  
❌ Do not trigger production workflows  

---

## Intelligence / Intel

**Command:** `/intel`  
**Role:** External radar — competitor moves, market trends, opportunities/threats.

### Modes

| Mode | Output |
|-----|-------|
| `/intel rakip-monitor` | Weekly competitor moves (funding/product/team/pricing/market) |
| `/intel rakip-derin` | Funding + product + customers + trajectory + SWOT |
| `/intel hareket-uyari` | Significant moves in last 30 days + impact on CEO |
| `/intel pazar-trend` | Rising/falling/plateau trends |
| `/intel firsat` | Detected opportunities (regulation/niche/competitor weakness) |
| `/intel pazar-haritasi` | Segment × player × market share + white space |
| `/intel cikti-radar` | Weekly top 5 takeaways (3-minute CEO briefing) |
| `/intel ekip-monitor` | Competitor LinkedIn + open roles growth analysis |

### News Category Severity
| Category | Trigger |
|----------|---------|
| 💰 Funding | Round announcement, acquisition |
| 🚀 Product | Major launch, breaking change |
| 👥 Team | C-level change, key hire |
| 💸 Pricing | Plan/limit change |
| 🌍 Market | New geography/segment |

### Intel → CEO Bridge
- For each finding: data → **"Impact on Us"** section is mandatory
- Speculative remarks: marked as **"Hypothesis"**
- Sources for all claims: link + date + author

---

## Manager (Orchestrator)

**Command:** `/mudur` or `/manager`  
**Role:** Orchestrates all workflows, reads outputs, prepares high-level management briefs, suggests new workers on pattern detection.

### Operating Modes
| Mode | Scope |
|-----|--------|
| `weekly` | Full cycle — all sub-workflows → brief |
| `read-only` | Collect latest reports only |
| `incident` | Urgent: bugs + site-health + security |
| `pre-launch` | Launch focused: launch-readiness + load-testing + user-flow |

### Sub-Workflows
`/site-saglik` / `/bug-tarama` / `/guvenlik-kontrolu` / `/seo-altyapisi` / `/temizlik` / `/kullanici-akisi` / `/yuk-testi` / `/lansman-hazirlik`

### Findings Severity
| Severity | Definition |
|--------|-------|
| 🚨 FIRE | Users affected in production |
| 🔥 BLOCKER | Postpones launch date if not resolved |
| ⚠️ RISK | Might affect soon |
| 📌 ATTENTION | Important but not urgent |
| 📋 INFO | For trace logs |

### Weekly Brief Format
```
# Weekly Brief — Week {WW}
> Launch countdown: {X days} remaining

## 🚦 General Status (single sentence)
## 🔥 Launch Blockers
## 🚨 Fire (urgent)
## ⚠️ Risk (within this week)
## 📌 Attention (2-4 weeks)
## 📋 Good News
## 📈 Trend (3-week ASCII chart)
## 🤖 New Worker Suggestion? (if patterns detected)
## 🎯 Top 3 Focuses for This Week
```
