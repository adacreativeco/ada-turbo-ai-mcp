# ADA Turbo — Ajans İşletim Sistemi Skill'i

Claude için **ADA Creative Co.** ajans işletim sistemi. 20+ ajanlık tam bir dijital ajans yapısını tek skill'e sığdırır. Herhangi bir müşteri veya proje için sanki ajansın bir çalışanıymış gibi devreye girer.

## Neler İçeriyor?

| Alan | Ajanlar |
|------|---------|
| **Strateji** | Strateji Direktörü, Marka Stratejisti |
| **Yaratıcı** | Yaratıcı Direktör, Copywriter, Art Director, Yapımcı |
| **Pazarlama** | Performans, SEO, E-posta/CRM, Growth, Sosyal, İçerik, Influencer, Medya Planlama |
| **Müşteri & Ops** | Hesap Yöneticisi, Proje Yöneticisi, Müşteri Başarısı (CS), Kriz İletişimi, PR |
| **Analitik & Ürün** | Analitik, CFO, CEO/Ürün Müdürü, CTO, CoS (Kurmay Başkanı), Intel |
| **Orkestrasyon** | Müdür (tüm workflow'ları koordine eder) |

## Kurulum

1. `.skill` dosyasını indirin
2. Claude.ai'da Settings → Skills → Install
3. Hazır

## Kullanım

### Komut formatıyla:
```
/strateji yaratici-brief --kampanya=Yaz_2025 --musteri=Nexus
/copy tagline --musteri=ADA
/cfo birim-ekonomi
/kriz alarm
/sosyal takvim --musteri=Nexus --hafta=22
```

### Serbest metin ile:
```
"Nexus SaaS için aylık analitik raporu yaz, MRR ₺145K, %8 büyüme"
"Bu kampanya için yaratıcı konsept önerileri hazırla"
"Churn riski olan müşteriler için save-call brief'i yaz"
```

## Yapı

```
ada-turbo/
├── SKILL.md                          ← Ana skill (komut haritası + kurallar)
└── references/
    ├── strateji-marka.md             ← Strateji Direktörü + Marka Stratejisti
    ├── yaratici-ekip.md              ← Yaratıcı Direktör + Copy + Art + Yapım
    ├── pazarlama-buyume.md           ← Performans, SEO, Email, Growth, Sosyal, İçerik, Influencer, Medya
    ├── musteri-operasyon.md          ← Hesap, Proje, CS, Kriz, PR
    └── analitik-urun-teknik.md       ← Analitik, CFO, CEO, CTO, CoS, Intel, Müdür
```

## Lisans

MIT — kopyala, uyarla, kullan.
