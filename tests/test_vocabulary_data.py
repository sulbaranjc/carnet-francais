import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data" / "vocabulary.json"
DUOLINGO_TOTAL = 64


def test_vocabulary_data_is_a_physical_json_catalog():
    assert DATA_PATH.is_file(), "Vocabulary must be stored in assets/data/vocabulary.json"

    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    entries = payload["entries"]

    assert len(entries) == DUOLINGO_TOTAL
    assert len({entry["id"] for entry in entries}) == DUOLINGO_TOTAL
    assert [entry["number"] for entry in entries] == list(range(1, DUOLINGO_TOTAL + 1))
    assert {entry["word"] for entry in entries} >= {
        "pas du tout",
        "ma tante",
        "tante",
        "bonjour",
        "thé",
    }

    for entry in entries:
        assert {"id", "number", "word", "article", "ipa", "sentence", "rule"} <= entry.keys()
        assert entry["word"]
        assert entry["rule"]

        if entry.get("source") == "duolingo":
            assert entry["importGloss"]
            assert entry["learningState"] == "à enrichir"
            assert not entry["ipa"]
            assert not entry["sentence"]
            assert "image" not in entry
            assert "audio" not in entry
            assert "sentenceAudio" not in entry
        else:
            assert entry["sentence"]
            assert {"image", "audio", "sentenceAudio"} <= entry.keys()
            assert {"name", "src", "alt"} <= entry["image"].keys()
            assert {"name", "src"} <= entry["audio"].keys()
            assert {"name", "src"} <= entry["sentenceAudio"].keys()
            assert (ROOT / entry["image"]["src"]).is_file()
            assert (ROOT / entry["audio"]["src"]).is_file()
            assert (ROOT / entry["sentenceAudio"]["src"]).is_file()


if __name__ == "__main__":
    test_vocabulary_data_is_a_physical_json_catalog()
    print("Vocabulary data test passed.")
