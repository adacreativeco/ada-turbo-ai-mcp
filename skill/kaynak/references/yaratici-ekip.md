# Yaratıcı Ekip Referans Dosyası

## İçindekiler
1. [Yaratıcı Direktör](#yaratıcı-direktör)
2. [Copywriter](#copywriter)
3. [Art Director](#art-director)
4. [Yapımcı / Producer](#yapımcı--producer)

---

## Yaratıcı Direktör

**Komut:** `/yaratici`  
**Rol:** Orkestra şefi — brief'i 4 yaratıcı role böler, çıktıları bütünsel değerlendirir, müşteri sunumuna kadar koordine eder. Kendisi üretmez, kalite eşiğini tutar.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/yaratici brief-dagit` | Copy + Art + Yapım + UI/UX için ayrı brief paketleri |
| `/yaratici konsept` | 3 yaratıcı yön (isim + manifesto + tagline + key visual + kanal önizleme + neden güçlü + risk) |
| `/yaratici round-yonetimi --round=1/2/3` | Round brief + ekip görevleri + süre |
| `/yaratici kalite-kontrol` | 7 boyutlu QC raporu (brief / marka / çapraz tutarlılık / big idea / kitle / cesaret / ölçülebilirlik) |
| `/yaratici sunum-haz` | Müşteri sunum dosyası akışı |
| `/yaratici prodüksiyon-onay` | Go/No-go checklist (yaratıcı + hukuki + bütçe + lojistik) |
| `/yaratici ekip-kapasite` | Ekip yük dağılımı + overload uyarısı |

### Round Yapısı (Sektör Standardı)
```
Round 1 → 3 konsept yönü → müşteri seçer
Round 2 → seçilen konsept × 2 varyant → ince ayar
Round 3 → final + son kalibrasyon → onay
→ Prodüksiyon
```

### Kalite Kontrol 7 Boyut
1. Brief uyumu
2. Marka uyumu
3. Çapraz tutarlılık (Copy + Art + Yapım)
4. Big idea sadakati
5. Hedef kitle uyumu
6. Yaratıcı cesaret
7. Ölçülebilirlik

---

## Copywriter

**Komut:** `/copy`  
**Rol:** Kelime ustası — tagline'dan TVC senaryosuna kadar, marka ton-of-voice'u uygulayarak üretir. Minimum 2-3 varyasyon her zaman.

### Modlar ve Çıktıları

| Mod | Çıktı |
|-----|-------|
| `/copy tagline` | 10 finalist + 5 boyut skor + domain/handle kontrol |
| `/copy headline` | 8 yaklaşım × 8 headline + top 3 öneri |
| `/copy body` | AIDA / PAS / Hikaye — min 3 varyasyon |
| `/copy script --format=tv-30/tv-15/tiktok-30/vs` | Saniye bazlı script (görüntü + ses + alt yazı) |
| `/copy sosyal --kanal=linkedin/x/instagram/tiktok` | Platform-spesifik copy + hashtag |
| `/copy email --tip=welcome/nurture/winback/vs` | E-posta serisi copy |
| `/copy seo-icerik` | SEO brief + outline + meta |
| `/copy urun` | Hero cümle + kısa/uzun ürün açıklaması + bullet'lar |
| `/copy ux` | Button + error + empty state + onboarding copy kütüphanesi |
| `/copy manifesto` | 3 varyasyon (inanç / savaş / hikaye odaklı) |
| `/copy revize` | Mevcut copy → marka tonuna çeviri |
| `/copy denetim` | Kanal × kanal ton skoru |

### Üretim Kuralları
- Her zaman minimum 2-3 varyasyon (A/B test için)
- Yasak kelimeler: "kullanıcı dostu", "best in class", "world-class", "next-gen", "revolutionary", "mükemmel"
- Uydurma sayı yasak — bilinmeyen → `%X` placeholder
- Her varyasyon için: kim için, hangi durumda, beklenen tepki

### Script Format (TV 30sn)
```
Saniye 0-5: Kanca (görüntü + ses)
Saniye 5-15: Problem (VO)
Saniye 15-25: Çözüm (VO)
Saniye 25-30: Kapanış + tagline
```

---

## Art Director

**Komut:** `/art`  
**Rol:** Görsel kafa — strateji + marka yönünü görsel dile çevirir. Brief'ler ve onaylar; tasarımı tasarımcı yapar, Art Director yönlendirir ve onaylar.

### Modlar ve Çıktıları

| Mod | Çıktı |
|-----|-------|
| `/art logo-yon` | 3 yön brief (hissetir/hissettirme + referans + anti-referans + round yapısı) |
| `/art kimlik-sistem` | Tam brand system (renk HEX/RGB/CMYK/Pantone + tipografi + görsel sistem + spacing + grid) |
| `/art moodboard` | 3 kampanya yönü + kıyaslama matrisi + önerilen |
| `/art kampanya-gorsel` | Key visual + format türetme tablosu (billboard → sosyal → banner → email) |
| `/art layout-brief --kanal=ooh/print/sosyal/display` | Kanal-spesifik tasarım kuralları + deliverable spec |
| `/art ikon-sistem` | Grid + stroke + corner kuralları + naming convention |
| `/art illustration-yon` | Stil rehberi (çizgi / renk / karakter / kullanım senaryoları) |
| `/art fotografk-yon` | Stil (lighting + composition + grading) + shot list + ekip + bütçe |
| `/art baski-brief` | Matbaa-ready spec (bleed + renk modu + finishing + yasal içerik) |
| `/art freelancer-brief` | Dış tasarımcıya iş paketi |
| `/art denetim` | Kanal × görsel tutarlılık skor tablosu |

### Logo Brief Round Yapısı
```
Round 1: 3 yön × 2 sketch → 6 konsept (10 gün)
Round 2: Seçilen yön × 3 varyant (1 hafta)
Round 3: Final + lockup paketi (1 hafta)
```

### Kimlik Sistem Deliverables
- Logo lockup'lar (ana / yatay / dikey / monogram / tek renk)
- Renk paleti (birincil + ikincil + accent + semantic)
- Tipografi (display + başlık + gövde + caption)
- Görsel sistem (foto stili + illüstrasyon + ikon + pattern)
- Uygulama örnekleri (kartvizit + sosyal + web + e-posta imzası)

---

## Yapımcı / Producer

**Komut:** `/yapim`  
**Rol:** Prodüksiyon operasyonu — fikirden teslimata; yönetmen treatment'tan format export'a kadar koordine eder. Kendisi üretmez, üretimi yönetir.

### Modlar ve Çıktıları

| Mod | Çıktı |
|-----|-------|
| `/yapim brief` | Prodüksiyon brief (format + teknik spec + ekip ihtiyacı + takvim + bütçe aralığı) |
| `/yapim treatment` | 3 yönetmen değerlendirme + seçim kriterleri |
| `/yapim casting` | Rol tanımları + casting süreci + model release + bütçe |
| `/yapim lokasyon` | Aday lokasyonlar + recce planı + izin + sözleşme |
| `/yapim ekip` | Full crew listesi (yaratıcı + kamera + lighting + ses + sanat + cast) |
| `/yapim takvim` | Hafta hafta pre-prod / shoot / post-prod planı |
| `/yapim butce` | 12 kategori bütçe (pre-prod + cast + crew + ekipman + lokasyon + post + lisans + sigorta + ajans fee + buffer) |
| `/yapim sahada` | Call sheet (çağrı saatleri + sahne akışı + iletişim + catering + risk) |
| `/yapim post-prod` | Edit + color + sound + VFX takip planı |
| `/yapim teslimat` | Master + 15+ format varyant + klasör yapısı |
| `/yapim animasyon-brief` | Motion graphics storyboard + stil + teknik spec |
| `/yapim ses-brief` | VO brief (cinsiyet + ton + tempo) + sound design + mix spec |
| `/yapim wrap` | Proje kapanış + ekip skoru + dersler |

### Teslimat Format Listesi (Minimum)
```
Masters: 4K ProRes + HD ProRes
Broadcast: TV 30s + 15s (ProRes)
Online: YouTube 30s + 15s (H.264 4K)
Sosyal Feed: 1:1 (1080×1080)
Sosyal Hikaye: 9:16 (1080×1920)
TikTok: 9:16 (1080×1920)
LinkedIn: 1.91:1 (1200×627)
Facebook: 4:5 (1080×1350)
Subtitle: TR.srt + EN.srt
```

### Bütçe Kategorileri (12)
Pre-prod / Cast / Crew / Equipment / Lokasyon / Art+Set / Catering+Lojistik / Post-prod / Lisans+Telif / Sigorta+Yasal / Buffer (%10) / Ajans Fee (%15-20)
