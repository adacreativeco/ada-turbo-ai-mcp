import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from .workflow_manager import WorkflowManager, BEHAVIOR_RULES, BEHAVIOR_RULES_EN

# Windows Unicode Console Encoding Fix (Avoids CP1254 / Unicode crashes on Windows)
if sys.platform.startswith("win"):
    import io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

mcp = FastMCP("ada-turbo")
manager = WorkflowManager()

# --------------------------------------------------------------------------
# TOOLS
# --------------------------------------------------------------------------

@mcp.tool()
def ada_workflow(komut: str, gorev: str = "", lang: str = "tr") -> str:
    """ADA ajans workflow'unu çalıştırmak için gereken talimat ve formatı döndürür.

    Bir /komut (ör. '/copy tagline', '/strateji yaratici-brief', '/cfo runway')
    veya serbest görev tanımı ver. Bu araç, o workflow'a ait davranış kurallarını
    ve referans formatını döndürür; sen de bu formata göre çıktıyı üretirsin.

    Args:
        komut: ADA komutu, ör. '/copy tagline' veya '/analitik aylik-rapor'.
        gorev: (Opsiyonel) Müşteri/proje bağlamı veya serbest görev tanımı.
        lang: (Opsiyonel) Çıktı dili ('tr' veya 'en'). Varsayılan 'tr'.
    """
    return manager.get_workflow(komut, gorev, log_action=True, lang=lang.lower())


@mcp.tool()
def ada_komutlar() -> str:
    """Tüm ADA ajans komutlarını ve hangi alana ait olduklarını listeler."""
    from .workflow_manager import log_agent_action
    log_agent_action("Müdür", "/ada_komutlar", "Komut haritası görüntülendi")
    
    lines = ["# ADA TURBO — KOMUT HARİTASI\n"]
    commands_list = manager.get_commands_list()
    
    for area in commands_list:
        lines.append(f"\n## {area['title']}")
        lines.append("Komutlar: " + ", ".join(area['commands']))
        
    lines.append(
        "\n\nKullanım: 'ada_workflow' aracını komut + opsiyonel görev bağlamı ile çağır.\n"
        "Örnek: ada_workflow(komut='/copy tagline', gorev='Nexus SaaS, B2B, fintech')"
    )
    return "\n".join(lines)


@mcp.tool()
def ada_kurallar(lang: str = "tr") -> str:
    """ADA Turbo'nun temel davranış kurallarını döndürür (her görevde geçerli)."""
    from .workflow_manager import log_agent_action
    log_agent_action("Kurmay Başkanı", "/ada_kurallar", "Temel davranış kuralları görüntülendi")
    return BEHAVIOR_RULES_EN if lang.lower() == "en" else BEHAVIOR_RULES


# --------------------------------------------------------------------------
# RESOURCES
# --------------------------------------------------------------------------

@mcp.resource("ada://kurallar")
def kurallar_resource() -> str:
    """ADA Turbo temel davranış kuralları."""
    return BEHAVIOR_RULES


@mcp.resource("ada://referans/{slug}")
def referans_resource(slug: str) -> str:
    """Belirli bir alanın referans bilgi tabanı.

    Geçerli slug'lar: strateji-marka, yaratici-ekip, pazarlama-buyume,
    musteri-operasyon, analitik-urun-teknik
    """
    return manager.load_reference(slug)


# --------------------------------------------------------------------------
# PROMPTS
# --------------------------------------------------------------------------

@mcp.prompt()
def ada(komut: str, gorev: str = "", lang: str = "tr") -> str:
    """ADA workflow'unu hızlıca başlat (slash-komut olarak görünür).

    Args:
        komut: ADA komutu, ör. '/copy tagline'.
        gorev: Opsiyonel müşteri/proje bağlamı.
        lang: Çıktı dili ('tr' veya 'en').
    """
    return manager.get_workflow(komut, gorev, log_action=True, lang=lang.lower())


def main():
    """Entry point — stdio transport ile sunucuyu başlatır."""
    mcp.run()


if __name__ == "__main__":
    main()
