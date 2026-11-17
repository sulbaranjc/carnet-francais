import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data" / "vocabulary.json"


def test_vocabulary_data_is_a_physical_json_catalog():
    assert DATA_PATH.is_file(), "Vocabulary must be stored in assets/data/vocabulary.json"

    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    entries = payload["entries"]

    assert len(entries) == 4
    assert [entry["id"] for entry in entries] == ["tante", "oncle", "the", "bonjour"]
    for entry in entries:
        assert {
            "id",
            "number",
            "word",
            "article",
            "ipa",
            "sentence",
            "rule",
            "image",
            "audio",
            "sentenceAudio",
        } <= entry.keys()
        assert {"name", "src", "alt"} <= entry["image"].keys()
        assert {"name", "src"} <= entry["audio"].keys()
        assert {"name", "src"} <= entry["sentenceAudio"].keys()
        assert (ROOT / entry["image"]["src"]).is_file()
        assert (ROOT / entry["audio"]["src"]).is_file()
        assert (ROOT / entry["sentenceAudio"]["src"]).is_file()


if __name__ == "__main__":
    test_vocabulary_data_is_a_physical_json_catalog()
    print("Vocabulary data test passed.")
