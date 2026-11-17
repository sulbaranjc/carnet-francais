#!/usr/bin/env python3
"""Generate a consistent vector illustration for every complete vocabulary card."""

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


def motif(kind: str, primary: str, accent: str) -> str:
    if kind in {"famille", "personne", "rencontre", "presentation"}:
        return f'''<circle cx="82" cy="53" r="19" fill="{primary}"/><path d="M43 132c4-35 22-53 39-53s35 18 39 53" fill="{accent}"/><circle cx="119" cy="68" r="14" fill="#F6C59D"/>'''
    if kind in {"nourriture", "patisserie", "commande"}:
        return f'''<ellipse cx="83" cy="119" rx="49" ry="12" fill="#D6C4AF"/><path d="M48 106h70l-8 14H56z" fill="{primary}"/><path d="M62 91c9-20 25-20 38 0" fill="none" stroke="{accent}" stroke-width="11" stroke-linecap="round"/>'''
    if kind in {"dialogue", "conversation", "politesse", "reponse", "emotion"}:
        return f'''<path d="M31 43h79a13 13 0 0 1 13 13v32a13 13 0 0 1-13 13H77l-20 17 4-17H31a13 13 0 0 1-13-13V56a13 13 0 0 1 13-13z" fill="{primary}"/><circle cx="54" cy="72" r="6" fill="white"/><circle cx="76" cy="72" r="6" fill="white"/><circle cx="98" cy="72" r="6" fill="white"/>'''
    if kind in {"lieu", "maison", "position", "objet", "association"}:
        return f'''<path d="M35 77 82 37l47 40v47H35z" fill="{primary}"/><path d="M73 124V91h19v33" fill="{accent}"/><rect x="48" y="88" width="15" height="15" rx="2" fill="white"/><rect x="101" y="88" width="15" height="15" rx="2" fill="white"/>'''
    if kind in {"temps", "mouvement", "voyage"}:
        return f'''<circle cx="82" cy="82" r="43" fill="white" stroke="{primary}" stroke-width="12"/><path d="M82 54v29l22 14" fill="none" stroke="{accent}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 123h96" stroke="{primary}" stroke-width="7" stroke-linecap="round"/>'''
    if kind in {"animal", "nature"}:
        return f'''<circle cx="82" cy="82" r="35" fill="{primary}"/><path d="M55 58 43 35l27 13M109 58l12-23-27 13" fill="{accent}"/><circle cx="69" cy="78" r="4"/><circle cx="95" cy="78" r="4"/><path d="M75 97q7 7 14 0" fill="none" stroke="#334" stroke-width="4" stroke-linecap="round"/>'''
    return f'''<circle cx="82" cy="82" r="43" fill="{primary}"/><path d="M61 82h42M82 61v42" stroke="white" stroke-width="10" stroke-linecap="round"/>'''


def render(entry: dict) -> str:
    background, primary, accent = PALETTES.get(entry.get("illustrationKind"), ("#E9F0F7", "#427AA1", "#E49354"))
    word = html.escape(entry["word"])
    alt = html.escape(entry["image"]["alt"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="330" height="300" viewBox="0 0 165 150" role="img" aria-labelledby="title desc">
  <title id="title">{word}</title><desc id="desc">{alt}</desc>
  <rect width="165" height="150" rx="16" fill="{background}"/>
  <circle cx="132" cy="28" r="13" fill="#fff" opacity=".72"/>
  <circle cx="28" cy="119" r="18" fill="#fff" opacity=".45"/>
  {motif(entry.get("illustrationKind", ""), primary, accent)}
  <rect x="16" y="126" width="133" height="17" rx="8.5" fill="#fff" opacity=".86"/>
  <text x="82.5" y="138" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="#28334A">{word}</text>
</svg>\n'''


def main() -> None:
    entries = json.loads(CATALOG.read_text(encoding="utf-8"))["entries"]
    created = 0
    for entry in entries:
        image = entry["image"]
        target = ROOT / image["src"]
        if target.suffix != ".svg":
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(entry), encoding="utf-8")
        created += 1
    print(f"Generated {created} vocabulary illustrations.")


if __name__ == "__main__":
    main()
