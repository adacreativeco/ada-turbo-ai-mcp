# Analitik, Ürün & Teknik Referans Dosyası

## İçindekiler
1. [Analitik & Raporlama](#analitik--raporlama)
2. [CFO / Finans](#cfo--finans)
3. [CEO / Ürün Müdürü](#ceo--ürün-müdürü)
4. [CTO / Teknoloji Müdürü](#cto--teknoloji-müdürü)
5. [Kurmay Başkanı (CoS)](#kurmay-başkanı-cos)
6. [İstihbarat / Intel](#istihbarat--intel)
7. [Müdür (Orchestrator)](#müdür-orchestrator)

---

## Analitik & Raporlama

**Komut:** `/analitik`  
**Rol:** Cross-channel analytics — veri değil, karar destekleyici insight.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/analitik onboard` | Tracking altyapı kurulum planı |
| `/analitik kurulum` | GTM container yapısı + event taksonomi |
| `/analitik dashboard` | Executive / Channel / Operational dashboard şablonu |
| `/analitik attribution` | Last-touch vs data-driven karşılaştırması |
| `/analitik kampanya-rapor` | KPI vs hedef + neden analizi + lessons |
| `/analitik aylik-rapor` | North Star + Tier 2 + kanal + cohort + insight |
| `/analitik ab-test-analiz` | İstatistiksel anlamlılık + p-value + karar |
| `/analitik cohort` | Retention heatmap + LTV by channel |
| `/analitik funnel` | Aşama × conversion × sızıntı noktası |
| `/analitik insight` | Hipotez → veri → doğrulama → aksiyon |
| `/analitik denetim` | Data health skor (tracking / completeness / consistency) |

### 3-Tier KPI Modeli
```
Tier 1 — North Star (1-3 metrik): MRR / GMV / ARR
Tier 2 — İş Sağlığı (5-10): CAC / LTV / Churn / NRR
Tier 3 — Operasyonel (20-50): kanal × kampanya metrikleri
```

### Attribution Modelleri (Önerilen Sıra)
1. **Data-driven** (GA4 ML) — en doğru, 300+ conversion/ay gerekir
2. **Time-decay** — varsayılan öneri
3. **Last-touch** — legacy karşılaştırma için
4. **First-touch** — awareness görünürlüğü için

### Aylık Rapor Format
```
# Aylık Rapor: {ay}
## Executive Özet (1 paragraf, CEO için)
## North Star
## Tier 2 KPI Tablosu (Bu ay / Geçen ay / %Δ / Hedef / Statü)
## Acquisition Analizi
## Channel Performance
## A/B Test Sonuçları
## Cohort Analizi
## Insight'lar (3 adet)
## Sonraki Ay Planı
## Risk
## ROI Özeti
## Aksiyon Listesi (sahip + deadline)
```

---

## CFO / Finans

**Komut:** `/cfo`  
**Rol:** Finansal sağlık — MRR, birim ekonomi, runway, fiyatlandırma, faturalandırma.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/cfo mrr` | MRR hareketi (yeni/expansion/churn/contraction) + NRR |
| `/cfo birim-ekonomi` | CAC / LTV / LTV:CAC / Payback / Gross Margin |
| `/cfo runway` | Burn rate + runway + 4 senaryo modeli |
| `/cfo fiyat-analizi` | Conversion + churn + rakip + birim ekonomi karşılaştırması |
| `/cfo faturalandirma` | Failed payment % + dunning recovery + KVKK |
| `/cfo cohort` | Revenue retention heatmap + LTV by channel |
| `/cfo p-and-l` | Gelir → COGS → Gross Profit → OpEx → EBITDA |
| `/cfo board-paketi` | Yatırımcı/board finansal paketi |

### Birim Ekonomi Benchmarklar (SaaS)
| Metrik | Kötü | Kabul | İyi | Mükemmel |
|--------|------|-------|-----|----------|
| LTV:CAC | <1 | 1-3 | 3-5 | 5+ |
| Payback | >24ay | 12-24ay | 6-12ay | <6ay |
| Gross Margin | <%50 | 50-70% | 70-80% | 80%+ |
| MRR Churn | >%5/ay | 2-5% | 1-2% | <%1 |

### Runway Eşik Uyarıları
- < 6 ay: 🔴 Kapatma kararı zamanı
- < 12 ay: 🟠 Yatırım turu başlat
- < 18 ay: 🟡 Plan yapmaya başla
- > 18 ay: 🟢 Sağlıklı

---

## CEO / Ürün Müdürü

**Komut:** `/ceo`  
**Rol:** Stratejik kafa — ürün vizyonundan yatırımcı pitchine, kuzey yıldızından karar destekten.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/ceo brief --tip=weekly/monthly/quarterly` | Strateji brief (müdür'den veri + iş yorumu) |
| `/ceo pitch --sure=1m/5m/30m --kitle=yatirimci/musteri/ekip` | Süre × kitle uyumlu pitch |
| `/ceo karar` | 3 senaryo + trade-off + CEO önerisi (Type 1/2 analizi) |
| `/ceo metrik` | North star + funnel + birim ekonomi + sağlık dashboard |
| `/ceo rakip` | Stratejik rakip profili (sermaye + ürün + pazar + SWOT) |
| `/ceo risk` | 5 kategori risk haritası (operasyonel/pazar/hukuki/teknik/finansal) |
| `/ceo roadmap` | RICE sıralı roadmap + yapmayacaklarımız bölümü |
| `/ceo paydas` | Yatırımcı/ekip/müşteri/basın iletişim şablonu |
| `/ceo org` | Agentic mimari denetimi — execution gap + yeni ajan önerisi |

### Yatırımcı Pitch 5dk Yapısı
```
1. Problem (45s): Kim yaşıyor, neden büyük
2. Çözüm (45s): Tek cümle + demo ekran
3. Pazar (30s): TAM + timing
4. Traction (45s): Sayılar + büyüme
5. İş Modeli (30s): Para akışı + birim ekonomi
6. Rekabet (30s): Pozisyonlama matrisi
7. Ekip (15s): Niye onlar
8. İstek (30s): Ne kadar, neye, milestones
```

---

## CTO / Teknoloji Müdürü

**Komut:** `/cto`  
**Rol:** Teknoloji stratejisi — mimari kararlar, teknik borç, scale planı, vendor değerlendirme.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/cto altyapi-saglik` | Stack sürüm × EOL × vendor sağlık tablosu |
| `/cto teknik-borc` | Borç envanteri (etki × aciliyet × tahmin süre) + 90 gün ödeme planı |
| `/cto scale-plani --hedef=10x/100x` | Darboğaz analizi + adım adım scale yolu |
| `/cto api-roadmap` | Public API stratejisi + versioning + SDK + docs |
| `/cto mimari-karar` | ADR (Architecture Decision Record) belgesi |
| `/cto build-vs-buy` | Yapma vs satın alma maliyet + TCO + karar |
| `/cto vendor-degerlendirme` | Mevcut vendor sağlık + alternatif karşılaştırma |
| `/cto disaster-recovery` | RTO/RPO + senaryo × müdahale planı |

### ADR Formatı
```
# ADR-{NN}: {Karar Başlığı}
Tarih / Durum / Verenler / Etkilenenler
## Bağlam
## Karar
## Gerekçe
## Değerlendirilen Alternatifler
## Sonuçlar (iyi + kötü/trade-off)
## Geri-dönülebilirlik (Type 1 / Type 2)
```

### Teknik Borç Skoru = Etki (1-5) × Aciliyet (1-5)
- 20-25: Acil (sprint'in %40'ı)
- 12-19: Bu çeyrek
- 6-11: Backlog
- 1-5: Kabul edilmiş borç

---

## Kurmay Başkanı (CoS)

**Komut:** `/cos`  
**Rol:** Stratejik disiplin katmanı — CEO + 5 ajandaki kararlar, beyinler arası tutarlılık, OKR riski.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/cos sync` | Beyinler arası çelişki raporu (🔴 kritik / 🟠 stale / 🟡 yön kayması) |
| `/cos roadmap-takip` | CEO roadmap × gerçek ilerleme tablosu |
| `/cos karar-takip` | Karar yaşam döngüsü (önerildi → kabul → uygulandı → tamamlandı) |
| `/cos action-items` | Tüm brief'lerden action item havuzu (sahip + deadline + durum) |
| `/cos haftalik-sync` | CEO için 1 sayfa: 5 ajan + müdürden bu hafta özet |
| `/cos eskalasyon` | Deadline geçmiş / karar bekleyen / OKR risk listesi |
| `/cos okr-checkpoint` | Çeyrek OKR ilerleme + trend + risk altında olanlar |

### CoS Yetki Sınırları
✅ Tüm beyinleri okur  
✅ Çelişki tespit eder, raporlar  
✅ Action item havuzu kurar  
❌ Beyinleri yazmaz/değiştirmez  
❌ Karar vermez (CEO verir)  
❌ Workflow tetiklemez  

---

## İstihbarat / Intel

**Komut:** `/intel`  
**Rol:** Dış dünya radarı — rakip hareketleri, pazar trendleri, fırsat/tehdit.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/intel rakip-monitor` | Haftalık rakip hareketleri (yatırım/ürün/ekip/fiyat/pazar) |
| `/intel rakip-derin` | Sermaye + ürün + müşteri + trajectory + SWOT |
| `/intel hareket-uyari` | Son 30g önemli hareketler + CEO için anlamı |
| `/intel pazar-trend` | Yükselen/düşen/plateau trendler |
| `/intel firsat` | Tespit edilen fırsatlar (regülasyon/niş/rakip zayıflığı) |
| `/intel pazar-haritasi` | Segment × oyuncu × pazar payı + white space |
| `/intel cikti-radar` | Haftalık 5 önemli şey (CEO için 3 dk özet) |
| `/intel ekip-monitor` | Rakip LinkedIn + açık pozisyon büyüme analizi |

### Haber Kategori Önem
| Kategori | Tetikleyici |
|----------|------------|
| 💰 Yatırım | Round haberi, acquisition |
| 🚀 Ürün | Major launch, breaking change |
| 👥 Ekip | C-level değişim, kilit hire |
| 💸 Fiyat | Plan/limit değişikliği |
| 🌍 Pazar | Yeni coğrafya/segment |

### Intel → CEO Köprüsü
- Her bulgu için: veri → **"Bizim için anlamı"** bölümü zorunlu
- Spekülatif yorumlar: **"Hipotez"** olarak işaretli
- Her iddianın kaynağı: link + tarih + yazar

---

## Müdür (Orchestrator)

**Komut:** `/mudur`  
**Rol:** Tüm workflow'ları orchestrate eder, çıktıları okur, üst seviye yönetim brief'i hazırlar, pattern tespit ederse yeni worker önerir.

### Çalışma Modları
| Mod | Kapsam |
|-----|--------|
| `weekly` | Tam döngü — tüm sub-workflow'lar → brief |
| `read-only` | Sadece son raporları topla |
| `incident` | Acil: bug + site-saglik + guvenlik |
| `pre-launch` | Lansman odaklı: lansman-hazirlik + yuk-testi + kullanici-akisi |

### Alt Workflow'lar
`/site-saglik` / `/bug-tarama` / `/guvenlik-kontrolu` / `/seo-altyapisi` / `/temizlik` / `/kullanici-akisi` / `/yuk-testi` / `/lansman-hazirlik`

### Bulgu Seviyeleri
| Seviye | Tanım |
|--------|-------|
| 🚨 YANGIN | Production'da kullanıcı etkileniyor |
| 🔥 BLOCKER | Lansman tarihinde olmazsa ertelenir |
| ⚠️ RİSK | Yakında etkileyebilir |
| 📌 DİKKAT | Önemli ama acil değil |
| 📋 BİLGİ | İz kaydı için |

### Haftalık Brief Format
```
# Haftalık Brief — Hafta {WW}
> Lansmana: {X gün} kaldı

## 🚦 Genel Durum (tek cümle)
## 🔥 Lansman Blocker'ları
## 🚨 Yangın (acil)
## ⚠️ Risk (bu hafta içinde)
## 📌 Dikkat (2-4 hafta)
## 📋 İyi Haber
## 📈 Trend (3 hafta ASCII grafiği)
## 🤖 Yeni İşçi Önerisi? (pattern varsa)
## 🎯 Bu Haftaki 3 Odak
```

### Worker (Yeni Workflow) Tetikleyicileri
- Aynı kategori bug 3+ haftadır 🔴
- Yeni 3rd party servis eklenmiş, workflow yok
- Yeni feature kategorisi (yeni controller cluster)
- Aynı sayfa tipi her deploy'da kırılıyor
- Manuel tekrarlayan kontrol tespit edildi
