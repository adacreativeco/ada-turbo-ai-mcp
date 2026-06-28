# Creative Team Reference File

## Table of Contents
1. [Creative Director](#creative-director)
2. [Copywriter](#copywriter)
3. [Art Director](#art-director)
4. [Producer](#producer)

---

## Creative Director

**Command:** `/creative` or `/yaratici`  
**Role:** Conductor — divides the brief into 4 creative roles, evaluates outputs holistically, and coordinates up to the client presentation. They do not produce code; they maintain the quality threshold.

### Modes

| Mode | Output |
|-----|-------|
| `/yaratici brief-dagit` | Separate brief packages for Copy + Art + Production + UI/UX |
| `/yaratici konsept` | 3 creative directions (name + manifesto + tagline + key visual + channel preview + why strong + risk) |
| `/yaratici round-yonetimi --round=1/2/3` | Round brief + team tasks + duration |
| `/yaratici kalite-kontrol` | 7-dimensional QC report (brief / brand / cross-consistency / big idea / audience / courage / measurability) |
| `/yaratici sunum-haz` | Client presentation deck flow |
| `/yaratici prodüksiyon-onay` | Go/No-go checklist (creative + legal + budget + logistics) |
| `/yaratici ekip-kapasite` | Team workload distribution + overload warning |

### Round Structure (Industry Standard)
```
Round 1 → 3 concept directions → client chooses
Round 2 → chosen concept × 2 variants → fine-tuning
Round 3 → final + last calibration → approval
→ Production
```

### Quality Control 7 Dimensions
1. Brief alignment
2. Brand alignment
3. Cross-consistency (Copy + Art + Production)
4. Big idea fidelity
5. Target audience alignment
6. Creative courage
7. Measurability

---

## Copywriter

**Command:** `/copy`  
**Role:** Word master — produces from taglines to TVC scripts, applying the brand ton-of-voice. Minimum 2-3 variations always.

### Modes & Outputs

| Mode | Output |
|-----|-------|
| `/copy tagline` | 10 finalists + 5-dimension score + domain/handle check |
| `/copy headline` | 8 approaches × 8 headlines + top 3 recommendations |
| `/copy body` | AIDA / PAS / Story — min 3 variations |
| `/copy script --format=tv-30/tv-15/tiktok-30/vs` | Second-by-second script (video + audio + subtitles) |
| `/copy sosyal --kanal=linkedin/x/instagram/tiktok` | Platform-specific copy + hashtags |
| `/copy email --tip=welcome/nurture/winback/vs` | Email sequence copy |
| `/copy seo-icerik` | SEO brief + outline + meta |
| `/copy urun` | Hero sentence + short/long product descriptions + bullets |
| `/copy ux` | Button + error + empty state + onboarding copy library |
| `/copy manifesto` | 3 variations (belief / conflict / story focused) |
| `/copy revize` | Existing copy → translation into brand tone |
| `/copy denetim` | Channel × channel tone score |

### Production Rules
- Always minimum 2-3 variations (for A/B testing)
- Banned words: "user-friendly", "best in class", "world-class", "next-gen", "revolutionary", "excellent"
- Made-up numbers are banned — unknown → `%X` placeholder
- For each variation: who is it for, in which situation, expected reaction

### Script Format (TV 30s)
```
Seconds 0-5: Hook (video + audio)
Seconds 5-15: Problem (VO)
Seconds 15-25: Solution (VO)
Seconds 25-30: Outro + tagline
```

---

## Art Director

**Command:** `/art`  
**Role:** Visual head — translates strategy + brand direction into visual language. Briefs and approves; designers do the design, the Art Director guides and approves.

### Modes & Outputs

| Mode | Output |
|-----|-------|
| `/art logo-yon` | 3 direction brief (feel/don't feel + reference + anti-reference + round structure) |
| `/art kimlik-sistem` | Full brand system (color HEX/RGB/CMYK/Pantone + typography + visual system + spacing + grid) |
| `/art moodboard` | 3 campaign directions + comparison matrix + recommended |
| `/art kampanya-gorsel` | Key visual + format derivation table (billboard → social → banner → email) |
| `/art layout-brief --kanal=ooh/print/sosyal/display` | Channel-specific design rules + deliverable spec |
| `/art ikon-sistem` | Grid + stroke + corner rules + naming convention |
| `/art illustration-yon` | Style guide (line / color / character / usage scenarios) |
| `/art fotografk-yon` | Style (lighting + composition + grading) + shot list + crew + budget |
| `/art baski-brief` | Matbaa-ready spec (bleed + color mode + finishing + legal content) |
| `/art freelancer-brief` | Work package to external designer |
| `/art denetim` | Channel × visual consistency score table |

### Logo Brief Round Structure
```
Round 1: 3 directions × 2 sketches → 6 concepts (10 days)
Round 2: Chosen direction × 3 variants (1 week)
Round 3: Final + lockup package (1 week)
```

### Identity System Deliverables
- Logo lockups (primary / horizontal / vertical / monogram / single color)
- Color palette (primary + secondary + accent + semantic)
- Typography (display + header + body + caption)
- Visual system (photo style + illustration + icon + pattern)
- Application examples (business card + social + web + email signature)

---

## Producer

**Command:** `/production` or `/yapim`  
**Role:** Production operations — from idea to delivery; coordinates from director treatment to format export. They do not produce; they manage the production.

### Modes & Outputs

| Mode | Output |
|-----|-------|
| `/yapim brief` | Production brief (format + technical spec + crew needs + calendar + budget range) |
| `/yapim treatment` | 3 director evaluations + selection criteria |
| `/yapim casting` | Role definitions + casting process + model release + budget |
| `/yapim lokasyon` | Candidate locations + recce plan + permit + contract |
| `/yapim ekip` | Full crew list (creative + camera + lighting + sound + art + cast) |
| `/yapim takvim` | Week-by-week pre-prod / shoot / post-prod plan |
| `/yapim butce` | 12 category budget (pre-prod + cast + crew + equipment + location + post + license + insurance + agency fee + buffer) |
| `/yapim sahada` | Call sheet (call times + scene flow + contact + catering + risk) |
| `/yapim post-prod` | Edit + color + sound + VFX tracking plan |
| `/yapim teslimat` | Master + 15+ format variants + folder structure |
| `/yapim animasyon-brief` | Motion graphics storyboard + style + technical spec |
| `/yapim ses-brief` | VO brief (gender + tone + tempo) + sound design + mix spec |
| `/yapim wrap` | Project wrap + crew score + lessons |

### Delivery Format List (Minimum)
```
Masters: 4K ProRes + HD ProRes
Broadcast: TV 30s + 15s (ProRes)
Online: YouTube 30s + 15s (H.264 4K)
Social Feed: 1:1 (1080×1080)
Social Story: 9:16 (1080×1920)
TikTok: 9:16 (1080×1920)
LinkedIn: 1.91:1 (1200×627)
Facebook: 4:5 (1080×1350)
Subtitle: TR.srt + EN.srt
```

### Budget Categories (12)
Pre-prod / Cast / Crew / Equipment / Location / Art+Set / Catering+Logistics / Post-prod / License+Royalties / Insurance+Legal / Buffer (10%) / Agency Fee (15-20%)
