from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "css" / "main.css"


def test_layout_has_tablet_and_mobile_reflow_rules():
    css = CSS_PATH.read_text(encoding="utf-8")

    assert "@media (max-width: 820px)" in css
    assert "@media (max-width: 520px)" in css
    assert ".vocabulary-grid { grid-template-columns: 1fr; }" in css
    assert ".scene { position: static;" in css
    assert ".sentence-row { max-width: 100%;" in css


if __name__ == "__main__":
    test_layout_has_tablet_and_mobile_reflow_rules()
    print("Responsive CSS test passed.")
