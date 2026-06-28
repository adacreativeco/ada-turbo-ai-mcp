# Müşteri İlişkileri & Operasyon Referans Dosyası

## İçindekiler
1. [Hesap Yöneticisi](#hesap-yöneticisi)
2. [Proje Yöneticisi](#proje-yöneticisi)
3. [Müşteri Başarısı (CS)](#müşteri-başarısı-cs)
4. [Kriz İletişimi](#kriz-iletişimi)
5. [PR & Kurumsal İletişim](#pr--kurumsal-iletişim)

---

## Hesap Yöneticisi

**Komut:** `/hesap`  
**Rol:** Müşteri × ajans köprüsü. Dışarıda müşterinin avukatı, içeride ajansın avukatı.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/hesap brief-al` | 20 soru → onaylı yazılı brief |
| `/hesap brief-tanitla` | İç ekip brief'i (deliverable tablosu + süre + bütçe + risk) |
| `/hesap onay-sureci` | Sunum formatı + revize yönetimi |
| `/hesap toplanti --tip=kickoff/weekly/QBR` | Gündem + notlar + action items şablonu |
| `/hesap status` | Haftalık status raporu (✅ tamamlanan / 🚧 devam / ⏳ sizden beklenen) |
| `/hesap eskalasyon` | Tier 1-4 eskalasyon belgesi |
| `/hesap qbr` | 90dk QBR gündemi + müşteri ilişkisi soru seti |
| `/hesap fatura` | Aylık fatura özeti + ödeme takip |
| `/hesap genisleme` | Upsell/cross-sell pitch belgesi |
| `/hesap yenileme` | T-3 ay yenileme pitch süreci |
| `/hesap memnuniyet` | Sağlık skoru (NPS + ödeme + iletişim + revize + ekip) |

### Brief Zorunlu 5 Soru
1. **Niye şimdi?** (tetikleyici)
2. **Hedef — sayısal ne?** (ölçülebilir)
3. **Hedef kitle tam olarak kim?**
4. **Başarı nasıl tanımlanır?**
5. **Kim hayır diyebilir?** (karar vericisi)

### Revize Yönetimi
- Standart sözleşme: 2 tur revize dahili
- 3+: kapsam dışı, yazılı onay + ekstra fatura
- "Daha modern olsun" → **"Modern derken? Hangi referans?"** — soyut feedback somutlaştır

### Müşteri Sağlık Skoru
```
NPS: 0-10
Ödeme durumu: 0-10 (zamanında mı?)
İletişim aktiflik: 0-10
Onay hızı: 0-10
Revize sayısı: 0-10 (az = iyi)
Ekip dinamiği: 0-10

Toplam / 6 → /10
8.5+: Yeşil | 7-8.5: Sarı | 5-7: Turuncu | <5: Kırmızı
```

---

## Proje Yöneticisi

**Komut:** `/proje`  
**Rol:** İç ekip operasyonu — timeline, kapasite, risk, görev takibi. "Olur" demez, gerçekçi taahhüt verir.

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/proje plan` | Hafta hafta faz → milestone → deliverable takvimi |
| `/proje kapasite` | Ekip × saat allocation + overload uyarısı |
| `/proje gorev` | SMART görev kartları (başlık + sahip + deadline + acceptance criteria) |
| `/proje stand-up` | Dün/bugün/blocker formatı |
| `/proje risk` | Risk register (olasılık × etki × mitigation) |
| `/proje status` | 🟢🟡🔴 sağlık + zaman + bütçe + ilerleme raporu |
| `/proje retro` | Keep/Stop/Start + action items |
| `/proje porfoy` | Tüm aktif projeler portföy tablosu |

### Kapasite Eşikleri
- 60%: Underutilized
- 60-80%: **İdeal**
- 80-95%: Tight, dikkat
- 95-110%: Overload risk
- 110%+: Kaçınılmaz fail

### Timeline Faz Şablonu (Kampanya)
```
Hafta 1-2: Strateji + Brief
Hafta 3: Konsept onay
Hafta 4-6: Üretim
Hafta 7: Review + Revize
Hafta 8: Lansman
Hafta 9-12: Post-launch + Rapor
```

### Risk Skor = Olasılık (1-5) × Etki (1-5)
- 15-25: 🔴 Kritik
- 9-14: 🟠 Yüksek
- 5-8: 🟡 Orta
- 1-4: 🟢 Düşük

---

## Müşteri Başarısı (CS)

**Komut:** `/cs`  
**Rol:** Mevcut müşteri/kullanıcı sağlığı — onboarding takip, churn erken uyarı, NPS, expansion.

### Sağlık Skoru Modeli
| Sinyal | Ağırlık |
|--------|---------|
| Login/kullanım frekansı | %15 |
| Ana aksiyon kullanımı | %25 |
| Onboarding tamamlama | %15 |
| Support ticket sentiment | %10 |
| Ödeme durumu | %15 |
| NPS son skoru | %10 |
| Çoklu kullanıcı (team) | %10 |

Toplam 0-100:
- 80+: 🟢 Sağlıklı
- 60-79: 🟡 İzlemede
- 40-59: 🟠 Risk
- <40: 🔴 Kritik

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/cs saglik` | Tüm kiracı sağlık tablosu |
| `/cs kiraci` | Tek kiracı derin profil (tarihçe + ticket + risk hipotez) |
| `/cs onboarding-takip` | İlk 30 gün takılma noktaları + müdahale |
| `/cs churn-uyari` | Risk tier × müdahale matrisi |
| `/cs nps` | NPS segment + detractor takip |
| `/cs expansion` | Upsell aday listesi (limit %80+, güçlü kullanım, büyüme sinyali) |
| `/cs save-call` | Churn riski call brief (sorular + hazır cevaplar + sınırlar) |
| `/cs qbr` | ₺50K+ kiracı için çeyreklik business review |

### Churn Müdahale Tier
| Yıllık Değer | Müdahale |
|-------------|----------|
| ≥ ₺50K | Kişisel save call + executive sponsor |
| ₺10K-50K | Kişisel save call |
| ₺2K-10K | Otomatik save mail + opsiyonel call |
| < ₺2K | Otomatik sequence |

---

## Kriz İletişimi

**Komut:** `/kriz`  
**Rol:** Kriz öncesi (oyun kitabı), kriz anında (yangın söndürme), sonrasında (ders).

### Zaman Standardı
- **T+30 dk:** Holding statement yayında
- **T+4 saat:** Tam yanıt yayında
- **T+1 saat:** Tier 1 stakeholder bilgilendirildi
- **T+7 gün:** Post-mortem tamamlandı

### Risk Matris Kategorileri
Operasyonel / İnsan kaynaklı / İtibar / Regülatif / Dış etken

Skor = Olasılık (1-5) × Etki (1-5)  
13-25: 🔴 Kritik → oyun kitabı zorunlu  
8-12: 🟠 Yüksek → oyun kitabı şart  

### Holding Statement Şablonu
```
{Müşteri}, bugün saat {X}'te tespit ettiğimiz {konu}
ile ilgili bir durum araştırıyoruz. Etkilenen 
taraflara doğrudan ulaşıyoruz. Daha fazla bilgiyi 
{zaman} içinde paylaşacağız.
```

### Tam Yanıt Yapısı
```
1. Açılış (ne oldu)
2. Ne yaptık (anında aksiyonlar)
3. Ne yapıyoruz (devam eden)
4. Etkilenenler için adımlar
5. Önleme (geleceğe dönük)
6. Sorumluluk (uygunsa)
7. Sonraki açıklama tarihi
```

### Tonlama Kuralları
✅ Açık / İnsani / Empatik / Sorumlu / Aksiyon odaklı  
❌ Pasif ses / "İddia edildi" / "Bazı kişiler" / Suçu başkasına yıkma / Spekülasyon

### Modlar

| Mod | Çıktı |
|-----|-------|
| `/kriz risk-haritasi` | Senaryo × olasılık × etki matrisi |
| `/kriz oyun-kitabi` | Senaryo-spesifik T+0 → T+72 protokolü |
| `/kriz simulasyon` | Tabletop egzersiz brief (2-3 saat) |
| `/kriz alarm` | AKTİF KRIZ — 3 paralel iş akışı hızlı başlatma |
| `/kriz holding-statement` | 30 dk içinde çıkacak geçici yanıt |
| `/kriz tam-yanit` | T+4 saat detaylı yanıt belgesi |
| `/kriz stakeholder-map` | Tier 1-4 bilgilendirme zinciri |
| `/kriz medya-brief` | Sözcü brief (mesaj çekirdeği + Q&A + yapma'lar) |
| `/kriz sosyal-yanit` | Platform × yanıt paketi + standart şablonlar |
| `/kriz post-mortem` | Zaman çizelgesi + etki + dersler + aksiyon maddeleri |

---

## PR & Kurumsal İletişim

**Not:** PR workflow bu sistemde `/pr` komutuyla çalışır. Temel output'lar:

### Temel Modlar
| Mod | Çıktı |
|-----|-------|
| `/pr basin-listesi` | Sektörel gazeteci + yayın + podcast listesi |
| `/pr basin-bulteni` | 5W + quote + boilerplate format |
| `/pr medya-kiti` | Şirket özeti + görsel + key facts + iletişim |
| `/pr sozcü-brief` | Mesaj çekirdeği + Q&A + bridging teknikleri |
| `/pr thought-leadership` | Makale + röportaj + konuşma konuları |
| `/pr kriz-pr` | Kriz İletişimi ile koordineli basın yanıtı |

### Basın Bülteni Yapısı
```
Başlık: eylem içerir (fiil + sonuç)
Alt başlık: bağlam
Lead paragraf: 5W tek paragrafta
Gövde: 3-4 paragraf (detay + quote + kanıt)
Boilerplate: şirket hakkında standart
İletişim: isim + e-mail + telefon
```
