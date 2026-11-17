from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.audio_ids = set()
        self.button_audio_ids = set()
        self.status_ids = set()
        self.inline_style = False
        self.inline_script = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "link" and values.get("href"):
            self.assets.append(values["href"])
        if tag in {"img", "audio", "script"} and values.get("src"):
            self.assets.append(values["src"])
        if tag == "audio" and values.get("id"):
            self.audio_ids.add(values["id"])
        if tag == "button" and values.get("data-audio"):
            self.button_audio_ids.add(values["data-audio"])
        if tag == "p" and values.get("id", "").startswith("status-"):
            self.status_ids.add(values["id"].removeprefix("status-"))
        if tag == "style":
            self.inline_style = True
        if tag == "script" and not values.get("src"):
            self.inline_script = True


def main():
    parser = AssetParser()
    parser.feed(INDEX.read_text(encoding="utf-8"))

    missing = [asset for asset in parser.assets if not (ROOT / asset).is_file()]
    assert not parser.inline_style, "Styles must live in assets/css/"
    assert not parser.inline_script, "Scripts must live in assets/js/"
    assert not missing, f"Missing assets: {missing}"
    assert parser.button_audio_ids == parser.audio_ids, "Audio buttons must match audio elements"
    assert parser.status_ids == parser.audio_ids, "Every audio element needs a playback status"
    assert len(list((ROOT / "assets" / "media" / "audio").glob("*.mp3"))) == 4
    assert len(list((ROOT / "assets" / "images").glob("*.png"))) == 4
    assert (ROOT / "assets" / "css" / "main.css").is_file()
    assert (ROOT / "assets" / "js" / "audio-player.js").is_file()
    assert b"file:///" not in (ROOT / "dist" / "carnet-francais.pdf").read_bytes(), "PDF must not expose local file URLs"
    assert "file:///" not in (ROOT / "scripts" / "generate_pdf.py").read_text(encoding="utf-8")
    print("Static-site validation passed.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
