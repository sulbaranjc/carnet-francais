import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data" / "vocabulary.json"
DUOLINGO_TOTAL = 68
REQUIRED_NEW_WORDS = {"c'est", "incroyable", "vraiment", "formidable"}
REQUIRED_CARD_FIELDS = {
    "id",
    "number",
    "word",
    "translation",
    "article",
    "ipa",
    "sentence",
    "sentenceTranslation",
    "rule",
    "image",
    "audio",
    "sentenceAudio",
}


def test_every_catalog_entry_is_a_complete_learning_card():
    assert DATA_PATH.is_file(), "Vocabulary must be stored in assets/data/vocabulary.json"

    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    entries = payload["entries"]

    assert len(entries) == DUOLINGO_TOTAL
    assert len({entry["id"] for entry in entries}) == DUOLINGO_TOTAL
    assert [entry["number"] for entry in entries] == list(range(1, DUOLINGO_TOTAL + 1))
    assert REQUIRED_NEW_WORDS <= {entry["word"] for entry in entries}

    for entry in entries:
        assert REQUIRED_CARD_FIELDS <= entry.keys(), f"Incomplete card: {entry['word']}"
        assert entry["word"]
        assert entry["translation"]
        assert entry["ipa"].startswith("/") and entry["ipa"].endswith("/")
        assert entry["sentence"]
        assert entry["sentenceTranslation"]
        assert entry["rule"]
        assert entry.get("learningState") != "à enrichir"

        assert {"name", "src", "alt"} <= entry["image"].keys()
        assert {"name", "src"} <= entry["audio"].keys()
        assert {"name", "src"} <= entry["sentenceAudio"].keys()
        assert (ROOT / entry["image"]["src"]).is_file()
        assert (ROOT / entry["audio"]["src"]).is_file()
        assert (ROOT / entry["sentenceAudio"]["src"]).is_file()


def test_mon_frere_reuses_juan_carlos_brother_portrait():
    entries = json.loads(DATA_PATH.read_text(encoding="utf-8"))["entries"]
    by_word = {entry["word"]: entry for entry in entries}

    assert by_word["mon frère"]["image"] == by_word["frère"]["image"]


def test_tante_cards_reuse_juan_carlos_aunt_portrait():
    entries = json.loads(DATA_PATH.read_text(encoding="utf-8"))["entries"]
    by_word = {entry["word"]: entry for entry in entries}

    assert by_word["ma tante"]["image"] == by_word["tante"]["image"]
    assert by_word["tante"]["image"]["src"] == "assets/images/tante-photo.png"


if __name__ == "__main__":
    test_every_catalog_entry_is_a_complete_learning_card()
    test_mon_frere_reuses_juan_carlos_brother_portrait()
    test_tante_cards_reuse_juan_carlos_aunt_portrait()
    print("Vocabulary data test passed.")
