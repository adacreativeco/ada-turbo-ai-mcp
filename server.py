#!/usr/bin/env python3
"""
ADA Turbo Entry Point (GÜNCEL)
==============================
ADA Creative Co. ajans işletim sistemini başlatır.
Varsayılan olarak stdio üzerinden MCP sunucusu olarak çalışır.
--web parametresi verilirse interaktif Pixel Office Visualizer web sunucusunu başlatır.
"""

import argparse

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
        # Web visualizer sunucusunu başlat
        from src.web_server import run_server
        run_server(args.port)
    else:
        # MCP sunucusunu başlat
        from src.mcp_server import main as run_mcp
        run_mcp()

if __name__ == "__main__":
    main()
