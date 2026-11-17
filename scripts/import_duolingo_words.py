#!/usr/bin/env python3
"""Importa el catálogo de palabras visible de Duolingo desde un árbol CUA guardado.

No usa cookies ni APIs internas. El archivo de entrada contiene únicamente el texto
expuesto por la página autenticada Practice Hub > Words.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

PAIR_PATTERN = re.compile(r'heading "([^"]+)".*?paragraph "([^"]+)"', re.DOTALL)
REQUIRED_CARD_FIELDS = {
    "id", "number", "word", "article", "ipa", "sentence", "rule", "image", "audio", "sentenceAudio"
}


def normalized_word(value: str) -> str:
    decomposed = unicodedata.normalize("NFD", value.lower())
    without_marks = "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", without_marks)


def entry_id(word: str) -> str:
    ascii_word = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_word.lower()).strip("-")


def extract_words(tree: str) -> list[tuple[str, str]]:
    marker = re.search(r"\b\d+ palabras\b", tree)
    if not marker:
        raise ValueError("No se encontró el contador de palabras de Duolingo.")

    pairs = PAIR_PATTERN.findall(tree[marker.start() :])
    records: list[tuple[str, str]] = []
    seen: set[str] = set()
    for word, gloss in pairs:
        if word not in seen:
            seen.add(word)
            records.append((word, gloss))
    if not records:
        raise ValueError("No se pudieron extraer filas de vocabulario.")
    return records


def build_catalog(words: list[tuple[str, str]], previous_entries: list[dict]) -> list[dict]:
    rich_entries = {normalized_word(entry["word"]): entry for entry in previous_entries if "audio" in entry}
    catalog: list[dict] = []

    for number, (word, gloss) in enumerate(words, start=1):
        previous = rich_entries.get(normalized_word(word))
        if previous:
            entry = {**previous, "number": number, "word": word}
        else:
            entry = {
                "id": entry_id(word),
                "number": number,
                "word": word,
                "article": "",
                "ipa": "",
                "sentence": "",
                "rule": "Importé de Duolingo — à enrichir.",
                "source": "duolingo",
                "importGloss": gloss,
                "learningState": "à enrichir",
            }
        catalog.append(entry)

    if len({entry["id"] for entry in catalog}) != len(catalog):
        raise ValueError("Des identifiants de vocabulaire ne sont pas uniques.")
    return catalog


def assert_complete_cards(catalog: list[dict]) -> None:
    incomplete = [
        entry["word"]
        for entry in catalog
        if not REQUIRED_CARD_FIELDS <= entry.keys()
        or not entry["ipa"]
        or not entry["sentence"]
        or not entry["rule"]
    ]
    if incomplete:
        words = ", ".join(incomplete)
        raise ValueError(
            "Importation annulée : chaque mot doit être enrichi avec IPA, phrase, règle, illustration et deux audios avant publication. "
            f"Entrées à compléter : {words}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tree", type=Path, help="Archivo de árbol CUA de Duolingo")
    parser.add_argument("catalog", type=Path, help="assets/data/vocabulary.json a actualizar")
    args = parser.parse_args()

    words = extract_words(args.tree.read_text(encoding="utf-8"))
    payload = json.loads(args.catalog.read_text(encoding="utf-8"))
    payload["version"] = max(2, payload.get("version", 1))
    candidate = build_catalog(words, payload.get("entries", []))
    assert_complete_cards(candidate)
    payload["entries"] = candidate
    args.catalog.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(payload['entries'])} unique Duolingo entries.")


if __name__ == "__main__":
    main()
