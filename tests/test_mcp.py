import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
sys.path.insert(0, str(Path(__file__).parent.parent.resolve() / "src"))

from workflow_manager import WorkflowManager, COMMAND_MAP, REFERENCE_TITLES

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


if __name__ == "__main__":
    unittest.main()
