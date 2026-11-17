from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "css" / "main.css"
INDEX_PATH = ROOT / "index.html"


def test_desktop_uses_three_cards_and_a_wider_reading_area():
    css = CSS_PATH.read_text(encoding="utf-8")

    assert "width: min(1440px, 100%);" in css
    assert "@media (min-width: 1180px)" in css
    assert ".vocabulary-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }" in css


def test_page_has_jc_french_learning_signature():
    html = INDEX_PATH.read_text(encoding="utf-8")
    assert "J’apprends le français avec Juan Carlos." in html


if __name__ == "__main__":
    test_desktop_uses_three_cards_and_a_wider_reading_area()
    test_page_has_jc_french_learning_signature()
    print("Desktop layout test passed.")
