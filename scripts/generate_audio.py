"""Generate the French phrase audio defined in the vocabulary catalog."""

import asyncio
import json
from pathlib import Path
import sys

import edge_tts

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = PROJECT_ROOT / "assets" / "data" / "vocabulary.json"
VOICE = "fr-FR-HenriNeural"


async def generate_sentence_audio(entry):
    target = PROJECT_ROOT / entry["sentenceAudio"]["src"]
    target.parent.mkdir(parents=True, exist_ok=True)
    communication = edge_tts.Communicate(entry["sentence"], VOICE)
    await communication.save(str(target))
    return target


async def main():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    targets = await asyncio.gather(*(generate_sentence_audio(entry) for entry in catalog["entries"]))
    for target in targets:
        print(target)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (OSError, ValueError, edge_tts.exceptions.NoAudioReceived) as error:
        print(f"Audio generation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
