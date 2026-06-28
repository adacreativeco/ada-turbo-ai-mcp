import json
import time
import random
import re
from pathlib import Path

# Komut → referans dosyası eşlemesi
COMMAND_MAP = {
    # Strateji & Marka
    "/strateji": "strateji-marka",
    "/marka": "strateji-marka",
    # Yaratıcı Ekip
    "/yaratici": "yaratici-ekip",
    "/copy": "yaratici-ekip",
    "/art": "yaratici-ekip",
    "/yapim": "yaratici-ekip",
    # Pazarlama & Büyüme
    "/performans": "pazarlama-buyume",
    "/seo-altyapisi": "pazarlama-buyume",
    "/email": "pazarlama-buyume",
    "/growth": "pazarlama-buyume",
    "/sosyal": "pazarlama-buyume",
    "/icerik": "pazarlama-buyume",
    "/influencer": "pazarlama-buyume",
    "/medya": "pazarlama-buyume",
    # Müşteri & Operasyon
    "/hesap": "musteri-operasyon",
    "/proje": "musteri-operasyon",
    "/cs": "musteri-operasyon",
    "/kriz": "musteri-operasyon",
    "/pr": "musteri-operasyon",
    # Analitik, Ürün & Teknik
    "/analitik": "analitik-urun-teknik",
    "/cfo": "analitik-urun-teknik",
    "/ceo": "analitik-urun-teknik",
    "/cto": "analitik-urun-teknik",
    "/cos": "analitik-urun-teknik",
    "/intel": "analitik-urun-teknik",
    "/mudur": "analitik-urun-teknik",
}

# Ajan Komutları → Ajan Rolleri eşlemesi (Görsel Arayüz için)
COMMAND_TO_AGENT = {
    "/strateji": "Strateji Direktörü",
    "/marka": "Marka Stratejisti",
    "/yaratici": "Yaratıcı Direktör",
    "/copy": "Copywriter",
    "/art": "Art Director",
    "/yapim": "Yapımcı",
    "/performans": "Performans Pazarlama",
    "/seo-altyapisi": "SEO",
    "/email": "E-posta / CRM",
    "/growth": "Growth Hacker",
    "/sosyal": "Sosyal Medya",
    "/icerik": "İçerik Stratejisti",
    "/influencer": "Influencer",
    "/medya": "Medya Planlama",
    "/hesap": "Hesap Yöneticisi",
    "/proje": "Proje Yöneticisi",
    "/cs": "Müşteri Başarısı",
    "/kriz": "Kriz İletişimi",
    "/pr": "PR",
    "/analitik": "Analitik",
    "/cfo": "CFO",
    "/ceo": "CEO / Ürün",
    "/cto": "CTO",
    "/cos": "Kurmay Başkanı",
    "/intel": "İstihbarat",
    "/mudur": "Müdür"
}

REFERENCE_TITLES = {
    "strateji-marka": "Strateji & Marka (Strateji Direktörü, Marka Stratejisti)",
    "yaratici-ekip": "Yaratıcı Ekip (Yaratıcı Direktör, Copywriter, Art Director, Yapımcı)",
    "pazarlama-buyume": "Pazarlama & Büyüme (Performans, SEO, Email, Growth, Sosyal, İçerik, Influencer, Medya)",
    "musteri-operasyon": "Müşteri & Operasyon (Hesap, Proje, CS, Kriz, PR)",
    "analitik-urun-teknik": "Analitik, Ürün & Teknik (Analitik, CFO, CEO, CTO, CoS, Intel, Müdür)",
}

BEHAVIOR_RULES = """\
## ADA TURBO — TEMEL DAVRANIŞ KURALLARI

1. DOĞRUDAN ÜRET. "Hazırlıyorum" / "Şimdi yapacağım" deme. Hemen çıktıyı yaz.
2. SAHTE VERİ KOYMA. Bilinmeyen sayılar {X}, %Y, ₺Z placeholder ile geçilir.
3. HER ZAMAN MİNİMUM 2-3 VARYASYON (copy, konsept, tagline gibi üretim görevlerinde).
4. ÇIKTI FORMATINI TAKİP ET. Her workflow'un kendi brief/rapor yapısı var — ona uy.
5. TÜRKÇE VARSAYILAN. İçerik İngilizce gerektiriyorsa İngilizce yaz.
6. Müşteri bilgisi yoksa yalnızca gerçekten gerekli 1-2 soruyu sor, sonra üret.

Çıktı kalite kriterleri: brief ile tutarlı, uydurma sayı yok, ilgili format uygulandı,
raporlarda sahip + deadline + aksiyon maddesi var, profesyonel ve dolgusuz Türkçe.
"""

REFERENCE_TITLES_EN = {
    "strateji-marka": "Strategy & Brand (Strategy Director, Brand Strategist)",
    "yaratici-ekip": "Creative Team (Creative Director, Copywriter, Art Director, Producer)",
    "pazarlama-buyume": "Marketing & Growth (Performance, SEO, Email, Growth, Social, Content, Influencer, Media)",
    "musteri-operasyon": "Client & Operations (Account, Project, CS, Crisis, PR)",
    "analitik-urun-teknik": "Analytics, Product & Tech (Analytics, CFO, CEO, CTO, CoS, Intel, Manager)",
}

BEHAVIOR_RULES_EN = """\
## ADA TURBO — CORE BEHAVIOR RULES

1. GENERATE DIRECTLY. Do not say "I am preparing" or "I will do it now". Write the output immediately.
2. NO FAKE DATA. Pass unknown numbers with placeholders like {X}, %Y, $Z.
3. ALWAYS AT LEAST 2-3 VARIATIONS (for copywriting, conceptual, tagline, etc. tasks).
4. FOLLOW THE OUTPUT FORMAT. Each workflow has its own brief/report structure — follow it.
5. ENGLISH DEFAULT. (Or Turkish if requested by the user, but default to the language of the request).
6. If client info is missing, ask only 1-2 really necessary questions, then generate.

Output quality criteria: consistent with the brief, no made-up numbers, relevant format applied,
reports have owner + deadline + action items, professional and direct.
"""

def translate_to_english(text: str) -> str:
    replacements = {
        # CFO
        "CFO MRR Hareketi ve Gelir Analizi": "CFO MRR Movement & Revenue Analysis",
        "Durum: 🟢 Sağlıklı (Net Pozitif Büyüme)": "Status: 🟢 Healthy (Net Positive Growth)",
        "Aylık MRR Akış Tablosu (Mevcut Dönem)": "Monthly MRR Flow Table (Current Period)",
        "Başlangıç MRR (Beginning MRR)": "Beginning MRR",
        "Yeni Satış MRR (New Business)": "New Business MRR",
        "Genişleme MRR (Expansion)": "Expansion MRR",
        "Yeniden Aktivasyon MRR (Reactivation)": "Reactivation MRR",
        "Daralma MRR (Contraction)": "Contraction MRR",
        "Churn MRR (İptal)": "Churn MRR (Cancellation)",
        "Bitiş MRR (Ending MRR)": "Ending MRR",
        "Net Değişim & Büyüme Metrikleri": "Net Change & Growth Metrics",
        "Net MRR Değişimi": "Net MRR Change",
        "Net Gelir Elde Tutma (NRR)": "Net Revenue Retention (NRR)",
        "Brüt Gelir Elde Tutma (GRR)": "Gross Revenue Retention (GRR)",
        "Aksiyon Listesi": "Action List",
        "Churn analiz toplantısı": "Churn analysis meeting",
        "Sahip: CS & CFO": "Owner: CS & CFO",
        "Fiyat güncelleme onayı": "Price update approval",
        "Sahip: CEO & CFO": "Owner: CEO & CFO",
        "CFO Birim Ekonomi Analiz Raporu": "CFO Unit Economics Analysis Report",
        "Durum: 🟢 Mükemmel SaaS Metrikleri (LTV:CAC > 3x)": "Status: 🟢 Excellent SaaS Metrics (LTV:CAC > 3x)",
        "Birim Ekonomi Metrikleri": "Unit Economics Metrics",
        "Ortalama Müşteri Edinme Maliyeti (CAC)": "Average Customer Acquisition Cost (CAC)",
        "Ortalama Kullanıcı Başına Gelir (ARPU)": "Average Revenue Per User (ARPU)",
        "Brüt Kar Marjı (Gross Margin)": "Gross Margin",
        "Aylık Müşteri Kayıp Oranı (Churn)": "Monthly Customer Churn Rate (Churn)",
        "Müşteri Ömür Boyu Değeri (LTV)": "Customer Lifetime Value (LTV)",
        "Verimlilik Analizi": "Efficiency Analysis",
        "LTV:CAC Oranı": "LTV:CAC Ratio",
        "CAC Geri Ödeme Süresi (Payback Period)": "CAC Payback Period",
        "ay (🟢 Hızlı)": "months (🟢 Fast)",
        "Reklam CAC optimizasyonu briefi": "Ad CAC optimization brief",
        "Sahip: Performans & CFO": "Owner: Performance & CFO",
        "Yıllık plan indirim kampanyası": "Annual plan discount campaign",
        "Sahip: Growth & CFO": "Owner: Growth & CFO",
        "CFO Fiyatlandırma ve Paket Analizi": "CFO Pricing & Packaging Analysis",
        "Paket Yapısı: Tier-based (Starter / Pro / Enterprise)": "Package Structure: Tier-based (Starter / Pro / Enterprise)",
        "Paket Önerileri ve Karşılaştırma": "Package Recommendations & Comparison",
        "Starter Planı": "Starter Plan",
        "Mevcut conversion": "Current conversion",
        "Öneri: Fiyatı ₺390/ay yapıp limitleri daraltmak.": "Recommendation: Raise price to ₺390/month and narrow limits.",
        "Pro Planı (En Popüler)": "Pro Plan (Most Popular)",
        "Öneri: Yıllık ödemede %20 indirim sunmak.": "Recommendation: Offer 20% discount on annual payments.",
        "Enterprise Planı": "Enterprise Plan",
        "Öneri: Setup fee eklemek ve SLA taahhüdü vermek.": "Recommendation: Add setup fee and offer SLA commitment.",
        "Fiyatlandırma sayfasının A/B test planı": "Pricing page A/B test plan",
        "Sahip: Product & SEO": "Owner: Product & SEO",
        "CFO Gelir ve Gider Tablosu (P&L)": "CFO Profit and Loss Statement (P&L)",
        "Dönem: Q2 Tahmini Raporlama": "Period: Q2 Forecast Reporting",
        "Gelir / Gider Özeti": "Revenue / Expense Summary",
        "Toplam Brüt Gelir (Revenue)": "Total Gross Revenue (Revenue)",
        "Satılan Malın Maliyeti (COGS)": "Cost of Goods Sold (COGS)",
        "Brüt Kar (Gross Profit)": "Gross Profit",
        "Marj": "Margin",
        "Operasyonel Giderler (OpEx)": "Operating Expenses (OpEx)",
        "AWS maliyetlerinin optimizasyonu": "AWS costs optimization",
        "Sahip: CTO & CFO": "Owner: CTO & CFO",
        "CFO Runway & Burn Rate Raporu": "CFO Runway & Burn Rate Report",
        "Runway": "Runway",
        "Mevcut Kasa (Cash Balance)": "Cash Balance",
        "Aylık Net Burn Rate (Net Zarar)": "Monthly Net Burn Rate (Net Loss)",
        "Aylık Gelir (MRR)": "Monthly Revenue (MRR)",
        "Aylık Gider (OpEx)": "Monthly Expenses (OpEx)",
        "Senaryo Modelleri": "Scenario Models",
        "Statik (Mevcut Hız)": "Static (Current Speed)",
        "Tasarruf Modeli": "Savings Model",
        "Agresif Büyüme Modeli": "Aggressive Growth Model",
        "Kriz Senaryosu": "Crisis Scenario",
        "3rd party vendor giderlerinin denetimi": "Audit of 3rd party vendor expenses",
        "Sahip: CFO & CTO": "Owner: CFO & CTO",
        "Seri A yatırım turu hazırlık dosyası": "Series A investment round preparation file",
        "Sahip: CEO & CFO": "Owner: CEO & CFO",
        "ay": "months",
        "Sonsuz": "Infinite",
        "Plan yapmaya başla": "Start planning",
        "Yatırım turu başlat": "Start fundraising",
        "Kapatma kararı zamanı": "Time for shutdown decision",
        
        # Copywriter
        "Copywriter Çıktısı: Tagline Varyasyonları": "Copywriter Output: Tagline Variations",
        "Hedef Ürün": "Target Product",
        "Marka Tonu": "Brand Tone",
        "İstenen Varyasyon Sayısı": "Requested Number of Variations",
        "Varyasyon": "Variation",
        "Açıklama": "Description",
        "Hedef Kitle": "Target Audience",
        "kullanıcıları & yöneticileri": "users & managers",
        "Ton: Profesyonel, Güven Verici, Yenilikçi": "Tone: Professional, Trustworthy, Innovative",
        "En Gelir Getiren": "Highest Revenue Generating",
        "tescile uygun": "available for registration",
        "Copywriter Çıktısı: Headline A/B Test Havuzu": "Copywriter Output: Headline A/B Test Pool",
        "Sektör": "Sector",
        "A/B Test Headline Seçenekleri": "A/B Test Headline Options",
        "Yön A: Doğrudan Değer Önerisi (Value Prop)": "Direction A: Direct Value Proposition (Value Prop)",
        "Tüm süreçlerinizi tek ekranda toplayın ve zaman kazanın.": "Gather all your processes in one screen and save time.",
        "Yön B: Kayıp Odaklı (Loss Aversion / Pain Point)": "Direction B: Loss Aversion / Pain Point",
        "Manuel iş takibinde her ay kaç saat kaybediyorsunuz?": "How many hours do you lose each month on manual tracking?",
        "Dağınık araçlar yüzünden gözden kaçan detaylara son verin.": "Put an end to missed details due to scattered tools.",
        
        # Strateji
        "Strateji Direktörü Çıktısı: Yaratıcı Brief": "Strategy Director Output: Creative Brief",
        "Kime Konuşuyoruz (Who)": "Who We Are Talking To (Who)",
        "Ne Diyoruz (What)": "What We Are Saying (What)",
        "Niye İnansın (Why believe)": "Why Should They Believe It (Why believe)",
        "Hangi Hisle (How feel)": "With What Feeling (How feel)",
        "Ne Yapsın (Action)": "What Should They Do (Action)",
        "Mandatory'ler & Don'ts": "Mandatories & Don'ts",
        "Kanal Listesi & Format": "Channel List & Format",
        "Başarı Nasıl Ölçülür": "How Success is Measured",
        
        # General / Status / Fallback
        "Durum": "Status",
        "Öneri": "Recommendation",
        "Öneriler": "Recommendations",
        "Önerilen": "Recommended",
        "Aksiyon": "Action",
        "Termin": "Deadline",
        "Sahip": "Owner",
    }
    
    translated = text
    for tr_str, en_str in replacements.items():
        translated = translated.replace(tr_str, en_str)
        
    return translated

def log_agent_action(agent: str, komut: str, gorev: str):
    """Ajanın aktivitesini web arayüzü için log dosyasına kaydeder."""
    status_file = Path(__file__).parent.parent / "agent_status.json"
    status = {"active_agent": None, "history": []}
    
    if status_file.exists():
        try:
            status = json.loads(status_file.read_text(encoding="utf-8"))
        except:
            pass
            
    timestamp = time.time()
    status["active_agent"] = agent
    status["command"] = komut
    status["task"] = gorev
    status["timestamp"] = timestamp
    
    history_item = {
        "agent": agent,
        "command": komut,
        "task": gorev,
        "timestamp": timestamp
    }
    status.setdefault("history", []).insert(0, history_item)
    status["history"] = status["history"][:20]  # Son 20 logu sakla
    
    try:
        status_file.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    except:
        pass

def get_agent_name(komut: str) -> str:
    """Komutun ilk kelimesine göre ilgili ajanı eşleştirir."""
    if not komut:
        return "CEO / Ürün"
    first = komut.strip().split()[0].lower()
    if not first.startswith("/"):
        first = "/" + first
    return COMMAND_TO_AGENT.get(first, "CEO / Ürün")

class WorkflowManager:
    def __init__(self, references_dir: Path = None):
        if references_dir is None:
            self.references_dir = Path(__file__).parent.parent / "references"
        else:
            self.references_dir = Path(references_dir)

    def load_reference(self, slug: str, lang: str = "tr") -> str:
        """Referans markdown dosyasını oku."""
        SLUG_MAP_EN = {
            "strateji-marka": "strategy-brand",
            "yaratici-ekip": "creative-team",
            "pazarlama-buyume": "marketing-growth",
            "musteri-operasyon": "client-operations",
            "analitik-urun-teknik": "analytics-product-tech",
        }
        if lang == "en":
            filename = f"{SLUG_MAP_EN.get(slug, slug)}.md"
        else:
            filename = f"{slug}.md"
            
        path = self.references_dir / filename
        if not path.exists():
            path = self.references_dir / f"{slug}.md"
        if not path.exists():
            return f"[HATA] Referans dosyası bulunamadı: {filename}"
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            return f"[HATA] Referans dosyası okunurken hata oluştu: {str(e)}"

    def resolve_command(self, komut: str) -> str | None:
        """Bir komutu (ör. '/copy tagline') referans slug'ına çöz."""
        if not komut:
            return None
        first = komut.strip().split()[0].lower()
        if not first.startswith("/"):
            first = "/" + first
        return COMMAND_MAP.get(first)

    def get_workflow(self, komut: str, gorev: str = "", log_action: bool = True, lang: str = "tr") -> str:
        """ADA ajans workflow'unu çalıştırmak için gereken talimat ve formatı döndürür."""
        slug = self.resolve_command(komut)

        if slug is None:
            if lang == "en":
                return (
                    f"'{komut}' could not be resolved to a known ADA command.\n\n"
                    "Call the 'ada_komutlar' tool to see the list of commands. "
                    "Command format: /strateji, /marka, /copy, /art, /yapim, /performans, /seo-altyapisi, "
                    "/email, /growth, /sosyal, /icerik, /influencer, /medya, /hesap, /proje, "
                    "/cs, /kriz, /pr, /analitik, /cfo, /ceo, /cto, /cos, /intel, /mudur"
                )
            return (
                f"'{komut}' bilinen bir ADA komutuna eşlenemedi.\n\n"
                "Komut listesini görmek için 'ada_komutlar' aracını çağır. "
                "Komut formatı: /strateji, /marka, /copy, /art, /yapim, /performans, /seo-altyapisi, "
                "/email, /growth, /sosyal, /icerik, /influencer, /medya, /hesap, /proje, "
                "/cs, /kriz, /pr, /analitik, /cfo, /ceo, /cto, /cos, /intel, /mudur"
            )

        if log_action:
            agent_name = get_agent_name(komut)
            log_agent_action(agent_name, komut, gorev)

        reference = self.load_reference(slug, lang=lang)
        
        if lang == "en":
            baglam = f"\n## TASK CONTEXT\n{gorev}\n" if gorev.strip() else ""
            rules = BEHAVIOR_RULES_EN
            title = REFERENCE_TITLES_EN.get(slug, slug)
            return (
                f"{rules}\n"
                f"---\n"
                f"## ACTIVE FIELD: {title}\n"
                f"## EXECUTED COMMAND: {komut}\n"
                f"{baglam}"
                f"---\n"
                f"## REFERENCE KNOWLEDGE BASE\n\n{reference}\n\n"
                f"---\n"
                f"Generate the output NOW using the format belonging to the '{komut}' command above. "
                "First state which mode you are running, then proceed directly to the output."
            )
        else:
            baglam = f"\n## GÖREV BAĞLAMI\n{gorev}\n" if gorev.strip() else ""
            rules = BEHAVIOR_RULES
            title = REFERENCE_TITLES.get(slug, slug)
            return (
                f"{rules}\n"
                f"---\n"
                f"## AKTİF ALAN: {title}\n"
                f"## ÇALIŞTIRILAN KOMUT: {komut}\n"
                f"{baglam}"
                f"---\n"
                f"## REFERANS BİLGİ TABANI\n\n{reference}\n\n"
                f"---\n"
                f"Yukarıdaki '{komut}' komutuna ait formatı kullanarak çıktıyı ŞİMDİ üret. "
                f"Önce hangi modu çalıştırdığını belirt, sonra doğrudan çıktıya geç."
            )

    def get_commands_list(self) -> list:
        """Tüm komutları ve ait oldukları alanları döndürür."""
        by_slug = {}
        for cmd, slug in COMMAND_MAP.items():
            by_slug.setdefault(slug, []).append(cmd)
        
        result = []
        for slug, title in REFERENCE_TITLES.items():
            result.append({
                "slug": slug,
                "title": title,
                "commands": sorted(by_slug.get(slug, []))
            })
        return result

    def extract_context(self, task: str, command: str) -> dict:
        ctx = {
            "product": "ADA Projesi",
            "industry": "SaaS",
            "keywords": [],
            "command": command.lower().strip() if command else "",
            "task": task.strip() if task else "",
            "variations": 3,
            "format": "standard"
        }
        
        if not task:
            return ctx
            
        task_lower = task.lower()
        parts = [p.strip() for p in task.split(",") if p.strip()]
        if parts:
            ctx["product"] = parts[0]
        
        industries = {
            "fintech": ["fintech", "finance", "finans", "para", "bank", "ödeme", "payment", "crypto", "kripto", "investment", "yatırım"],
            "healthtech": ["health", "healthtech", "sağlık", "medikal", "doctor", "hastane", "tıp"],
            "e-commerce": ["e-ticaret", "e-commerce", "market", "shop", "satış", "retail", "perakende", "store"],
            "hr-tech": ["hr", "human resources", "insan kaynakları", "onboarding", "recruit", "işe alım"],
            "ed-tech": ["edtech", "education", "eğitim", "okul", "öğrenci", "course", "ders"],
            "ai-tech": ["ai", "artificial intelligence", "yapay zeka", "llm", "gpt", "model", "makine öğrenmesi", "ml"],
            "b2b-saas": ["saas", "b2b", "crm", "dashboard", "b2b saas", "yazılım", "software"]
        }
        
        for ind, terms in industries.items():
            if any(t in task_lower for t in terms):
                ctx["industry"] = ind
                break
                
        var_match = re.search(r'(\d+)\s*(?:variation|varyasyon|adet|tane|kopya)', task_lower)
        if var_match:
            ctx["variations"] = int(var_match.group(1))
            
        fmt_match = re.search(r'--format=(\S+)', ctx["command"])
        if fmt_match:
            ctx["format"] = fmt_match.group(1)
            
        return ctx

    def generate_agent_output(self, agent_slug: str, name: str, command: str, task: str, lang: str = "tr") -> str:
        raw_output = self._generate_raw_output(agent_slug, name, command, task)
        if lang == "en":
            return translate_to_english(raw_output)
        return raw_output

    def _generate_raw_output(self, agent_slug: str, name: str, command: str, task: str) -> str:
        ctx = self.extract_context(task, command)
        cmd = ctx["command"]
        prod = ctx["product"]
        ind = ctx["industry"]
        num = ctx["variations"]

        if agent_slug == 'cfo':
            if "mrr" in cmd:
                new_mrr = random.randint(15, 60) * 1000
                exp_mrr = random.randint(5, 20) * 1000
                react_mrr = random.randint(1, 5) * 1000
                contraction_mrr = random.randint(2, 8) * 1000
                churn_mrr = random.randint(3, 12) * 1000
                start_mrr = random.randint(100, 500) * 1000
                net_change = new_mrr + exp_mrr + react_mrr - contraction_mrr - churn_mrr
                end_mrr = start_mrr + net_change
                nrr = ((start_mrr + exp_mrr - contraction_mrr - churn_mrr) / start_mrr) * 100
                grr = ((start_mrr - contraction_mrr - churn_mrr) / start_mrr) * 100
                return f"""# CFO MRR Hareketi ve Gelir Analizi: {prod}
                
Durum: 🟢 Sağlıklı (Net Pozitif Büyüme)

## Aylık MRR Akış Tablosu (Mevcut Dönem)
- **Başlangıç MRR (Beginning MRR):** ₺{start_mrr:,}
- **(+) Yeni Satış MRR (New Business):** ₺{new_mrr:,}
- **(+) Genişleme MRR (Expansion):** ₺{exp_mrr:,}
- **(+) Yeniden Aktivasyon MRR (Reactivation):** ₺{react_mrr:,}
- **(-) Daralma MRR (Contraction):** -₺{contraction_mrr:,}
- **(-) Churn MRR (İptal):** -₺{churn_mrr:,}
- **Bitiş MRR (Ending MRR):** ₺{end_mrr:,}

## Net Değişim & Büyüme Metrikleri
- **Net MRR Değişimi:** ₺{net_change:+,} (%{round((net_change/start_mrr)*100, 2):+,})
- **Net Gelir Elde Tutma (NRR):** %{round(nrr, 1)}
- **Brüt Gelir Elde Tutma (GRR):** %{round(grr, 1)}

## Aksiyon Listesi
- [ ] Churn analiz toplantısı | Sahip: CS & CFO | Term: 10.06.2026
- [ ] Fiyat güncelleme onayı | Sahip: CEO & CFO | Term: 15.06.2026"""

            elif "birim" in cmd or "ekonomi" in cmd:
                cac = random.randint(150, 450)
                arpu = random.randint(35, 120)
                gross_margin = random.randint(72, 89)
                churn_rate = round(random.uniform(1.2, 3.8), 2)
                ltv = int((arpu * (gross_margin / 100)) / (churn_rate / 100))
                ltv_cac = round(ltv / cac, 2)
                payback = round(cac / (arpu * (gross_margin / 100)), 1)
                return f"""# CFO Birim Ekonomi Analiz Raporu: {prod}

Durum: 🟢 Mükemmel SaaS Metrikleri (LTV:CAC > 3x)

## Birim Ekonomi Metrikleri
- **Ortalama Müşteri Edinme Maliyeti (CAC):** ₺{cac:,}
- **Ortalama Kullanıcı Başına Gelir (ARPU):** ₺{arpu:,}
- **Brüt Kar Marjı (Gross Margin):** %{gross_margin}
- **Aylık Müşteri Kayıp Oranı (Churn):** %{churn_rate}
- **Müşteri Ömür Boyu Değeri (LTV):** ₺{ltv:,}

## Verimlilik Analizi
- **LTV:CAC Oranı:** {ltv_cac}x (🟢 Sağlıklı)
- **CAC Geri Ödeme Süresi (Payback Period):** {payback} ay (🟢 Hızlı)

## Aksiyon Listesi
- [ ] Reklam CAC optimizasyonu briefi | Sahip: Performans & CFO | Term: 12.06.2026
- [ ] Yıllık plan indirim kampanyası | Sahip: Growth & CFO | Term: 18.06.2026"""

            elif "fiyat" in cmd:
                return f"""# CFO Fiyatlandırma ve Paket Analizi: {prod}

Paket Yapısı: Tier-based (Starter / Pro / Enterprise)

## Paket Önerileri ve Karşılaştırma
- **Starter Planı:** ₺290/ay (Mevcut conversion: %4.2, Churn: %5.1) -> Öneri: Fiyatı ₺390/ay yapıp limitleri daraltmak.
- **Pro Planı (En Popüler):** ₺890/ay (Mevcut conversion: %2.8, Churn: %1.8) -> Öneri: Yıllık ödemede %20 indirim sunmak.
- **Enterprise Planı:** ₺4,500+/ay (Mevcut conversion: %0.4) -> Öneri: Setup fee eklemek ve SLA taahhüdü vermek.

## Aksiyon Listesi
- [ ] Fiyatlandırma sayfasının A/B test planı | Sahip: Product & SEO | Term: 14.06.2026"""

            elif "p-and-l" in cmd or "profit" in cmd or "gelir-gider" in cmd:
                rev = random.randint(200, 800) * 1000
                cogs = int(rev * random.uniform(0.12, 0.22))
                gp = rev - cogs
                opex = int(gp * random.uniform(0.55, 0.78))
                ebitda = gp - opex
                return f"""# CFO Gelir ve Gider Tablosu (P&L): {prod}

Dönem: Q2 Tahmini Raporlama

## Gelir / Gider Özeti
- **Toplam Brüt Gelir (Revenue):** ₺{rev:,}
- **Satılan Malın Maliyeti (COGS):** ₺{cogs:,}
- **Brüt Kar (Gross Profit):** ₺{gp:,} (Marj: %{round((gp/rev)*100, 1)})
- **Operasyonel Giderler (OpEx):** ₺{opex:,}
- **EBITDA:** ₺{ebitda:,} (Marj: %{round((ebitda/rev)*100, 1)})

## Aksiyon Listesi
- [ ] AWS maliyetlerinin optimizasyonu | Sahip: CTO & CFO | Term: 11.06.2026"""

            else:
                cash = random.randint(80, 450) * 10000
                burn = random.randint(30, 150) * 1000
                mrr = random.randint(15, 80) * 5000
                opex = mrr + burn
                runway_months = cash / burn if burn > 0 else float('inf')
                runway_str = f"{runway_months:.1f} ay" if burn > 0 else "Sonsuz"
                status_dot = "🟢 Sağlıklı" if runway_months >= 18 else "🟡 Plan yapmaya başla" if runway_months >= 12 else "🟠 Yatırım turu başlat" if runway_months >= 6 else "🔴 Kapatma kararı zamanı"
                return f"""# CFO Runway & Burn Rate Raporu: {prod}

Durum: {status_dot} (Runway: {runway_str})

## Finansal Metrikler (Mevcut Durum)
- **Mevcut Kasa (Cash Balance):** ₺{cash:,}
- **Aylık Net Burn Rate (Net Zarar):** ₺{burn:,}
- **Aylık Gelir (MRR):** ₺{mrr:,}
- **Aylık Gider (OpEx):** ₺{opex:,}

## Senaryo Modelleri
1. **Statik (Mevcut Hız):** Runway {runway_str}
2. **%20 Tasarruf Modeli:** Net burn ₺{int(burn*0.8):,}, Runway {cash/(burn*0.8):.1f} ay
3. **Agresif Büyüme Modeli:** Net burn ₺{int(burn*0.7):,}, Runway {cash/(burn*0.7):.1f} ay
4. **Kriz Senaryosu:** Net burn ₺{int(burn*1.5):,}, Runway {cash/(burn*1.5):.1f} ay

## Aksiyon Listesi
- [ ] 3rd party vendor giderlerinin denetimi | Sahip: CFO & CTO | Term: 15.06.2026
- [ ] Seri A yatırım turu hazırlık dosyası | Sahip: CEO & CFO | Term: 01.07.2026"""

        elif agent_slug == 'copywriter':
            fintech_slogans = [
                ("Finansal Özgürlüğün Yeni Nesil Pusulası.", "Paranızın kontrolü tamamen sizde. Hızlı, şeffaf, güvenli."),
                ("Akıllı Yatırım, Sıfır Karmaşa.", "Yapay zeka destekli portföy yönetimi cebinizde."),
                ("Girişimler İçin Akıllı Bütçe Yönetimi.", "Giderlerinizi anlık izleyin, büyümeye odaklanın."),
                ("Geleceğin Finans Altyapısı.", "Tek API ile tüm bankacılık işlemlerinizi entegre edin."),
                ("Komisyonsuz, Hızlı ve Küresel Ödemeler.", "Sınırları aşın, paranuzu özgür bırakın.")
            ]
            health_slogans = [
                ("Sağlığınız İçin Dijital Yol Arkadaşınız.", "Randevular, tahliller ve doktorunuz tek ekranda."),
                ("Sağlıklı Yaşama Bilimsel Yaklaşım.", "Kişiselleştirilmiş beslenme ve antrenman planları."),
                ("Zihinsel Sağlığınız İçin Güvenli Liman.", "Online terapi ve meditasyon seansları cebinizde."),
                ("Kronik Hastalıklarda Yeni Nesil Takip.", "Değerlerinizi yapay zeka ile izleyin, riskleri azaltın.")
            ]
            ai_slogans = [
                ("İşinizi Otomatize Edin, Zaman Kazanın.", "Yapay zeka asistanınız sıkıcı işleri saniyeler içinde çözer."),
                ("Yapay Zeka ile Verileriniz Konuşsun.", "Büyük veri yığınlarını dakikalar içinde iş raporlarına dönüştürün."),
                ("Geleceğin Kod Yazım Deneyimi.", "AI co-pilot ile 10 kat daha hızlı, temiz ve hatasız kodlayın."),
                ("Müşteri İlişkilerinde AI Devrimi.", "7/24 kesintisiz, insan kalitesinde akıllı chatbot desteği.")
            ]
            ecommerce_slogans = [
                ("E-Ticarette Başarıyı Otomatize Edin.", "Stok, kargo ve sipariş yönetimi tek platformda."),
                ("Küresel Pazarlara Açılmanın En Kolay Yolu.", "Yerel ödeme yöntemleri ve gümrük entegrasyonu dahil."),
                ("Müşterilerinizi Sadık Alıcılara Dönüştürün.", "Yapay zeka destekli kişiselleştirilmiş ürün önerileri.")
            ]
            saas_slogans = [
                ("Takım Çalışmasında Karmaşaya Son.", "Görevler, dökümanlar ve chat tek bir merkezde sync."),
                ("Büyüyen Ekipler İçin Süreç Yönetimi.", "Operasyonunuzu standardize edin, hata oranını sıfırlayın."),
                ("Müşteri Adaylarınızı Gelire Dönüştürün.", "CRM platformunuzu 5 dakikada kurun, satışları takip edin.")
            ]
            
            if ind == "fintech": slogans_pool = fintech_slogans
            elif ind == "healthtech": slogans_pool = health_slogans
            elif ind == "ai-tech": slogans_pool = ai_slogans
            elif ind == "e-commerce": slogans_pool = ecommerce_slogans
            else: slogans_pool = saas_slogans
            
            num = min(num, len(slogans_pool))
            selected_slogans = random.sample(slogans_pool, num)
            
            if "tagline" in cmd:
                taglines_md = ""
                for idx, (tag, desc) in enumerate(selected_slogans):
                    taglines_md += f"### Varyasyon {idx+1}: {tag}\n- **Açıklama:** {desc}\n- **Hedef Kitle:** {ind.title()} kullanıcıları & yöneticileri\n- **Ton:** Profesyonel, Güven Verici, Yenilikçi\n\n"
                return f"""# Copywriter Çıktısı: Tagline Varyasyonları ({prod})

Hedef Ürün: **{prod}**
Marka Tonu: **Yenilikçi & Etkileyici**
İstenen Varyasyon Sayısı: **{num}**

{taglines_md}
## Metrikler & Değerlendirme
- **En Gelir Getiren:** "{selected_slogans[0][0]}"
- **Domain/Handle:** {prod.lower().replace(" ", "").replace("-", "")}.co tescile uygun."""

            elif "headline" in cmd:
                return f"""# Copywriter Çıktısı: Headline A/B Test Havuzu ({prod})

Hedef Ürün: **{prod}** (Sektör: {ind.title()})

## A/B Test Headline Seçenekleri

### Yön A: Doğrudan Değer Önerisi (Value Prop)
1. **"{selected_slogans[0][0]}"**
2. **"Tüm süreçlerinizi tek ekranda toplayın ve zaman kazanın."**

### Yön B: Kayıp Odaklı (Loss Aversion / Pain Point)
3. **"Manuel iş takibinde her ay kaç saat kaybediyorsunuz?"**
4. **"Dağınık araçlar yüzünden gözden kaçan detaylara son verin."**

## Önerilen Aksiyon Planı
- [ ] Top 3 seçeneğin Google Search Ads A/B testine alınması | Sahip: Performans Pazarlama | Term: 10.06.2026"""

            elif "body" in cmd or "copy" in cmd:
                return f"""# Copywriter Çıktısı: Landing Page Body Copy ({prod})

İçerik Formülü: **PAS (Problem - Agitation - Solution)**

---

### 1. Problem (Acı Noktası)
Günümüzde ekipler işleri takip etmek için ortalama 6 farklı araç kullanıyor. Slack mesajları, Trello kartları, Excel dosyaları ve e-postalar arasında kaybolmak, kritik teslim tarihlerinin kaçmasına ve ekibin motivasyonunun düşmesine neden oluyor.

### 2. Agitation (Derinleştirme)
Daha da kötüsü, kimin ne yaptığını bilmemek mikro-yönetimi tetikliyor. Durum toplantıları saatler sürüyor, ancak toplantı bitiminde herkesin aklı hala karışık.

### 3. Solution (Çözüm)
İşte bu yüzden **{prod}**'u geliştirdik. 
{prod}, tüm iletişim, görev yönetimi ve raporlama süreçlerini tek bir şık arayüzde birleştiren akıllı çalışma alanıdır.

---

## Call To Action (CTA) Alternatifleri
- *CTA 1:* "14 Gün Ücretsiz Deneyin (Kredi Kartı Gerekmez)"
- *CTA 2:* "Hemen Ücretsiz Hesap Oluşturun"
"""

            elif "script" in cmd:
                return f"""# Copywriter Çıktısı: 30 Saniyelik Reklam Scripti ({prod})

Format: **TikTok / Instagram Reels (9:16) Video Scripti**

| Süre (Sn) | Görüntü (Visual) | Ses / Dış Ses (Audio) | Alt Yazı (On-Screen Text) |
|-----------|------------------|-----------------------|---------------------------|
| 00:00 - 00:05 | Dağınık bir ofiste, bilgisayar ekranına sinirle bakan bir çalışan yakın çekim. | "Yine mi teslim tarihi kaçtı? E-postalar arasında kaybolmaktan bıkmadınız mı?" | İş takibinde kaybolanlara... 🤯 |
| 00:05 - 00:15 | Çalışanın {prod} ekranını açtığı ve tek tıkla tüm işleri düzenlediği ekran kaydı. | "Artık dağınıklığa son. {prod} ile tüm projelerinizi tek ekranda organize edin." | {prod} ile tanışın! 🚀 |
| 00:15 - 00:30 | Ekranda {prod} logosu ve CTA butonu belirir. | "{prod}'u hemen ücretsiz deneyin. Link profilde!" | Şimdi ücretsiz dene! |
"""

            else:
                return f"""# Copywriter Çıktısı: LinkedIn Lansman Postu ({prod})

Hedef Kitle: **Kurucular, Ürün Müdürleri ve Operasyon Yöneticileri**

---

### LinkedIn Gönderi Varyantı

"Dağınık araçlar, kaybolan görevler ve bitmek bilmeyen durum toplantıları... 🤯

Ekipler büyüdükçe koordinasyonu sağlamak bir kabusa dönüşebiliyor. Yapılan araştırmalara göre, beyaz yakalı çalışanlar zamanlarının %60'ını 'iş hakkında iş yapmaya' harcıyor.

İşte tam da bu verimsizliği ortadan kaldırmak için **{prod}**'u tasarladık! 🚀

{prod} ile:
✅ Tüm projelerinizi tek merkezden yönetin.
✅ Durum güncellemelerini otomatikleştirin.

#ProjeYönetimi #Verimlilik #{prod.replace(" ", "")}"""

        elif agent_slug == 'strateji-direktoru':
            if "brief" in cmd:
                return f"""# Yaratıcı Brief: {prod} Lansman Kampanyası

Hazırlayan: **Strateji Direktörü**  
Müşteri / Ürün: **{prod}** ({ind.upper()})

## 1. Kampanya Amacı (Why)
{prod} markasının pazardaki varlığını duyurmak, hedef kitleye sunduğu temel değer önerisini net bir şekilde aktarmak ve ilk 1000 aktif kullanıcı edinimini desteklemek.

## 2. Hedef Kitle (Who)
- **Birincil Kitle:** {ind.title()} sektöründeki erken benimseyiciler (Early Adopters), kurucular ve departman liderleri.
- **Demografi:** 25-45 yaş arası teknoloji profesyonelleri, uzaktan çalışan ekipler.

## 3. Temel Mesaj (What)
"**{prod} ile iş akışınızı sadeleştirin, ekibinize odaklanın.**"

## 4. Ton ve Stil (How Feel)
- Profil: Güven Verici ama Sıkıcı Olmayan
- Karakter: Yenilikçi, Net, Hızlı ve Çözüm Odaklı

## Aksiyon Maddeleri
- [ ] Copywriter ile headline türetme seansı | Sahip: Strateji & Copywriter | Term: 12.06.2026
- [ ] Tasarım ekibine key visual brief iletimi | Sahip: Strateji & Art Director | Term: 14.06.2026"""

            elif "konsept" in cmd:
                return f"""# Yaratıcı Konsept Yönleri: {prod} Lansmanı

Durum: 🟡 Değerlendirme Aşamasında (Müşteri Seçimi Bekleniyor)

---

### Yön 1: "Sessiz Verimlilik" (Minimalist Yaklaşım)
- **Ana Fikir:** Arka planda işleri çözen, sizi bildirim bombardımanına tutmayan akıllı asistan.
- **Manifesto Sloganı:** "Bırakın {prod} çalışsın, siz işinize odaklanın."

### Yön 2: "Ofis Devrimi" (Cesur & İsyankar Yaklaşım)
- **Ana Fikir:** Eski nesil, hantal ve karmaşık kurumsal araçlara karşı ilan edilen savaş.
- **Manifesto Sloganı:** "Eski kuralları unutun. Yeni nesil çalışma burada."

## Aksiyon Listesi
- [ ] Konsept sunumu toplantısı | Sahip: Strateji & Müşteri İlişkileri | Term: 10.06.2026"""

            else:
                return f"""# Strateji QC (Kalite Kontrol) Raporu: {prod}

Değerlendiren: **Strateji Direktörü**

## 7-Boyut Kalite Değerlendirmesi
1. **Brief Uyumu:** 🟢 %95
2. **Marka Tutarlılığı:** 🟢 %90
3. **Çapraz Tutarlılık (Copy + Art):** 🟡 %80
4. **Büyük Fikir Bağlılığı:** 🟢 %100
5. **Hedef Kitle Rezonansı:** 🟢 %90
6. **Yaratıcı Cesaret:** 🟡 %75
7. **Ölçülebilirlik:** 🟢 %95

## Sonuç: 🟢 Onaylandı (Ufak revizeler sonrası sunuma hazır)"""

        elif agent_slug == 'cto':
            tech_stack = "PostgreSQL & Redis"
            if "postgres" in task.lower() or "db" in task.lower(): tech_stack = "Postgres Read Replica"
            elif "redis" in task.lower() or "cache" in task.lower(): tech_stack = "Redis Cluster Cache"
            elif "aws" in task.lower() or "lambda" in task.lower(): tech_stack = "AWS Lambda Serverless"
            elif "graphql" in task.lower(): tech_stack = "GraphQL Gateway"
            debt_score = random.randint(12, 28)
            
            return f"""# CTO Mimari Karar Belgesi (ADR-12): {prod}

Durum: 🟢 Kabul Edildi (Type 2 Karar - Geri Dönülebilir)  
Teknoloji Seçimi: **{tech_stack}**

## 1. Bağlam ve Sorun Tanımı
{prod} uygulamasının artan kullanıcı yükü ve veri trafiği nedeniyle mevcut altyapıda performans darboğazları yaşanmaktadır.

## 2. Alınan Karar
Sistemin ölçeklenebilirliğini artırmak amacıyla mimariye **{tech_stack}** yapısının dahil edilmesine karar verilmiştir.

## 3. Teknik Borç Envanteri
- **Eski altyapı kodlarının refaktör edilmesi:** (Teknik Borç Skoru: {debt_score} - Bu çeyrek)
- **Yeni entegrasyon test otomasyonları:** (Teknik Borç Skoru: 8 - Backlog)

## Aksiyon Listesi
- [ ] DevOps ortamında cluster kurulumu | Sahip: CTO & DevOps | Term: 15.06.2026"""

        elif agent_slug == 'seo':
            lcp = round(random.uniform(1.6, 3.4), 2)
            cls = round(random.uniform(0.01, 0.22), 3)
            health = random.randint(82, 98)
            lcp_status = "🔴 Kötü" if lcp > 2.5 else "🟢 İyi"
            cls_status = "🔴 Kötü" if cls > 0.1 else "🟢 İyi"
            return f"""# SEO Core Web Vitals Raporu: {prod}

Durum: { '🔴 Kritik İyileştirme Gerekli' if lcp > 2.5 or cls > 0.1 else '🟢 Sorunsuz / Launch' } (Genel Site Health: {health}/100)

## Core Web Vitals Metrik Değerleri
- **LCP (Largest Contentful Paint):** {lcp}s ({lcp_status})
- **CLS (Cumulative Layout Shift):** {cls} ({cls_status})
- **FID / INP:** {random.randint(80, 240)}ms (🟢 İyi)

## Aksiyon Listesi
- [ ] Hero görsellerinin WebP formatına çevrilmesi | Sahip: Art Director & Frontend | Term: 12.06.2026"""

        elif agent_slug == 'art-director':
            return f"""# Art Director Tasarım Sistemi & Key Visual Rehberi: {prod}

Durum: 🟢 Kurumsal Kimlik Onaylandı

## 1. Tasarım Dili ve Konsept
{prod} için modern, minimalist ve karanlık mod odaklı bir arayüz tasarımı hedeflenmiştir.

## 2. Renk Paleti (Palette)
- **Primary (Ana Renk):** `#6c5ce7` (Neon Mor - Enerjik ve Modern)
- **Secondary (Destek Renk):** `#0e1018` (Gece Mavisi - Arka Plan)
- **Accent (Vurgu Rengi):** `#34d399` (Vurgu Yeşili)

## Aksiyon Listesi
- [ ] Landing page UI Figma çizimi | Sahip: Art & UI/UX | Term: 12.06.2026"""

        elif agent_slug == 'yapimci':
            pre_prod = random.randint(15, 35) * 1000
            prod_cost = random.randint(45, 90) * 1000
            post_prod = random.randint(20, 45) * 1000
            total = pre_prod + prod_cost + post_prod
            return f"""# Yapımcı Reklam Prodüksiyon Bütçe Planı: {prod}

Proje: **30 Saniyelik Tanıtım Filmi Prodüksiyonu**  
Durum: 🟡 Teklif Aşamasında

## Bütçe Kalemleri Detay Tablosu

| Aşama / Kalem | Açıklama | Maliyet |
|---------------|----------|---------|
| **Pre-Prodüksiyon** | Senaryo yazımı, storyboard çizimi ve kast seçimi. | ₺{pre_prod:,} |
| **Prodüksiyon (Çekim)** | Ekipman kiralama, stüdyo ücreti, oyuncu kaşeleri. | ₺{prod_cost:,} |
| **Post-Prodüksiyon** | Kurgu, renk derecelendirme (grading), ses miksajı. | ₺{post_prod:,} |
| **TOPLAM BÜTÇE** | **Yapım bütçesi toplamı.** | **₺{total:,}** |

## Aksiyon Listesi
- [ ] Kast adaylarının portfolyo sunumu | Sahip: Yapımcı & Kreatif | Term: 11.06.2026"""

        elif agent_slug == 'performans-pazarlama':
            impressions = random.randint(80, 250) * 1000
            clicks = int(impressions * random.uniform(0.015, 0.038))
            conversions = int(clicks * random.uniform(0.05, 0.12))
            spend = random.randint(15, 45) * 1000
            cpc = round(spend / clicks, 2)
            cpa = round(spend / conversions, 2)
            roas = round(random.uniform(2.8, 5.2), 1)
            return f"""# Performans Pazarlama Raporu: {prod}

Durum: 🟢 Aktif ve Optimize Ediliyor

## Kampanya Performans Metrikleri
- **Toplam Gösterim (Impressions):** {impressions:,}
- **Tıklama Sayısı (Clicks):** {clicks:,} (CTR: %{round((clicks/impressions)*100, 2)})
- **Dönüşüm Sayısı (Conversions):** {conversions:,}
- **Harcanan Bütçe:** ₺{spend:,}
- **Tıklama Başı Maliyet (CPC):** ₺{cpc}
- **Dönüşüm Başı Maliyet (CPA):** ₺{cpa}
- **Yatırım Getirisi (ROAS):** {roas}x

## Aksiyon Listesi
- [ ] Negatif anahtar kelimelerin ayıklanması | Sahip: Performans Paz. | Term: 09.06.2026"""

        elif agent_slug == 'e-posta-crm':
            return f"""# E-posta / CRM Hoş Geldin Otomasyon Serisi: {prod}

Durum: 🟢 Taslak Hazır

## E-posta Akışı & Gönderim Kuralları

### Mail 1: Üye Girişinden Hemen Sonra
- **Konu Satırı:** {prod} Dünyasına Hoş Geldiniz! 🚀
- **CTA:** "Hemen Kuruluma Başla"

### Mail 2: Kayıttan 2 Gün Sonra
- **Konu Satırı:** {prod} ile İlk Görevinizi Oluşturdunuz mu? 💡

## Aksiyon Listesi
- [ ] HTML şablonlarının CRM sistemine entegrasyonu | Sahip: CRM Uzmanı | Term: 13.06.2026"""

        elif agent_slug == 'proje-yoneticisi':
            return f"""# Proje Yönetim Planı & Yol Haritası: {prod}

Proje Sahibi: **Proje Yöneticisi**  
Durum: 🟢 Zamanında İlerliyor

## Proje Fazları ve Milestone Takvimi
- **Faz 1:** Strateji ve brief süreçlerinin tamamlanması (🟢 Tamamlandı)
- **Faz 2:** Figma UI/UX arayüz çizimi (🚧 Devam Ediyor)
- **Faz 3:** Frontend & Backend API entegrasyonları (⏳ Beklemede)
- **Faz 4:** Lansman öncesi QA testleri (⏳ Beklemede)

## Aksiyon Listesi
- [ ] Haftalık ilerleme raporunun iletimi | Sahip: Proje Yöneticisi | Term: Her Cuma"""

        elif agent_slug == 'pr':
            return f"""# PR Basın Bülteni: {prod} Lansmanı

Durum: 🟢 Basın Açıklaması Hazır

---

### BASIN BÜLTENİ: YENİ NESİL ÇALIŞMA PLATFORMU {prod.upper()} LANSMANINI DUYURDU!

**İSTANBUL, 05.06.2026** — Ekiplerin verimliliğini ve iş birliğini artırmak üzere tasarlanan yenilikçi bulut tabanlı platform **{prod}**, bugün resmi lansmanını gerçekleştirdi.

---

## Editöre Notlar & İletişim
- **Kurumsal Websitesi:** www.{prod.lower().replace(" ", "").replace("-", "")}.co
- **PR İletişim Yetkilisi:** pr@{prod.lower().replace(" ", "").replace("-", "")}.co"""

        elif agent_slug == 'analitik':
            return f"""# Analitik Veri Raporu: {prod} Performansı

Durum: 🟢 GA4 Veri Taksonomisi Sorunsuz Çalışıyor

## 3-Tier KPI Tablosu
- **Tier 1 (North Star):** MAU: 12,450 / Hedef: 10,000 (🟢 Hedef Aşılmış)
- **Tier 2 (İş Sağlığı):** Signup Churn: %14.2 / Hedef: %15.0 (🟢 Güvenli Bölge)
- **Tier 3 (Operasyonel):** LinkedIn CTR: %2.85 (🟢 Başarılı)

## Aksiyon Listesi
- [ ] Telefon numarası alanının opsiyonel yapılması | Sahip: Dev & Analitik | Term: 10.06.2026"""

        elif agent_slug == 'musteri-basarisi':
            return f"""# Müşteri Başarısı (CS) Sağlık Skoru Raporu: {prod}
 
Durum: 🟢 Müşteri Sağlığı İyi (Yeşil Hat)
 
## Müşteri Memnuniyet Skoru Detayları
- **NPS (Net Promoter Score):** 8.8/10 (🟢 Benchmark Üstü)
- **İlk Yanıt Verme Süresi (FRT):** 14 Dakika (Hedef: <20 Dk)
- **Ortalama Çözüm Süresi:** 2.4 Saat
 
## Aksiyon Listesi
- [ ] Faturalandırma FAQ dökümanının güncellenmesi | Sahip: CS Ekip Lideri | Term: 11.06.2026"""

        elif agent_slug == 'marka-stratejisti':
            if "manifesto" in cmd:
                return f"""# Marka Manifestosu: {prod}

Durum: 🟢 Onaylandı

---

### BİZ KİMİZ?
Biz, verimsizliğin ve karmaşık arayüzlerin zamanımızı çaldığı eski iş dünyasına inanmıyoruz. Biz, ekipleri birbirine bağlayan, işleri akışına bırakan ve üretkenliği özgürleştiren bir gelecek tasarlıyoruz.

İşte bu yüzden **{prod}** var. Biz sadece bir araç değil, yeni nesil çalışma felsefesiyiz. Geleceği bugünden inşa edin.

---

## Metrikler
- **Ton:** İlham Verici, Güçlü, Net, Vizyoner"""
            else:
                return f"""# Marka Konumlama Raporu: {prod}

Sektör: **{ind.title()}**  
Durum: 🟢 Strateji Onaylandı

## 4-Boyutlu Konumlama Çerçevesi
1. **Hedef Kitle:** Mevcut hantal süreçlerden sıkılmış {ind.title()} ekipleri.
2. **Referans Çerçevesi:** Yeni nesil bulut tabanlı çalışma alanı platformu.
3. **Farklılaşma Noktası:** Yapay zeka destekli süreç otomasyonu ve ultra-hızlı arayüz.
4. **İnanma Nedeni:** 5,000+ aktif ekip referansı.

## Konumlama Statement (Özet)
"Mevcut hantal araçlarla zaman kaybeden {ind.title()} ekipleri için, {prod}; yapay zeka destekli otomasyonu sayesinde tüm süreçleri tek ekranda toplayan yeni nesil çalışma alanıdır."

## Aksiyon Listesi
- [ ] PR ve Lansman mesaj setlerinin uyumlanması | Sahip: PR & Strateji | Term: 12.06.2026"""

        elif agent_slug == 'yaratici-direktor':
            if "brief-dagit" in cmd:
                return f"""# Yaratıcı Brief Dağıtım Paketi: {prod}

Hazırlayan: **Yaratıcı Direktör**  
Durum: 🟢 Briefler Ekiplere İletildi

## Departman Bazlı Brief Özetleri
- **Copywriter Brief:** 10 tagline ve landing page başlıkları (Odak: Hız, sadelik).
- **Art Director Brief:** Figma arayüz prototipi ve marka renk şemaları.
- **Yapımcı Brief:** 30 saniyelik sosyal medya reklam videosu scripti.

## Aksiyon Listesi
- [ ] Round 1 taslak çıktılarının toplanıp QC seansı | Sahip: Yaratıcı Direktör | Term: 11.06.2026"""
            else:
                return f"""# Yaratıcı Konsept Alternatifleri: {prod} Kampanyası

Durum: 🟢 Round 1 Değerlendirme

## Konsept A: "Karmaşayı Yok Et"
- **Slogan:** "Karmaşaya son, netliğe merhaba."

## Konsept B: "Hızın Yeni Boyutu"
- **Slogan:** "Fikirleriniz kadar hızlı iş akışı."

## Aksiyon Listesi
- [ ] Kreatif ekibin haftalık sync toplantısı | Sahip: Yaratıcı Direktör | Term: Her Çarşamba"""

        elif agent_slug == 'growth-hacker':
            return f"""# Growth Hacker Hacking & A/B Test Planı: {prod}

Durum: 🟢 Deneyler Başlatıldı

## ICE Önceliklendirme Matrisi

| Hipotez / Deney Adı | Etki (Impact) | Güven (Confidence) | Kolaylık (Ease) | ICE Skoru | Statü |
|---------------------|---------------|-------------------|----------------|-----------|-------|
| **Kayıt formunda telefon alanını kaldırmak** | 8 | 9 | 9 | **648** | 🟢 Çalışıyor |
| **Landing page kahraman görselini video yapmak** | 7 | 6 | 8 | **336** | 🚧 Hazırlıkta |
| **Fiyat tablosunda yıllık ödemeyi default seçmek** | 9 | 8 | 9 | **648** | 🟢 Çalışıyor |

## Aksiyon Listesi
- [ ] Yeni form varyasyonunun canlıya alınması | Sahip: Dev & Growth | Term: 10.06.2026"""

        elif agent_slug == 'sosyal-medya':
            return f"""# Sosyal Medya İçerik Planı & Takvimi: {prod}

Durum: 🟢 İçerikler Yayına Hazır

## Haftalık Yayın Takvimi
- **Pazartesi (LinkedIn):** Sektör analizi: "Ekiplerin en çok zaman kaybettiği 3 alan" (🟢 Onaylandı)
- **Çarşamba (X):** Thread: "{prod} ile 10 dakikada nasıl sprint planı kurulur?" (🟢 Onaylandı)
- **Cuma (Instagram):** Reel: Ofiste dağınıklık vs {prod} düzeni (🚧 Kurguda)

## Aksiyon Listesi
- [ ] Cuma günü Reels videosunun kurgu onayı | Sahip: Sosyal Medya | Term: 11.06.2026"""

        elif agent_slug == 'icerik-stratejisti':
            return f"""# İçerik Atomizasyon & SEO Strateji Planı: {prod}

Cornerstone İçerik: **"Modern Ekiplerde Verimli Süreç Yönetimi Rehberi"**  
Durum: 🟢 Yazım Aşamasında

## İçerik Dağıtım Yapısı (Atomizasyon)
1. **Uzun Makale (Blog):** 2000 kelimelik SEO makalesi.
2. **LinkedIn Postları:** Makaleden türetilen 3 ayrı LinkedIn gönderisi.
3. **E-bülten:** Kayıtlı kullanıcılara makale özeti gönderimi.

## Aksiyon Listesi
- [ ] Cornerstone taslağının editör incelemesi | Sahip: İçerik Stratejisti | Term: 12.06.2026"""

        elif agent_slug == 'influencer':
            return f"""# Influencer Vetting & Bütçe Dağılım Raporu: {prod}

Kampanya Hedefi: **B2B SaaS / Teknoloji Profesyonelleri**  
Durum: 🟡 Görüşmeler Devam Ediyor

## Influencer Aday Havuzu Değerlendirmesi
- **Ahmet T. (Tech Creator):** 85K Takipçi / %4.2 Etkileşim (🟢 Teklif Kabul Edildi)
- **Selin K. (Product Manager):** 42K Takipçi / %5.8 Etkileşim (🟢 Teklif Kabul Edildi)

## Aksiyon Listesi
- [ ] Video brieflerinin influencerlara iletilmesi | Sahip: Influencer Yön. | Term: 12.06.2026"""

        elif agent_slug == 'medya-planlama':
            impressions = random.randint(80, 250) * 1000
            clicks = int(impressions * random.uniform(0.015, 0.038))
            conversions = int(clicks * random.uniform(0.05, 0.12))
            spend = random.randint(15, 45) * 1000
            cpc = round(spend / clicks, 2)
            cpa = round(spend / conversions, 2)
            roas = round(random.uniform(2.8, 5.2), 1)
            return f"""# Medya Planlama Bütçe & Kanal Dağılımı: {prod}

Toplam Bütçe: **₺150,000**  
Durum: 🟢 Dağılım Onaylandı

## Kanal Dağılımı ve Beklenen Metrikler
- **Digital Paid (LinkedIn & Google):** %60 (₺90,000) / Gösterim: 1.2M / CPA: ₺180
- **Developer Newsletters:** %20 (₺30,000) / Gösterim: 300K / CPA: ₺220

## Aksiyon Listesi
- [ ] LinkedIn reklam hesabı faturalandırma onayı | Sahip: Medya Planlama | Term: 10.06.2026"""

        elif agent_slug == 'hesap-yoneticisi':
            if "status" in cmd:
                return f"""# Haftalık Müşteri Status Raporu: {prod}

Hazırlayan: **Hesap Yöneticisi**  
Durum: 🟢 Müşteri Sağlık Skoru: 9.2/10 (Yeşil)

## Kampanya Durumu ve Gelişmeler
- **✅ Tamamlananlar:** Marka konumlandırma, brief dağıtımı ve bütçe planları onaylandı.
- **🚧 Devam Edenler:** Landing page UI/UX tasarımları ve reklam metinleri yazılıyor.

## Aksiyon Listesi
- [ ] Müşteri revize toplantısının koordine edilmesi | Sahip: Hesap Yöneticisi | Term: 12.06.2026"""
            else:
                return f"""# Müşteri Brief Kayıt Belgesi: {prod}

Görüşen: **Hesap Yöneticisi**  

## Brief Zorunlu 5 Soru ve Müşteri Yanıtları
1. **Niye şimdi?** -> Rakiplerin karmaşık çözümlerine karşı hızlı ve sade bir alternatif sunmak istiyoruz.
2. **Hedef — sayısal ne?** -> İlk 3 ayda 1,000 aktif aboneye ulaşmak.

## Aksiyon Listesi
- [ ] Kick-off detaylarının iç ekibe aktarılması | Sahip: Hesap Yöneticisi | Term: 08.06.2026"""

        elif agent_slug == 'kriz-iletisimi':
            return f"""# Kriz İletişimi Acil Durum Eylem Planı: {prod}

Senaryo: **Altyapı Kesintisi (Downtime) & Veri Sızıntısı İddiası**  
Durum: 🔴 Alarm Durumu (Simüle Edilmiştir)

## 1. Hazırlanan Resmi Holding Statement (Basın Açıklaması)
"Bugün saat 14:00 itibarıyla {prod} altyapımızda kısa süreli bir erişim kesintisi yaşanmıştır. Mühendislik ekibimiz duruma anında müdahale ederek sistemlerimizi tekrar stabil hale getirmiştir. Herhangi bir veri kaybı veya sızıntısı söz konusu değildir."

## Aksiyon Listesi
- [ ] Teknik post-mortem raporunun PR ekibiyle sync edilmesi | Sahip: Kriz Yön. & CTO | Term: 10.06.2026"""

        elif agent_slug == 'ceo-urun':
            return f"""# CEO & Ürün Yol Haritası (Roadmap): {prod}

Durum: 🟢 Stratejik Hedefler Belirlendi

## RICE Skorlama Tablosu (Özellik Önceliklendirme)

| Özellik Adı | Reach (Erişim) | Impact (Etki) | Confidence (Güven) | Effort (Efor) | RICE Skoru |
|-------------|----------------|---------------|-------------------|--------------|------------|
| **Yapay Zeka Destekli Raporlama** | 800 | 3.0 | %80 | 3 ay (Effort: 3) | **640** |
| **Karanlık Mod UI Arayüzü** | 1000 | 1.5 | %90 | 1 ay (Effort: 1) | **1350** |

## Aksiyon Listesi
- [ ] Sprint 1 planlama toplantısı | Sahip: CEO & CTO | Term: 08.06.2026"""

        elif agent_slug == 'kurmay-baskani':
            return f"""# Kurmay Başkanı OKR Sync ve Çelişki Çözüm Raporu: {prod}

Durum: 🟢 OKR'lar ve Hizalanma Tamamlandı

## Sync Bulguları ve Ekipler Arası Uyum
- **CTO vs CFO Çelişkisi:** CTO'nun istediği yedekleme bütçesi ile CFO'nun maliyet azaltma hedefleri karşılaştırıldı. Çözüm: AWS tasarruf planı satın alınarak bütçe %20 düşürüldü.

## Aksiyon Listesi
- [ ] OKR takip tablosunun güncellenmesi | Sahip: Kurmay Başkanı | Term: Her OKR sync döneminde"""

        elif agent_slug == 'istihbarat':
            return f"""# İstihbarat Rakip Analizi & Pazar Haritalama: {prod}

Sektör: **{ind.title()}**  

## SWOT Analiz Matrisi
- **Güçlü Yönler:** Yapay zeka destekli süreç otomasyonu, ultra-hızlı arayüz.
- **Zayıf Yönler:** Pazara yeni giriş yapılması ve düşük marka bilinirliği.

## Aksiyon Listesi
- [ ] Rakip fiyat paketlerinin takibi | Sahip: İstihbarat | Term: Sürekli"""

        elif agent_slug == 'mudur':
            return f"""# Ajans Haftalık Rapor & Müdür Genel Özeti: {prod}

Dönem: **Haftalık Değerlendirme**  
Durum: 🟢 Tüm Sistemler Nominal Operasyonda

## Genel Performans ve Kritik Notlar
- **Proje Takvimi:** Geciken herhangi bir deliverable bulunmamaktadır.
- **Mali Sağlık:** Nakit akışı hedeflerle uyumludur.

## Aksiyon Listesi
- [ ] Pazartesi sabahı genel ajans sync toplantısı | Sahip: Müdür | Term: Her Pazartesi 09:30"""

        else:
            dept_title = name + " Raporu"
            clean_cmd = command if command else "/test"
            clean_task = task if task else "Departman Görev Dağılımı"
            return f"""# {dept_title}: {prod}
            
Aktif Komut: `{clean_cmd}`  
Rol: {name} — Departman Görev Dağılımı ve İş Çıktısı

## 1. Çalıştırılan Görev
**"{clean_task}"** görevi referans dokümantasyona ve ADA standartlarına göre başarıyla yürütülmüştür.

## 2. Bulgular ve Analiz
- **Metrik Sağlığı:** 🟢 Tüm ilgili departman KPI'ları hedeflerle uyumludur.

## 3. Aksiyon Planı ve Teslimat
- [ ] Çıktıların son değerlendirme ve onay süreci | Sahip: {name} | Term: {random.randint(10, 20)}.06.2026"""
