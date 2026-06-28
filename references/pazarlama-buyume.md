# Pazarlama & Büyüme Referans Dosyası

## İçindekiler
1. [Performans Pazarlama](#performans-pazarlama)
2. [SEO](#seo)
3. [E-posta & CRM Pazarlama](#e-posta--crm-pazarlama)
4. [Growth Hacker](#growth-hacker)
5. [Sosyal Medya Yöneticisi](#sosyal-medya-yöneticisi)
6. [İçerik Stratejisti](#içerik-stratejisti)
7. [Influencer & Partnership](#influencer--partnership)
8. [Medya Planlama & Satın Alma](#medya-planlama--satın-alma)

---

## Performans Pazarlama

**Komut:** `/performans` (referans: CMO workflow içinde `/cmo kampanya` de dahil)  
**Rol:** Paid acquisition — Google/Meta/LinkedIn/TikTok self-serve kanallar, ROAS/CPA optimizasyonu.

### Temel Çerçeve
- **Acquisition:** Paid traffic → landing
- **Metrikler:** ROAS, CPA, CAC, CTR, CPM
- **Araçlar:** Google Ads, Meta Ads Manager, LinkedIn Campaign Manager, TikTok Ads

### Kampanya Raporu Formatı
```
# Kampanya Raporu: {kampanya}
## KPI Sonuçları (Hedef vs Gerçek tablosu)
## Niye Başarısız/Başarılı (hipotezler)
## Channel × Performance (Spend / Conversion / CPA / ROAS)
## Creative × Performance (Top 3 + Bottom 3)
## Audience × Performance
## Time × Performance
## Lessons Learned
## Sonraki Kampanya İçin
## ROI Re-Analiz (multi-touch ile)
```

---

## SEO

**Komut:** `/seo-altyapisi`  
**Rol:** Teknik SEO altyapısı — lansman öncesi/sonrası kontrol, indexing, structured data, Core Web Vitals.

### Pre-launch Kontrol Listesi
- robots.txt + sitemap.xml
- Structured data (JSON-LD) — schema tipi × sayfa tipi
- Title + meta description benzersizliği
- Open Graph + Twitter Card
- Image alt text + format (WebP/AVIF)
- Core Web Vitals (LCP <2.5s, INP <200ms, CLS <0.1)
- Google Search Console + Bing Webmaster doğrulama
- IndexNow entegrasyonu
- **Lansman blocker:** noindex kaldırıldı mı?

### Sınıflandırma
| Sınıf | Kriter |
|-------|--------|
| 🔴 Blocker | robots Disallow:/, sitemap broken, %50+ canonical hatalı |
| 🟠 Yüksek | Title/desc duplicate %20+, alt text %50- eksik |
| 🟡 Orta | Internal linking, breadcrumb eksik |

---

## E-posta & CRM Pazarlama

**Komut:** `/email`  
**Rol:** Lifecycle marketing — welcome'dan win-back'e, newsletter'dan transactional'a. Owned kanal = liste sahipliği.

### Sequence Tipleri
| Sequence | Amaç | Uzunluk |
|---------|-------|---------|
| Welcome | İlk değere ulaştır | 5-7 e-mail |
| Nurture | Lead → müşteri | 8-12 e-mail, 4-6 hafta |
| Abandoned | Sepet/form geri kazanma | 3 e-mail |
| Post-purchase | Retention + cross-sell | 5-6 e-mail |
| Win-back | Dormant yeniden canlandır | 4 e-mail |

### Deliverability Zorunluları
- SPF + DKIM + DMARC (p=quarantine minimum)
- Mail-Tester.com ≥ 9/10
- Bounce rate < %2, Spam complaint < %0.1
- Warm-up: lansmandan 14 gün önce başla

### Welcome Sequence (SaaS örnek)
```
E-mail 1 (anında): Hoş geldin + ilk aksiyon CTA
E-mail 2 (gün 1): Pozitif reinforcement + power feature
E-mail 3 (gün 3): Use case / müşteri hikayesi
E-mail 4 (gün 5): Yardım var (support + docs)
E-mail 5 (gün 7): Plan seç (eğer trial bitiyorsa)
```

### KVKK / GDPR Zorunluları
- Açık rıza (pre-checked yasak)
- Footer'da unsubscribe
- Footer'da fiziksel adres
- Veri sahibi hakları kanalı

---

## Growth Hacker

**Komut:** `/growth`  
**Rol:** AARRR funnel optimizasyonu — data-driven deneyler, ICE skorlama, A/B test disiplini.

### AARRR Funnel
```
Acquisition → Activation → Retention → Revenue → Referral
```

### ICE Skoru
```
Impact (1-10) × Confidence (1-10) × Ease (1-10) / 3
ICE > 7 → ship-worthy
```

### Deney Brief Şablonu
```
Hipotez: "Eğer X yaparsak, Y metrik Z% iyileşir, çünkü..."
Variant A (control): ...
Variant B (test): ...
Sample size: N/variant (95% confidence)
Süre: minimum 1 hafta
Birincil metrik: ...
Guardrail: ...
Karar kriteri: p < 0.05 + +5pp minimum lift
```

### 90 Gün Pipeline Yapısı
- Ay 1: Activation sprint (en zayıf halka)
- Ay 2: Retention sprint
- Ay 3: Revenue/Referral sprint

---

## Sosyal Medya Yöneticisi

**Komut:** `/sosyal`  
**Rol:** Organik sosyal — broadcast (post) + conversation (yorum/DM/mention).

### Platform Rolleri
| Platform | Birincil Rol | Format Mix |
|----------|-------------|------------|
| Instagram | Brand awareness + ürün | Reel %40, carousel %30, story günlük |
| LinkedIn | Otorite + B2B | Text %40, CEO insight %30, carousel %20 |
| TikTok | Discovery + genç | Trend %40, educational %30, BTS %20 |
| YouTube | Deep content + SEO | Tutorial %30, shorts %30, review %20 |
| X/Twitter | Conversation + hızlı tepki | Reply %50, thread %25 |

### Community Tepki Süreleri (SLA)
| Tip | Hedef |
|-----|-------|
| DM yeni | < 2 saat (mesai) |
| Yorum | < 2 saat |
| Müşteri şikayeti | < 30 dakika |
| Kriz/viral negatif | < 15 dakika → Kriz İletişimi'ne eskalasyon |

### İçerik Pillar Dağılımı
- Eğitim/değer: %30-40
- BTS/insanlaştırma: %20-25
- Sosyal kanıt/müşteri: %15-20
- Promo: max %15-20 (aşarsa spam algısı)

### Trend Watch (Günlük)
TikTok Discover + X trending + Google Trends TR  
→ Değerlendirme: marka uyumlu? hâlâ canlı? hızlı yapılabilir? risk var mı?

---

## İçerik Stratejisti

**Komut:** `/icerik`  
**Rol:** Uzun vadeli editorial sistem — pillarlar, takvim, atomization, thought leadership.

### İyi Pillar Kriterleri
- Persona'nın gerçek sorununa hizmet eder
- Markaya özel otorite alanı
- Rakipten farklı açı var
- 50+ içerik üretilebilir
- 5 yıl sonra bile alakalı

### Atomization Zinciri
```
1 Tentpole (whitepaper/60dk video/podcast)
→ 3-5 blog post (chapter bazlı)
→ 3-5 video (YouTube)
→ 1 LinkedIn carousel
→ 1 Twitter thread
→ 3 newsletter bölüm
→ 5+ Short/Reel
→ 1 webinar
→ 1 e-mail nurture sequence
```

### Aylık Ritim
- Haftalık: 1-2 blog + newsletter + sosyal destek
- Aylık: 1 cornerstone (whitepaper/video serisi)
- Çeyreklik: 1 major kampanya içerik paketi

---

## Influencer & Partnership

**Komut:** `/influencer`  
**Rol:** Discovery → vetting → sözleşme → brief → performans takip.

### Creator Tier (TR)
| Tier | Followers | Avg Fee | Engagement |
|------|-----------|---------|------------|
| Nano | <10K | ₺500-3K | %5-10 |
| Mikro | 10K-100K | ₺3K-25K | %3-7 |
| Mid | 100K-500K | ₺25K-100K | %2-5 |
| Macro | 500K-1M | ₺100K-300K | %1-3 |
| Mega | 1M+ | ₺300K-2M+ | %0.5-2 |

### Vetting Kriterleri (HypeAuditor)
- Bot oranı < %5
- Audience Quality Score > 70
- Persona demografik uyumu > %70
- Sponsorship saturation < %20

### Zorunlular
- KVKK: sözleşmede
- TR reklam beyanı: #sponsorluk / #ad caption başında
- Pre-publish marka onayı zorunlu
- Model release imzalı

### Kriz Protokolü (Creator Skandalı)
🔴 → Tüm aktif content pause + Kriz İletişimi uyar  
🟠 → Yeni yayın yok, gözlem  
🟡 → Olağan devam  

---

## Medya Planlama & Satın Alma

**Komut:** `/medya`  
**Rol:** Rezervasyon-bazlı medya — TV, OOH, print, programatik, sinema, podcast sponsorluk.

### Kanal Rolleri Matrisi
| Rol | Kanal | Bütçe Ağırlığı |
|-----|-------|---------------|
| Reach | TV, OOH, YouTube | %35-50 |
| Engage | Meta, TikTok organik boost | %20-30 |
| Convert | Google Search, retargeting | %15-20 |
| Retain/Advocate | E-mail, influencer | %5-10 |

### OOH Format'lar (TR)
Billboard, otobüs durağı, metro istasyonu, AVM içi dijital, DOOH (programatik), taksi üstü, asansör

### Programatik DSP'ler
- DV360 (Google): display + video + YouTube reach
- The Trade Desk: premium + CTV
- DOOH: Vistar Media, Broadsign

### Negosiasyon Kartları
- Yıllık hacim taahhüdü → AVB %5-15
- Kombinasyon paketi → pozisyon iyileştirme
- Hızlı ödeme → ekstra indirim
