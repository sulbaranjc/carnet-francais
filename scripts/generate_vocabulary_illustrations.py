#!/usr/bin/env python3
"""Generate meaningful, consistent vector illustrations for vocabulary cards.

The illustrations use a compact visual vocabulary: concrete nouns get a direct
scene, while grammar and conversational phrases get a conventional contextual
cue (question, direction, agreement, contrast, greeting or negation).
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "assets" / "data" / "vocabulary.json"

PALETTES = {
    "famille": ("#FDE7D7", "#D9653B", "#3C6E71"),
    "nourriture": ("#FFF0C9", "#C96A2B", "#5A8D67"),
    "patisserie": ("#FBE0E5", "#9A4E62", "#D39B2B"),
    "conversation": ("#DCEFFA", "#397AAB", "#E89A59"),
    "salutation": ("#E6F3E8", "#4B8A5D", "#E6AB41"),
    "voyage": ("#E6EFFA", "#3F72A3", "#E07855"),
    "temps": ("#EEE8FA", "#7057A8", "#D59C2D"),
    "adjectif": ("#FBE8D5", "#C96B3B", "#675B9C"),
    "negation": ("#F9E1E1", "#B65050", "#555C7A"),
}

SCENE_BY_ID = {
    "pas-du-tout": "negation", "mais": "contrast", "toujours": "clock",
    "interessant": "book", "tres": "intensity", "est": "position",
    "bien-sur": "agreement", "mechant": "wolf", "amusant": "game",
    "il-vient": "arrival", "elle-vient": "arrival", "viens-de": "arrival",
    "tu-viens-de": "arrival", "il-habite": "house", "elle-habite": "house",
    "a": "school", "de": "possession", "une": "article", "un": "article",
    "j-ai": "possession", "tu-as": "possession", "oh": "surprise",
    "tu-viens-d-ou": "question-place", "a-bientot": "goodbye",
    "moi-aussi": "agreement", "et-toi": "question", "je-m-appelle": "name-tag",
    "bien": "agreement", "ca-va": "wellbeing", "enchanté": "handshake",
    "au-revoir": "goodbye", "parfait": "medal", "ou": "choice",
    "non": "negation", "merci": "thanks", "et": "connection", "oui": "agreement",
    "je-voudrais": "order", "s-il-vous-plait": "order", "monsieur": "personne",
}


def person(primary: str, accent: str) -> str:
    return f'''<circle cx="76" cy="52" r="18" fill="#F6C59D"/><path d="M41 124c4-33 20-49 35-49s31 16 35 49" fill="{primary}"/><circle cx="117" cy="68" r="13" fill="{accent}"/>'''


def speech(primary: str) -> str:
    return f'''<path d="M28 43h83a13 13 0 0 1 13 13v31a13 13 0 0 1-13 13H78l-21 18 5-18H28a13 13 0 0 1-13-13V56a13 13 0 0 1 13-13z" fill="{primary}"/><circle cx="52" cy="72" r="6" fill="white"/><circle cx="75" cy="72" r="6" fill="white"/><circle cx="98" cy="72" r="6" fill="white"/>'''


def motif(kind: str, primary: str, accent: str) -> str:
    if kind == "negation":
        return f'''<path d="M43 102h47l-6 15H49z" fill="#F4C78C"/><path d="M55 84c6-13 18-13 24 0" fill="none" stroke="{accent}" stroke-width="8" stroke-linecap="round"/><circle cx="112" cy="64" r="27" fill="#C64F4F"/><path d="m96 64 32 0" stroke="white" stroke-width="8" stroke-linecap="round"/>'''
    if kind == "contrast":
        return f'''<rect x="26" y="51" width="47" height="57" rx="10" fill="{primary}"/><rect x="92" y="51" width="47" height="57" rx="10" fill="{accent}"/><path d="M80 53v52" stroke="white" stroke-width="7"/><path d="m74 76 6 6 6-6M74 90l6-6 6 6" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'''
    if kind == "clock":
        return f'''<circle cx="82" cy="80" r="42" fill="white" stroke="{primary}" stroke-width="11"/><path d="M82 53v29l22 13" fill="none" stroke="{accent}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 122h96" stroke="{primary}" stroke-width="7" stroke-linecap="round"/>'''
    if kind == "book":
        return f'''<path d="M36 50c18-8 32-4 46 8v61c-14-12-28-16-46-8zM128 50c-18-8-32-4-46 8v61c14-12 28-16 46-8z" fill="{primary}"/><path d="M82 59v59" stroke="white" stroke-width="4"/><path d="M51 70h18M96 70h18M51 86h18M96 86h18" stroke="white" stroke-width="4" stroke-linecap="round"/>'''
    if kind == "intensity":
        return f'''<path d="m82 35 10 24 26 2-20 17 6 26-22-14-22 14 6-26-20-17 26-2z" fill="{primary}"/><path d="m124 72 6 14 16 1-12 11 4 16-14-9-14 9 4-16-12-11 16-1z" fill="{accent}"/><path d="m40 72 6 14 16 1-12 11 4 16-14-9-14 9 4-16-12-11 16-1z" fill="{accent}"/>'''
    if kind == "position":
        return f'''<rect x="34" y="96" width="96" height="12" rx="5" fill="{accent}"/><path d="M44 108v20M120 108v20" stroke="{accent}" stroke-width="7"/><circle cx="82" cy="72" r="27" fill="{primary}"/><path d="M62 55 53 39l20 9M102 55l9-16-20 9" fill="{accent}"/><circle cx="72" cy="71" r="3"/><circle cx="92" cy="71" r="3"/><path d="M74 86q8 7 16 0" fill="none" stroke="#27374D" stroke-width="3"/>'''
    if kind in {"agreement", "wellbeing"}:
        return f'''<circle cx="82" cy="78" r="39" fill="{primary}"/><path d="m61 78 14 14 30-31" fill="none" stroke="white" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'''
    if kind == "wolf":
        return f'''<path d="M48 109V61l18 13 16-28 16 28 18-13v48z" fill="{primary}"/><circle cx="70" cy="83" r="4" fill="white"/><circle cx="94" cy="83" r="4" fill="white"/><path d="m74 98 8 6 8-6" fill="none" stroke="white" stroke-width="4"/>'''
    if kind == "game":
        return f'''<rect x="43" y="57" width="78" height="54" rx="20" fill="{primary}"/><circle cx="67" cy="84" r="8" fill="white"/><path d="M59 84h16M67 76v16" stroke="{accent}" stroke-width="4"/><circle cx="99" cy="78" r="6" fill="white"/><circle cx="108" cy="91" r="6" fill="white"/><path d="M44 42 56 31M108 35l13-11" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>'''
    if kind in {"arrival", "question-place", "question"}:
        return f'''<path d="M33 102h65" stroke="{primary}" stroke-width="9" stroke-linecap="round"/><path d="m87 84 22 18-22 18" fill="none" stroke="{accent}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><circle cx="57" cy="64" r="15" fill="{primary}"/><path d="M34 95c3-21 12-31 23-31s20 10 23 31" fill="{primary}"/><text x="123" y="64" text-anchor="middle" font-family="Arial" font-size="30" font-weight="700" fill="{accent}">{"?" if kind.startswith("question") else ""}</text>'''
    if kind in {"house", "school"}:
        symbol = "A" if kind == "school" else ""
        return f'''<path d="M35 76 82 36l47 40v48H35z" fill="{primary}"/><path d="M73 124V91h19v33" fill="{accent}"/><rect x="47" y="87" width="15" height="15" rx="2" fill="white"/><rect x="102" y="87" width="15" height="15" rx="2" fill="white"/><text x="82" y="77" text-anchor="middle" font-family="Arial" font-size="21" font-weight="700" fill="white">{symbol}</text>'''
    if kind in {"possession", "article", "choice", "connection"}:
        center = "UN" if kind == "article" else ("?" if kind == "choice" else "=")
        return f'''<circle cx="57" cy="79" r="27" fill="{primary}"/><circle cx="108" cy="79" r="27" fill="{accent}"/><path d="M76 79h14" stroke="white" stroke-width="6" stroke-linecap="round"/><text x="57" y="87" text-anchor="middle" font-family="Arial" font-size="17" font-weight="700" fill="white">{center if kind == "article" else ""}</text><text x="108" y="87" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700" fill="white">{center if kind != "article" else ""}</text>'''
    if kind in {"goodbye", "handshake", "name-tag", "medal", "order", "thanks"}:
        if kind == "goodbye":
            return f'''{person(primary, accent)}<path d="M119 42c14 10 15 26 4 37" fill="none" stroke="{accent}" stroke-width="7" stroke-linecap="round"/><path d="m119 42 12 3-4 12" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'''
        if kind == "handshake":
            return f'''<path d="m32 80 25-20 21 16 13-11 42 33-22 23-33-28-12 10z" fill="{primary}"/><path d="m31 83 20 20 16-15" fill="none" stroke="{accent}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'''
        if kind == "name-tag":
            return f'''<rect x="34" y="52" width="96" height="61" rx="13" fill="{primary}"/><circle cx="57" cy="76" r="11" fill="white"/><path d="M76 70h34M76 87h24" stroke="white" stroke-width="6" stroke-linecap="round"/>'''
        if kind == "medal":
            return f'''<path d="m60 43 22 24 23-24 11 42H49z" fill="{accent}"/><circle cx="82" cy="97" r="27" fill="{primary}"/><path d="m82 80 6 13 14 2-10 10 3 14-13-7-13 7 3-14-10-10 14-2z" fill="white"/>'''
        return f'''<rect x="37" y="60" width="91" height="52" rx="12" fill="{primary}"/><path d="M54 82h56M54 96h39" stroke="white" stroke-width="6" stroke-linecap="round"/><circle cx="123" cy="52" r="16" fill="{accent}"/>'''
    if kind in {"famille", "personne", "rencontre", "presentation"}:
        return person(primary, accent)
    if kind in {"nourriture", "patisserie", "commande"}:
        return f'''<ellipse cx="83" cy="119" rx="49" ry="12" fill="#D6C4AF"/><path d="M48 106h70l-8 14H56z" fill="{primary}"/><path d="M62 91c9-20 25-20 38 0" fill="none" stroke="{accent}" stroke-width="11" stroke-linecap="round"/>'''
    if kind in {"dialogue", "conversation", "politesse", "reponse", "emotion"}:
        return speech(primary)
    if kind in {"lieu", "maison", "objet", "association"}:
        return f'''<path d="M35 77 82 37l47 40v47H35z" fill="{primary}"/><path d="M73 124V91h19v33" fill="{accent}"/><rect x="48" y="88" width="15" height="15" rx="2" fill="white"/><rect x="101" y="88" width="15" height="15" rx="2" fill="white"/>'''
    if kind in {"temps", "mouvement", "voyage"}:
        return motif("clock", primary, accent)
    if kind in {"animal", "nature"}:
        return f'''<circle cx="82" cy="82" r="35" fill="{primary}"/><path d="M55 58 43 35l27 13M109 58l12-23-27 13" fill="{accent}"/><circle cx="69" cy="78" r="4"/><circle cx="95" cy="78" r="4"/><path d="M75 97q7 7 14 0" fill="none" stroke="#334" stroke-width="4" stroke-linecap="round"/>'''
    return speech(primary)


def render(entry: dict) -> str:
    kind = SCENE_BY_ID.get(entry["id"], entry.get("illustrationKind", ""))
    background, primary, accent = PALETTES.get(entry.get("illustrationKind"), ("#E9F0F7", "#427AA1", "#E49354"))
    word = html.escape(entry["word"])
    alt = html.escape(entry["image"]["alt"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="330" height="300" viewBox="0 0 165 150" role="img" aria-labelledby="title desc">
  <title id="title">{word}</title><desc id="desc">{alt}</desc>
  <rect width="165" height="150" rx="16" fill="{background}"/>
  <circle cx="132" cy="28" r="13" fill="#fff" opacity=".72"/>
  <circle cx="28" cy="119" r="18" fill="#fff" opacity=".45"/>
  {motif(kind, primary, accent)}
  <rect x="16" y="126" width="133" height="17" rx="8.5" fill="#fff" opacity=".86"/>
  <text x="82.5" y="138" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#28334A">{word}</text>
</svg>\n'''


def main() -> None:
    entries = json.loads(CATALOG.read_text(encoding="utf-8"))["entries"]
    created = 0
    for entry in entries:
        target = ROOT / entry["image"]["src"]
        if target.suffix != ".svg":
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(entry), encoding="utf-8")
        created += 1
    print(f"Generated {created} contextual vocabulary illustrations.")


if __name__ == "__main__":
    main()
