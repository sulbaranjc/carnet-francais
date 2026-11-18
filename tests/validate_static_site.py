from html.parser import HTMLParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DATA_PATH = ROOT / "assets" / "data" / "vocabulary.json"


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.inline_style = False
        self.inline_script = False
        self.search_input = False
        self.vocabulary_container = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "link" and values.get("href"):
            self.assets.append(values["href"])
        if tag == "script" and values.get("src"):
            self.assets.append(values["src"])
        if tag == "style":
            self.inline_style = True
        if tag == "script" and not values.get("src"):
            self.inline_script = True
        if tag == "input" and values.get("id") == "word-search":
            self.search_input = True
        if tag == "section" and values.get("id") == "vocabulary-grid":
            self.vocabulary_container = True


def main():
    parser = AssetParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    entries = payload["entries"]

    missing = [asset for asset in parser.assets if not (ROOT / asset).is_file()]
    assert not parser.inline_style, "Styles must live in assets/css/"
    assert not parser.inline_script, "Scripts must live in assets/js/"
    assert not missing, f"Missing HTML assets: {missing}"
    assert parser.search_input, "A search input is required"
    assert parser.vocabulary_container, "A dynamic vocabulary container is required"
    assert (ROOT / "assets" / "js" / "app.js").is_file()
    assert (ROOT / "assets" / "js" / "vocabulary.js").is_file()
    assert (ROOT / "assets" / "js" / "audio-player.js").is_file()
    assert len(entries) == 68
    assert len({entry["id"] for entry in entries}) == len(entries)
    for entry in entries:
        if entry.get("source") == "duolingo":
            continue
        assert (ROOT / entry["image"]["src"]).is_file()
        assert (ROOT / entry["audio"]["src"]).is_file()
    assert b"file:///" not in (ROOT / "dist" / "carnet-francais.pdf").read_bytes(), "PDF must not expose local file URLs"
    assert "file:///" not in (ROOT / "scripts" / "generate_pdf.py").read_text(encoding="utf-8")
    print("Static-site validation passed.")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, json.JSONDecodeError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
