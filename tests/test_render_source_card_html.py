import tempfile
import unittest
from pathlib import Path

from scripts.render_source_card_html import main, render_card_html
try:
    from test_validate_source_card import valid_card
except ModuleNotFoundError:
    from tests.test_validate_source_card import valid_card


class RenderSourceCardHtmlTests(unittest.TestCase):
    def test_render_escapes_html(self):
        card = valid_card()
        card["title"] = "<script>alert('x')</script>"
        card["evidence_notes"] = ["Use <b>escaping</b> here."]

        html = render_card_html(card)

        self.assertIn("&lt;script&gt;", html)
        self.assertIn("&lt;b&gt;escaping&lt;/b&gt;", html)
        self.assertNotIn("<script>alert", html)

    def test_render_main_writes_output_file(self):
        card_path = Path("examples/source-card.example.json")
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "card.html"
            result = main(["render_source_card_html.py", str(card_path), str(out_path)])
            self.assertEqual(result, 0)
            rendered = out_path.read_text(encoding="utf-8")
            self.assertIn("Local source card review page", rendered)
            self.assertIn("Synthetic city water notice summary", rendered)


if __name__ == "__main__":
    unittest.main()
