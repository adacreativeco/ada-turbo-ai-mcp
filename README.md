# ADA Turbo — Agency OS & Pixel Office

<div align="center">

[![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-6366f1?style=for-the-badge&logo=anthropic&logoColor=white)](https://modelcontextprotocol.io/)
[![PyPI](https://img.shields.io/pypi/v/ada-turbo-ai-mcp?style=for-the-badge&color=3775A9&logo=pypi&logoColor=white)](https://pypi.org/project/ada-turbo-ai-mcp/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-PolyForm_NC-10b981?style=for-the-badge)](LICENSE)
[![Smithery](https://img.shields.io/badge/Smithery-Ready-f59e0b?style=for-the-badge)](https://smithery.ai)
[![GitHub Stars](https://img.shields.io/github/stars/adacreativeco/ada-turbo-ai-mcp?style=for-the-badge&color=ffd700)](https://github.com/adacreativeco/ada-turbo-ai-mcp/stargazers)
[![Case Study](https://img.shields.io/badge/Case_Study-ADA_Creative_Co.-0ea5e9?style=for-the-badge&logo=safari&logoColor=white)](https://adacreative.co/vaka-analizleri/ada-turbo-mcp)

<br/>

**🇺🇸 English Documentation | 🇹🇷 [Türkçe Dokümantasyon](README.tr.md)**

<p align="center">
  <strong>Transform your IDE into a full-scale creative agency.</strong><br/>
  ADA Turbo delivers the <strong>ADA Creative Co.</strong> agency operating system with 26 specialized AI roles via <strong>MCP (Model Context Protocol)</strong>, paired with a real-time retro CRT <strong>Pixel Office Visualizer</strong>.
</p>

</div>

---

## 🎬 Live Office & Animation Preview

<div align="center">
  <img src="animasyonlar/ada-turbo-walk-preview.gif" alt="Pixel Office Characters Walking Animation" width="100%" />
</div>

<br/>

| 🏢 Pixel Office Visualizer | 🧪 CRT Workflow Playground |
| :---: | :---: |
| ![Pixel Office Dashboard](dashboard_screenshot_en.png) | ![CRT Workflow Playground](playground_screenshot_en.png) |

---

## ⚡ Quick Start (Run in 10 Seconds)

### Option A: Zero-Install with `uvx` (Recommended)
You can run ADA Turbo instantly without cloning or managing virtual environments:

```bash
uvx ada-turbo-ai-mcp
```
*(Or launch just the web visualizer: `uvx ada-turbo-ai-mcp --web`)*

---

### Option B: Standard Git / Python
```bash
# 1. Clone the repository
git clone https://github.com/adacreativeco/ada-turbo-ai-mcp.git
cd ada-turbo-ai-mcp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Unified Dual-Mode (MCP stdio + Web Visualizer)
python server.py
```
Open [http://localhost:8000](http://localhost:8000) (auto-fallback to `8001`, `8002`... if occupied) in your browser.

---

## 🚀 Key Features

- **Unified Dual-Mode Architecture:**
  - **MCP Mode (Default):** Runs as an MCP stdio server. Concurrently starts the Pixel Office Web Server in the background. Seamlessly connects to Antigravity, Claude Desktop, Cursor, Claude Code, and Windsurf.
  - **Pixel Office Web Mode:** Starts a local, highly-optimized retro CRT-effect web workspace (`python server.py --web`).
- **⚡ Real-Time Server-Sent Events (SSE):**
  - Zero-latency event streaming (`/api/events`). When an agent is triggered in your IDE, the corresponding character visually walks to their desk in real-time!
- **🧠 Direct Live LLM Engine:**
  - Multi-provider AI execution directly in the browser via `/api/llm-generate`:
    - 🟢 **Built-in Template Engine (Offline):** Instant access to professional agency workflow templates without API keys.
    - ✨ **Google Gemini:** `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`
    - 🧠 **OpenAI:** `gpt-4o-mini`, `gpt-4o`, `o3-mini`
    - ⚡ **Anthropic Claude:** `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`
  - Safe local credential storage in browser `localStorage`.
- **Developer Tools (CRT Console Modals):**
  - **Playground (Workflow & Live AI Tester):** Select commands and test tasks with offline templates or live LLM models with typewriter output.
  - **AI Model Configurator:** Switch providers, enter API keys safely, and select model presets.
  - **Setup Wizard:** Dynamically outputs ready-to-copy configuration blocks for Cursor, Antigravity, Claude Desktop, and Claude Code.
- **Pixel Characters & Animations:** 26 unique agency characters with idle (breathing, blinking) and walking cycles across custom office floors.
- **Full Bilingual Support (TR / EN):** One-click toggle for all UI elements, status badges, modals, agent prompts, and knowledge references.

---

## 🔌 IDE Integration (MCP)

### 1. Antigravity
Add to your `mcp_config.json`:
```json
{
  "mcpServers": {
    "ada-turbo": {
      "command": "uvx",
      "args": ["ada-turbo-ai-mcp"]
    }
  }
}
```

### 2. Cursor
Add to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project-level):
```json
{
  "mcpServers": {
    "ada-turbo": {
      "command": "uvx",
      "args": ["ada-turbo-ai-mcp"]
    }
  }
}
```

### 3. Claude Desktop
Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "ada-turbo": {
      "command": "uvx",
      "args": ["ada-turbo-ai-mcp"]
    }
  }
}
```

### 4. Claude Code (CLI)
```bash
claude mcp add ada-turbo -- uvx ada-turbo-ai-mcp
```

*(Note: If using local clone, replace `"command": "uvx"` and `"args": ["ada-turbo-ai-mcp"]` with `"command": "python"` and `"args": ["/ABSOLUTE/PATH/server.py"]`)*

---

## 👥 26 Agency Roles & Specializations

ADA Turbo organizes 26 specialized agents across 5 key departments:

1. **Strategy & Brand:** Brand Director, Brand Strategist, Consumer Insight Lead, Naming Specialist, Creative Technologist.
2. **Creative & Design:** Creative Director, Senior Copywriter, Art Director, UX/UI Lead, 3D/Motion Designer.
3. **Marketing & Growth:** Growth Marketing Director, Performance Marketing Specialist, SEO/Content Strategist, Social Media Lead, CRM & Retention Manager.
4. **Client & Operations:** Account Director, Senior Account Manager, Agency Producer, Operations Director, Traffic Manager.
5. **Analytics & Tech:** Chief Data Officer, Marketing Data Analyst, Full-Stack Lead, AI Solutions Architect, QA & Delivery Lead.

---

## 📂 Architecture

```
ada-turbo-mcp/
├── server.py                   ← Unified dual-mode entry point (MCP + Web)
├── index.html                  ← Retro CRT Pixel Office single-page UI
├── pyproject.toml              ← Package metadata & entry points
├── smithery.yaml               ← Smithery.ai 1-click install configuration
├── requirements.txt            ← Project dependencies
├── references/                 ← Bilingual domain knowledge bases (.md)
│   ├── strategy-brand.md / strateji-marka.md
│   ├── creative-team.md / yaratici-ekip.md
│   ├── marketing-growth.md / pazarlama-buyume.md
│   ├── client-operations.md / musteri-operasyon.md
│   └── analytics-product-tech.md / analitik-urun-teknik.md
├── karakterler/                ← Pixel character graphics and generator scripts
├── animasyonlar/               ← Character walk/idle spritesheets & GIF previews
├── office-bina/ & office-zon/  ← Procedural pixel art building generation assets
├── skill/                      ← Pre-packaged .skill distribution bundle
└── src/                        ← Python modules
    ├── mcp_server.py           ← FastMCP server definitions & tool registrations
    ├── web_server.py           ← Multi-threaded HTTP server, SSE broadcaster & LLM proxy
    └── workflow_manager.py     ← Command routing, action listener dispatch & templates
```

---

## 📄 License

Distributed under the PolyForm Noncommercial License 1.0.0. See [LICENSE](LICENSE) for details.

Developed with ❤️ by **[ADA Creative Co.](https://github.com/adacreativeco)**
