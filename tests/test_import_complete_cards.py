import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "import_duolingo_words.py"

spec = importlib.util.spec_from_file_location("import_duolingo_words", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_import_rejects_a_word_without_a_complete_card():
    candidate = module.build_catalog([("mot inconnu", "unknown word")], [])
    try:
        module.assert_complete_cards(candidate)
    except ValueError as error:
        assert "Importation annulée" in str(error)
        assert "mot inconnu" in str(error)
    else:
        raise AssertionError("An incomplete word must never be written to the catalog")


if __name__ == "__main__":
    test_import_rejects_a_word_without_a_complete_card()
    print("Complete-card import guard test passed.")
