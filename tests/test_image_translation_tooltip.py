from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JS_PATH = ROOT / "assets" / "js" / "vocabulary.js"
CSS_PATH = ROOT / "assets" / "css" / "main.css"


def test_image_reference_exposes_the_spanish_translation_on_hover_and_focus():
    javascript = JS_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8")

    assert 'className: "image-reference"' in javascript
    assert 'className: "translation-tooltip"' in javascript
    assert 'text: entry.translation' in javascript
    assert 'tabindex: "0"' in javascript
    assert ".image-reference:hover .translation-tooltip" in css
    assert ".image-reference:focus .translation-tooltip" in css
    assert "bottom: calc(100% + 10px);" in css


if __name__ == "__main__":
    test_image_reference_exposes_the_spanish_translation_on_hover_and_focus()
    print("Image translation tooltip test passed.")
