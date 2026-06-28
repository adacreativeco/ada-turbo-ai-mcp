import http.server
import socketserver
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from .workflow_manager import WorkflowManager, BEHAVIOR_RULES, log_agent_action

# Windows Unicode Console Encoding Fix (Avoids CP1254 / Unicode crashes)
if sys.platform.startswith("win"):
    import io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

class OfficeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Statik dosyaları sunmak için projenin kök dizinini belirle (src'nin bir üst dizini)
        self.root_dir = str(Path(__file__).parent.parent.resolve())
        super().__init__(*args, directory=self.root_dir, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/status':
            self._handle_status()
        elif path == '/api/output':
            self._handle_output(parsed_path.query)
        elif path == "/api/commands":
            self._send_json(WorkflowManager().get_commands_list())
        elif path == "/api/rules":
            self._send_json({"rules": BEHAVIOR_RULES})
        elif path == "/api/config":
            self._handle_config()
        elif path.startswith("/api/reference/"):
            slug = path.split("/")[-1]
            content = WorkflowManager().load_reference(slug)
            self._send_json({"slug": slug, "content": content})
        elif path == '/':
            self.path = '/index.html'
            super().do_GET()
        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/trigger':
            self._handle_trigger()
        elif path == "/api/workflow":
            self._handle_workflow()
        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _handle_status(self):
        status_file = Path(self.root_dir) / 'agent_status.json'
        if status_file.exists():
            try:
                content = status_file.read_text(encoding="utf-8")
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
                return
            except Exception as e:
                self._send_json({"error": str(e), "active_agent": None, "history": []})
                return
        self._send_json({"active_agent": None, "history": []})

    def _handle_output(self, query_str):
        query = parse_qs(query_str)
        agent_slug = query.get('agent', [''])[0]
        command = query.get('command', [''])[0]
        task = query.get('task', [''])[0]
        lang = query.get('lang', ['tr'])[0].lower()
        
        # Map slug to name
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
        
        name = "Ajan"
        for cmd_key, agent_name in COMMAND_TO_AGENT.items():
            slug_test = agent_name.lower().replace(" ", "").replace("/", "-").replace("ö", "o").replace("ü", "u").replace("ş", "s").replace("ç", "c").replace("ğ", "g").replace("ı", "i")
            if agent_slug == slug_test:
                name = agent_name
                break
        
        if name == "Ajan" and agent_slug:
            name = agent_slug.replace("-", " ").title()
            
        try:
            markdown_content = WorkflowManager().generate_agent_output(agent_slug, name, command, task, lang=lang)
            self._send_json({"markdown": markdown_content})
        except Exception as e:
            self._send_json({"error": str(e)}, status_code=500)

    def _handle_trigger(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            agent = data.get("agent")
            command = data.get("command", "")
            task = data.get("task", "")
            
            log_agent_action(agent, command, task)
            self._send_json({"success": True})
        except Exception as e:
            self._send_json({"error": str(e)}, status_code=400)

    def _handle_workflow(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode("utf-8"))
            komut = data.get("komut", "")
            gorev = data.get("gorev", "")
            lang = data.get("lang", "tr")
            
            result = WorkflowManager().get_workflow(komut, gorev, log_action=True, lang=lang)
            self._send_json({"workflow": result})
        except Exception as e:
            self._send_json({"error": str(e)}, status_code=400)

    def _handle_config(self):
        server_path = str(Path(self.root_dir) / "server.py")
        server_path_unix = server_path.replace("\\", "/")
        
        configs = {
            "absolute_path": server_path,
            "antigravity": {
                "mcpServers": {
                    "ada-turbo": {
                        "command": "python",
                        "args": [server_path_unix]
                    }
                }
            },
            "claude_desktop": {
                "mcpServers": {
                    "ada-turbo": {
                        "command": "python",
                        "args": [server_path_unix]
                    }
                }
            },
            "cursor": {
                "mcpServers": {
                    "ada-turbo": {
                        "command": "python",
                        "args": [server_path_unix]
                    }
                }
            },
            "windsurf": {
                "mcpServers": {
                    "ada-turbo": {
                        "command": "python",
                        "args": [server_path_unix]
                    }
                }
            },
            "claude_code": f"claude mcp add ada-turbo -- python \"{server_path_unix}\""
        }
        self._send_json(configs)


class RobustThreadingTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    
    def handle_error(self, request, client_address):
        # Ignore socket close/abort tracebacks to prevent stderr issues on Windows background tasks
        import sys
        exc_type, exc_value, _ = sys.exc_info()
        if exc_type in (ConnectionAbortedError, ConnectionResetError, BrokenPipeError) or (exc_value and "10053" in str(exc_value)):
            pass
        else:
            try:
                super().handle_error(request, client_address)
            except:
                pass


def run_server(port=8000):
    server_address = ('', port)
    httpd = RobustThreadingTCPServer(server_address, OfficeHTTPRequestHandler)
    print(f"\n=========================================")
    print(f"ADA Turbo Pixel Office Visualizer Hazır!")
    print(f"Tarayıcıda açın: http://localhost:{port}")
    print(f"Durdurmak için: Ctrl+C")
    print(f"=========================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
