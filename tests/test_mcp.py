import unittest
import threading
import urllib.request
import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
sys.path.insert(0, str(Path(__file__).parent.parent.resolve() / "src"))

from workflow_manager import (
    WorkflowManager,
    COMMAND_MAP,
    REFERENCE_TITLES,
    register_action_listener,
    unregister_action_listener,
    log_agent_action
)
from web_server import find_free_port, RobustThreadingTCPServer, OfficeHTTPRequestHandler

class TestWorkflowManager(unittest.TestCase):
    def setUp(self):
        # Test için varsayılan workflow manager'ı kur
        self.manager = WorkflowManager()

    def test_resolve_command(self):
        # Geçerli komutların çözülmesi
        self.assertEqual(self.manager.resolve_command("/copy"), "yaratici-ekip")
        self.assertEqual(self.manager.resolve_command("/cfo"), "analitik-urun-teknik")
        self.assertEqual(self.manager.resolve_command("/strateji"), "strateji-marka")
        
        # Harf büyüklüğü duyarlılığı ve boşluk temizleme
        self.assertEqual(self.manager.resolve_command("  /COPY tagline  "), "yaratici-ekip")
        self.assertEqual(self.manager.resolve_command("cfo"), "analitik-urun-teknik") # Slaşsız
        
        # Geçersiz komut
        self.assertIsNone(self.manager.resolve_command("/gecersiz-komut"))

    def test_load_reference_success(self):
        # Var olan referansı yükleme
        content = self.manager.load_reference("strateji-marka")
        self.assertTrue(len(content) > 0)
        self.assertNotIn("[HATA]", content)
        self.assertIn("Strateji & Marka", content)

    def test_load_reference_failure(self):
        # Var olmayan referans
        content = self.manager.load_reference("olmayan-dosya")
        self.assertTrue(content.startswith("[HATA]"))

    def test_get_workflow_success(self):
        # Geçerli workflow üretme
        workflow = self.manager.get_workflow("/copy tagline", "Lansman kampanyası")
        self.assertIn("Lansman kampanyası", workflow)
        self.assertIn("Yaratıcı Ekip", workflow)
        self.assertIn("TEMEL DAVRANIŞ KURALLARI", workflow)

    def test_get_workflow_english(self):
        # English workflow generation
        workflow = self.manager.get_workflow("/copy tagline", "Launch campaign", lang="en")
        self.assertIn("Launch campaign", workflow)
        self.assertIn("Creative Team", workflow)
        self.assertIn("CORE BEHAVIOR RULES", workflow)

    def test_generate_output_english(self):
        # English output generation translation
        output = self.manager.generate_agent_output("cfo", "CFO", "/cfo mrr", "Launch", lang="en")
        self.assertIn("CFO MRR Movement & Revenue Analysis", output)
        self.assertIn("Monthly MRR Flow Table", output)

    def test_get_workflow_invalid(self):
        # Geçersiz komut durumunda hata mesajı döndürmesi
        workflow = self.manager.get_workflow("/gecersiz-komut", "Lansman")
        self.assertIn("bilinen bir ADA komutuna eşlenemedi", workflow)

    def test_get_commands_list(self):
        # Komut listesinin dönen yapısının kontrolü
        commands = self.manager.get_commands_list()
        self.assertIsInstance(commands, list)
        self.assertTrue(len(commands) > 0)
        
        # İlk elemanın anahtar yapısı
        first_item = commands[0]
        self.assertIn("slug", first_item)
        self.assertIn("title", first_item)
        self.assertIn("commands", first_item)

    def test_action_listener_and_sse_dispatch(self):
        # SSE / Action Listener Event Tetikleme Testi
        received_events = []
        def listener(evt):
            received_events.append(evt)

        register_action_listener(listener)
        try:
            log_agent_action("Test Ajanı", "/test_komut", "Test Görevi")
            self.assertTrue(len(received_events) > 0)
            last_event = received_events[-1]
            self.assertEqual(last_event.get("agent"), "Test Ajanı")
            self.assertEqual(last_event.get("command"), "/test_komut")
            self.assertEqual(last_event.get("type"), "agent_action")
        finally:
            unregister_action_listener(listener)

    def test_find_free_port(self):
        # Dinamik port bulucu testi
        port = find_free_port(8000, max_tries=20)
        self.assertIsInstance(port, int)
        self.assertGreaterEqual(port, 8000)

    def test_live_web_server_endpoints(self):
        # Canlı web sunucusu endpoint testleri
        test_port = find_free_port(8950, max_tries=50)
        httpd = RobustThreadingTCPServer(('', test_port), OfficeHTTPRequestHandler)
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()
        time.sleep(0.1)

        try:
            # 1. /api/status GET
            with urllib.request.urlopen(f"http://localhost:{test_port}/api/status", timeout=5) as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode('utf-8'))
                self.assertIn("history", data)

            # 2. /api/commands GET
            with urllib.request.urlopen(f"http://localhost:{test_port}/api/commands", timeout=5) as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode('utf-8'))
                self.assertIsInstance(data, list)

            # 3. /api/llm-generate (Builtin Mode) POST
            req_data = json.dumps({
                "provider": "builtin",
                "komut": "/copy tagline",
                "gorev": "Test SaaS fintech lansmanı",
                "lang": "tr"
            }).encode('utf-8')
            req = urllib.request.Request(
                f"http://localhost:{test_port}/api/llm-generate",
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as res:
                self.assertEqual(res.status, 200)
                data = json.loads(res.read().decode('utf-8'))
                self.assertIn("output", data)
                self.assertEqual(data.get("provider"), "builtin")

        finally:
            try:
                httpd.shutdown()
            except:
                pass
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
