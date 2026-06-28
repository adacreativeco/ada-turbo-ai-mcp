# Marketing & Growth Reference File

## Table of Contents
1. [Performance Marketing](#performance-marketing)
2. [SEO](#seo)
3. [Email & CRM Marketing](#email--crm-marketing)
4. [Growth Hacker](#growth-hacker)
5. [Social Media Manager](#social-media-manager)
6. [Content Strategist](#content-strategist)
7. [Influencer & Partnership](#influencer--partnership)
8. [Media Planning & Buying](#media-planning--buying)

---

## Performance Marketing

**Command:** `/performance` or `/performans`  
**Role:** Paid acquisition — Google/Meta/LinkedIn/TikTok self-serve channels, ROAS/CPA optimization.

### Core Framework
- **Acquisition:** Paid traffic → landing page
- **Metrics:** ROAS, CPA, CAC, CTR, CPM
- **Tools:** Google Ads, Meta Ads Manager, LinkedIn Campaign Manager, TikTok Ads

### Campaign Report Format
```
# Campaign Report: {campaign}
## KPI Results (Target vs Actual table)
## Why We Failed/Succeeded (hypotheses)
## Channel × Performance (Spend / Conversion / CPA / ROAS)
## Creative × Performance (Top 3 + Bottom 3)
## Audience × Performance
## Time × Performance
## Lessons Learned
## For the Next Campaign
## ROI Re-Analysis (with multi-touch attribution)
```

---

## SEO

**Command:** `/seo-altyapisi` or `/seo`  
**Role:** Technical SEO infrastructure — pre-launch/post-launch checks, indexing, structured data, Core Web Vitals.

### Pre-launch Checklist
- robots.txt + sitemap.xml
- Structured data (JSON-LD) — schema type × page type
- Title + meta description uniqueness
- Open Graph + Twitter Card
- Image alt text + format (WebP/AVIF)
- Core Web Vitals (LCP <2.5s, INP <200ms, CLS <0.1)
- Google Search Console + Bing Webmaster verification
- IndexNow integration
- **Launch blocker:** Is noindex removed?

### Classification
| Class | Criteria |
|-------|--------|
| 🔴 Blocker | robots Disallow:/, sitemap broken, 50%+ canonical errors |
| 🟠 High | Title/desc duplicate 20%+, alt text 50%+ missing |
| 🟡 Medium | Internal linking, breadcrumb missing |

---

## Email & CRM Marketing

**Command:** `/email`  
**Role:** Lifecycle marketing — from welcome to win-back, newsletter to transactional. Owned channel = list ownership.

### Sequence Types
| Sequence | Goal | Length |
|---------|-------|---------|
| Welcome | Lead to first value activation | 5-7 emails |
| Nurture | Lead → customer | 8-12 emails, 4-6 weeks |
| Abandoned | Cart/form recovery | 3 emails |
| Post-purchase | Retention + cross-sell | 5-6 emails |
| Win-back | Re-activate dormant | 4 emails |

### Deliverability Requirements
- SPF + DKIM + DMARC (p=quarantine minimum)
- Mail-Tester.com ≥ 9/10
- Bounce rate < 2%, Spam complaint < 0.1%
- Warm-up: start 14 days before launch

### Welcome Sequence (SaaS Example)
```
Email 1 (Immediate): Welcome + first action CTA
Email 2 (Day 1): Positive reinforcement + power feature
Email 3 (Day 3): Use case / customer story
Email 4 (Day 5): Help is here (support + docs)
Email 5 (Day 7): Select plan (if trial is ending)
```

### GDPR / Privacy Requirements
- Double opt-in (pre-checked boxes banned)
- Unsubscribe link in footer
- Physical address in footer
- Data subject rights request channel

---

## Growth Hacker

**Command:** `/growth`  
**Role:** AARRR funnel optimization — data-driven experiments, ICE scoring, A/B test discipline.

### AARRR Funnel
```
Acquisition → Activation → Retention → Revenue → Referral
```

### ICE Score
```
Impact (1-10) × Confidence (1-10) × Ease (1-10) / 3
ICE > 7 → ship-worthy
```

### Experiment Brief Template
```
Hypothesis: "If we do X, then Y metric will lift by Z%, because..."
Variant A (Control): ...
Variant B (Test): ...
Sample size: N/variant (95% confidence)
Duration: minimum 1 week
Primary metric: ...
Guardrail: ...
Decision criteria: p < 0.05 + +5pp minimum lift
```

### 90-Day Pipeline Structure
- Month 1: Activation sprint (weakest link)
- Month 2: Retention sprint
- Month 3: Revenue/Referral sprint

---

## Social Media Manager

**Command:** `/social` or `/sosyal`  
**Role:** Organic social — broadcast (posts) + conversation (comments/DMs/mentions).

### Platform Roles
| Platform | Primary Role | Format Mix |
|----------|-------------|------------|
| Instagram | Brand awareness + product | Reels 40%, carousels 30%, daily stories |
| LinkedIn | Authority + B2B | Text 40%, CEO insights 30%, carousels 20% |
| TikTok | Discovery + youth | Trends 40%, educational 30%, BTS 20% |
| YouTube | Deep content + SEO | Tutorials 30%, shorts 30%, reviews 20% |
| X/Twitter | Conversation + fast reaction | Replies 50%, threads 25% |

### Community Response Times (SLA)
| Type | Target |
|-----|-------|
| DM new | < 2 hours (business hours) |
| Comment | < 2 hours |
| Customer complaint | < 30 minutes |
| Crisis/viral negative | < 15 minutes → Escalation to Crisis Comm |

### Content Pillar Distribution
- Education/value: 30-40%
- BTS/humanization: 20-25%
- Social proof/customer success: 15-20%
- Promo: max 15-20% (more feels spammy)

### Trend Watch (Daily)
TikTok Discover + X trending + Google Trends TR  
→ Evaluation: Brand aligned? Still active? Quick to build? Any risks?

---

## Content Strategist

**Command:** `/content` or `/icerik`  
**Role:** Long-term editorial system — pillars, calendar, atomization, thought leadership.

### Good Pillar Criteria
- Serves persona's actual pain points
- Brand's exclusive authority area
- Distinct angle from competitors
- 50+ content pieces can be generated
- Relevant even 5 years from now

### Atomization Chain
```
1 Tentpole (whitepaper/60m video/podcast)
→ 3-5 blog posts (chapter-based)
→ 3-5 videos (YouTube)
→ 1 LinkedIn carousel
→ 1 Twitter thread
→ 3 newsletter issues
→ 5+ Shorts/Reels
→ 1 webinar
→ 1 email nurture sequence
```

### Monthly Rhythm
- Weekly: 1-2 blog posts + newsletter + social distribution
- Monthly: 1 cornerstone piece (whitepaper/video series)
- Quarterly: 1 major campaign content package

---

## Influencer & Partnership

**Command:** `/influencer`  
**Role:** Discovery → vetting → contract → brief → performance tracking.

### Creator Tiers (TR/Global)
| Tier | Followers | Avg Fee (TR) | Engagement |
|------|-----------|--------------|------------|
| Nano | <10K | ₺500-3K | 5-10% |
| Micro | 10K-100K | ₺3K-25K | 3-7% |
| Mid | 100K-500K | ₺25K-100K | 2-5% |
| Macro | 500K-1M | ₺100K-300K | 1-3% |
| Mega | 1M+ | ₺300K-2M+ | 0.5-2% |

### Vetting Criteria (HypeAuditor)
- Bot ratio < 5%
- Audience Quality Score > 70
- Persona demographic fit > 70%
- Sponsorship saturation < 20%

### Legal & Regulatory
- Data Protection (KVKK/GDPR): In contract
- Ad declaration: #sponsored / #ad at start of caption
- Pre-publish brand approval required
- Model release signed

### Crisis Protocol (Creator Scandal)
🔴 → Pause all active content + alert Crisis Comm  
Push notifications off, observe.

---

## Media Planning & Buying

**Command:** `/media` or `/medya`  
**Role:** Reservation-based media — TV, OOH, print, programmatic, cinema, podcast sponsorship.

### Channel Roles Matrix
| Role | Channel | Budget Weight |
|-----|-------|---------------|
| Reach | TV, OOH, YouTube | 35-50% |
| Engage | Meta, TikTok organic boost | 20-30% |
| Convert | Google Search, retargeting | 15-20% |
| Retain/Advocate | Email, influencer | 5-10% |

### OOH Formats (TR)
Billboard, bus stop shelter, metro station, in-mall digital, DOOH (programmatic), taxi top, elevator screens

### Programmatic DSPs
- DV360 (Google): display + video + YouTube reach
- The Trade Desk: premium web + CTV
- DOOH: Vistar Media, Broadsign

### Negotiation Lever Cards
- Annual volume commitment → AVB 5-15% discount
- Combo packaging → position optimization
- Fast payment → extra cash discount
