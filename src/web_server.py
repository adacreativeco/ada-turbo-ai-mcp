import http.server
import socketserver
import socket
import json
import os
import sys
import time
import queue
import threading
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import urlparse, parse_qs
try:
    from .workflow_manager import (
        WorkflowManager,
        BEHAVIOR_RULES,
        BEHAVIOR_RULES_EN,
        log_agent_action,
        register_action_listener
    )
except ImportError:
    from workflow_manager import (
        WorkflowManager,
        BEHAVIOR_RULES,
        BEHAVIOR_RULES_EN,
        log_agent_action,
        register_action_listener
    )

# Windows Unicode Console Encoding Fix (Avoids CP1254 / Unicode crashes)
if sys.platform.startswith("win"):
    import io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "buffer"):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ==============================================================================
# SERVER-SENT EVENTS (SSE) EVENT BUS
# ==============================================================================
SSE_CLIENTS = []
SSE_LOCK = threading.Lock()

def broadcast_sse(event_data: dict):
    """Broadcasts event data to all connected SSE browser clients."""
    with SSE_LOCK:
        dead_clients = []
        for q in list(SSE_CLIENTS):
            try:
                q.put_nowait(event_data)
            except Exception:
                dead_clients.append(q)
        for q in dead_clients:
            if q in SSE_CLIENTS:
                SSE_CLIENTS.remove(q)

# Register SSE broadcaster with workflow manager
register_action_listener(broadcast_sse)


# ==============================================================================
# PORT UTILS
# ==============================================================================
def is_port_in_use(port: int) -> bool:
    """Checks if an active server is listening on 127.0.0.1:port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            return s.connect_ex(('127.0.0.1', port)) == 0
    except Exception:
        return False

def find_free_port(start_port: int = 8000, max_tries: int = 50) -> int:
    """Tries consecutive ports starting from `start_port` to find an available one."""
    for port in range(start_port, start_port + max_tries):
        if not is_port_in_use(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
    return start_port


# ==============================================================================
# HTTP & SSE REQUEST HANDLER
# ==============================================================================
class OfficeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Statik dosyaları sunmak için projenin kök dizinini belirle (src'nin bir üst dizini)
        self.root_dir = str(Path(__file__).parent.parent.resolve())
        super().__init__(*args, directory=self.root_dir, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-api-key')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/api/events':
            self._handle_sse()
        elif path == '/api/status':
            self._handle_status()
        elif path == '/api/output':
            self._handle_output(parsed_path.query)
        elif path == "/api/commands":
            self._send_json(WorkflowManager().get_commands_list())
        elif path == "/api/rules":
            lang = parse_qs(parsed_path.query).get('lang', ['tr'])[0].lower()
            self._send_json({"rules": BEHAVIOR_RULES_EN if lang == 'en' else BEHAVIOR_RULES})
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
        elif path == "/api/llm-generate":
            self._handle_llm_generate()
        else:
            self.send_response(404)
            self.end_headers()

    def _send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _handle_sse(self):
        """Server-Sent Events stream for real-time agent dispatch & animations."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-transform')
        self.send_header('Connection', 'keep-alive')
        self.end_headers()

        client_queue = queue.Queue(maxsize=100)
        with SSE_LOCK:
            SSE_CLIENTS.append(client_queue)

        try:
            # Initial handshake
            init_msg = json.dumps({"type": "connected", "timestamp": time.time()})
            self.wfile.write(f"data: {init_msg}\n\n".encode('utf-8'))
            self.wfile.flush()

            while True:
                try:
                    event_data = client_queue.get(timeout=15.0)
                    msg = json.dumps(event_data, ensure_ascii=False)
                    self.wfile.write(f"data: {msg}\n\n".encode('utf-8'))
                    self.wfile.flush()
                except queue.Empty:
                    # Keep-alive ping comment
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, Exception):
            pass
        finally:
            with SSE_LOCK:
                if client_queue in SSE_CLIENTS:
                    SSE_CLIENTS.remove(client_queue)

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

    def _handle_llm_generate(self):
        """Direct Live LLM generation endpoint supporting Gemini, OpenAI, Anthropic & Local Engine."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data.decode("utf-8"))
            provider = data.get("provider", "builtin").lower()
            api_key = data.get("apiKey", "").strip()
            model = data.get("model", "").strip()
            komut = data.get("komut", "")
            gorev = data.get("gorev", "")
            system_prompt = data.get("systemPrompt", "")
            user_prompt = data.get("userPrompt", "")
            lang = data.get("lang", "tr").lower()

            # If system prompt is not supplied, fetch workflow reference
            if not system_prompt and komut:
                system_prompt = WorkflowManager().get_workflow(komut, gorev, log_action=True, lang=lang)

            if not user_prompt:
                user_prompt = f"Görev: {gorev}" if lang == "tr" else f"Task: {gorev}"

            if provider == "builtin" or not api_key:
                # Builtin high-quality local generator
                agent_name = data.get("agent", "")
                agent_slug = data.get("agentSlug", "")
                out = WorkflowManager().generate_agent_output(agent_slug, agent_name, komut, gorev, lang=lang)
                self._send_json({"output": out, "provider": "builtin", "model": "local-template-engine"})
                return

            if provider == "gemini":
                model_name = model or "gemini-2.0-flash"
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                payload = {
                    "system_instruction": {
                        "parts": [{"text": system_prompt}]
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": user_prompt}]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 4096
                    }
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    candidates = res_data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        text_out = "".join([p.get("text", "") for p in parts])
                        self._send_json({"output": text_out, "provider": "gemini", "model": model_name})
                        return
                    else:
                        raise ValueError(f"Gemini yanıt veremedi: {res_data}")

            elif provider == "openai":
                model_name = model or "gpt-4o-mini"
                url = "https://api.openai.com/v1/chat/completions"
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.7
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    }
                )
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    choices = res_data.get("choices", [])
                    if choices and "message" in choices[0]:
                        text_out = choices[0]["message"].get("content", "")
                        self._send_json({"output": text_out, "provider": "openai", "model": model_name})
                        return
                    else:
                        raise ValueError(f"OpenAI yanıt veremedi: {res_data}")

            elif provider == "anthropic":
                model_name = model or "claude-3-5-sonnet-20241022"
                url = "https://api.anthropic.com/v1/messages"
                payload = {
                    "model": model_name,
                    "max_tokens": 4096,
                    "system": system_prompt,
                    "messages": [
                        {"role": "user", "content": user_prompt}
                    ]
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01"
                    }
                )
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    content = res_data.get("content", [])
                    text_out = "".join([c.get("text", "") for c in content if c.get("type") == "text"])
                    self._send_json({"output": text_out, "provider": "anthropic", "model": model_name})
                    return
            else:
                self._send_json({"error": f"Bilinmeyen model sağlayıcısı: {provider}"}, status_code=400)

        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='ignore')
            self._send_json({"error": f"API Hatası ({e.code}): {err_body}"}, status_code=500)
        except Exception as e:
            self._send_json({"error": f"Model Çalıştırma Hatası: {str(e)}"}, status_code=500)

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
    allow_reuse_address = False if sys.platform.startswith("win") else True
    
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


def run_server(port=8000, auto_port=True):
    """Starts the Pixel Office Visualizer on an available port."""
    target_port = find_free_port(port) if auto_port else port
    
    if target_port != port:
        print(f"\n⚠️  [BİLGİ] İstenen port ({port}) meşgul olduğu için otomatik olarak port {target_port} seçildi.", file=sys.stderr, flush=True)
    
    server_address = ('', target_port)
    httpd = RobustThreadingTCPServer(server_address, OfficeHTTPRequestHandler)
    print(f"\n=======================================================", file=sys.stderr, flush=True)
    print(f"🚀 ADA Turbo Pixel Office Visualizer Hazır!", file=sys.stderr, flush=True)
    print(f"📡 Canlı Web Arayüzü : http://localhost:{target_port}", file=sys.stderr, flush=True)
    print(f"⚡ Server-Sent Events : http://localhost:{target_port}/api/events", file=sys.stderr, flush=True)
    print(f"🛑 Durdurmak için     : Ctrl+C", file=sys.stderr, flush=True)
    print(f"=======================================================\n", file=sys.stderr, flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...", file=sys.stderr, flush=True)
        httpd.server_close()


if __name__ == "__main__":
    run_server()
