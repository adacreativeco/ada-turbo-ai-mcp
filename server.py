#!/usr/bin/env python3
"""
ADA Turbo Entry Point (GÜNCEL)
==============================
ADA Creative Co. ajans işletim sistemini başlatır.
Varsayılan olarak stdio üzerinden MCP sunucusu olarak çalışır.
--web parametresi verilirse interaktif Pixel Office Visualizer web sunucusunu başlatır.
"""

import sys
import argparse
from pathlib import Path

# Ensure project root and src are available in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

try:
    from web_server import run_server
    from mcp_server import main as run_mcp
except ImportError:
    from src.web_server import run_server
    from src.mcp_server import main as run_mcp


def main():
    parser = argparse.ArgumentParser(description="ADA Turbo Agentic OS Server")
    parser.add_argument(
        "--web", "-w",
        action="store_true",
        help="Start the interactive Pixel Office Visualizer instead of the MCP server"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8000,
        help="Port to run the visualizer web server on (default: 8000)"
    )

    args = parser.parse_args()

    if args.web:
        # Sadece Web görselleştirici sunucusunu başlat (bloklayıcı mod)
        run_server(args.port)
    else:
        # BİRLEŞİK ÇİFT MOD (UNIFIED DUAL-MODE):
        # Arka planda Pixel Office Web sunucusunu başlat, ön planda FastMCP stdio'yu dinle!
        import threading
        web_thread = threading.Thread(target=run_server, kwargs={"port": args.port, "auto_port": True}, daemon=True)
        web_thread.start()

        # MCP sunucusunu başlat (stdio transport)
        run_mcp()


if __name__ == "__main__":
    main()
