"""Generate French word and sentence audio for every complete vocabulary card."""

import asyncio
import json
from pathlib import Path
import sys

import edge_tts

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = PROJECT_ROOT / "assets" / "data" / "vocabulary.json"
VOICE = "fr-FR-HenriNeural"


async def generate_audio(text, relative_target):
    target = PROJECT_ROOT / relative_target
    target.parent.mkdir(parents=True, exist_ok=True)
    communication = edge_tts.Communicate(text, VOICE)
    await communication.save(str(target))
    return target


async def generate_entry_audio(entry):
    word_target, sentence_target = await asyncio.gather(
        generate_audio(entry["word"], entry["audio"]["src"]),
        generate_audio(entry["sentence"], entry["sentenceAudio"]["src"]),
    )
    return word_target, sentence_target


async def main():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    targets = await asyncio.gather(*(generate_entry_audio(entry) for entry in catalog["entries"]))
    for word_target, sentence_target in targets:
        print(word_target)
        print(sentence_target)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (OSError, ValueError, edge_tts.exceptions.NoAudioReceived) as error:
        print(f"Audio generation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
