#!/usr/bin/env python3
"""Construye cards completos para cada palabra importada de Duolingo.

La escritura falla antes de modificar el catálogo si falta cualquier componente
pedagógico. Así una importación nueva no puede publicar cards incompletos.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "assets" / "data" / "vocabulary.json"

# word, article, IPA, French example, French grammar note, image alt, visual category
ROWS = [
    ("pas du tout", "", "/pa dy tu/", "Je n'aime pas du tout le café.", "Locution adverbiale de négation renforcée, généralement employée avec « ne » dans une phrase soignée.", "Une personne repousse une tasse de café avec une expression de refus.", "negation"),
    ("mais", "", "/mɛ/", "J'aime le thé, mais pas le café.", "Conjonction de coordination qui exprime une opposition ou une restriction.", "Deux boissons posées côte à côte, avec une personne qui choisit le thé.", "conversation"),
    ("mon frère", "le", "/mɔ̃ fʁɛʁ/", "Mon frère joue au football.", "« Frère » est un nom masculin. « Mon » est le déterminant possessif masculin singulier.", "Un garçon joue au football dans un parc.", "famille"),
    ("mon fils", "le", "/mɔ̃ fis/", "Mon fils lit une histoire.", "« Fils » est un nom masculin. Le « s » final se prononce /s/ dans « fils ».", "Un jeune garçon lit un livre illustré.", "famille"),
    ("ma tante", "la", "/ma tɑ̃t/", "Ma tante prépare le dîner.", "« Tante » est un nom féminin. « Ma » est le déterminant possessif féminin singulier.", "Une femme prépare un repas dans une cuisine.", "famille"),
    ("toujours", "", "/tu.ʒuʁ/", "Il arrive toujours à l'heure.", "Adverbe qui indique une action habituelle, continue ou répétée.", "Une personne arrive devant une horloge à l'heure exacte.", "temps"),
    ("intéressant", "", "/ɛ̃.te.ʁɛ.sɑ̃/", "Ce livre est très intéressant.", "Adjectif masculin singulier ; au féminin, on ajoute généralement « e » : « intéressante ».", "Une personne lit un livre avec beaucoup d'attention.", "adjectif"),
    ("très", "", "/tʁɛ/", "La classe est très calme.", "Adverbe d'intensité placé devant un adjectif ou un autre adverbe.", "Une salle de classe silencieuse avec des élèves attentifs.", "intensite"),
    ("ma nièce", "la", "/ma njɛs/", "Ma nièce dessine un chat.", "« Nièce » est un nom féminin. « Ma » est le déterminant possessif féminin singulier.", "Une jeune fille dessine un chat sur une feuille.", "famille"),
    ("ma sœur", "la", "/ma sœʁ/", "Ma sœur chante bien.", "« Sœur » est un nom féminin. « Ma » est le déterminant possessif féminin singulier.", "Une fille chante devant un microphone.", "famille"),
    ("elle", "", "/ɛl/", "Elle parle avec son amie.", "Pronom personnel sujet de la troisième personne du singulier, employé pour une personne ou une chose féminine.", "Une femme parle avec une amie.", "conversation"),
    ("est", "", "/ɛ/", "Le chat est sur la table.", "Forme du verbe « être » à la troisième personne du singulier : il est, elle est, on est.", "Un chat est assis sur une table.", "position"),
    ("bien sûr", "", "/bjɛ̃ syʁ/", "Bien sûr, je peux t'aider.", "Expression utilisée pour confirmer une réponse ou marquer l'évidence.", "Une personne sourit et fait un signe positif de la tête.", "conversation"),
    ("il", "", "/il/", "Il regarde le ciel.", "Pronom personnel sujet de la troisième personne du singulier, souvent employé pour une personne masculine.", "Un garçon regarde le ciel avec des nuages.", "personne"),
    ("méchant", "", "/me.ʃɑ̃/", "Le loup est méchant dans cette histoire.", "Adjectif masculin singulier ; au féminin, on écrit « méchante ».", "Un loup au regard sévère dans un conte.", "adjectif"),
    ("amusant", "", "/a.my.zɑ̃/", "Ce jeu est amusant.", "Adjectif masculin singulier ; au féminin, on écrit « amusante ».", "Des enfants rient en jouant à un jeu.", "adjectif"),
    ("il vient", "", "/il vjɛ̃/", "Il vient à la maison ce soir.", "« Vient » est la forme du verbe « venir » à la troisième personne du singulier.", "Un garçon marche vers une maison.", "mouvement"),
    ("il habite", "", "/il a.bit/", "Il habite près de l'école.", "« Habite » est la forme du verbe « habiter » à la troisième personne du singulier.", "Un garçon se tient devant sa maison près d'une école.", "lieu"),
    ("neveu", "le", "/nə.vø/", "Mon neveu joue dans le jardin.", "« Neveu » est un nom masculin ; le féminin correspondant est « nièce ».", "Un jeune garçon joue dans un jardin.", "famille"),
    ("nièce", "la", "/njɛs/", "Ma nièce aime les animaux.", "« Nièce » est un nom féminin ; le masculin correspondant est « neveu ».", "Une jeune fille caresse un petit chien.", "famille"),
    ("à", "", "/a/", "Elle va à l'école.", "« À » introduit souvent un lieu, une personne ou une heure.", "Une fille marche vers une école.", "lieu"),
    ("elle habite", "", "/ɛl a.bit/", "Elle habite près du parc.", "« Habite » est la forme du verbe « habiter » avec « elle » au présent.", "Une fille devant sa maison près d'un parc.", "maison"),
    ("maintenant", "", "/mɛ̃.tə.nɑ̃/", "Maintenant, nous lisons une histoire.", "« Maintenant » indique le moment présent.", "Des enfants lisent un livre maintenant.", "temps"),
    ("oncle", "l’", "/ɔ̃kl/", "Mon oncle aime cuisiner.", "« Oncle » est un nom masculin : un oncle, l'oncle.", "Un homme cuisine dans une cuisine.", "famille"),
    ("tante", "la", "/tɑ̃t/", "Ma tante arrive ce soir.", "« Tante » est un nom féminin : une tante, la tante.", "Une femme arrive avec une valise.", "famille"),
    ("de", "", "/də/", "Le vélo de Paul est bleu.", "« De » peut exprimer la possession, l'origine ou la matière ; il devient « d' » devant une voyelle.", "Un vélo bleu appartient à Paul.", "objet"),
    ("une", "", "/yn/", "Une fleur pousse dans le jardin.", "« Une » est un article indéfini féminin singulier.", "Une fleur colorée dans un jardin.", "nature"),
    ("elle vient", "", "/ɛl vjɛ̃/", "Elle vient de Lyon.", "« Vient » est la forme du verbe « venir » avec « elle » au présent.", "Une fille arrive de Lyon avec un sac.", "voyage"),
    ("j'ai", "", "/ʒe/", "J'ai un petit chat.", "« J'ai » est la forme du verbe « avoir » avec « je » au présent.", "Un enfant tient un petit chat.", "animal"),
    ("fille", "la", "/fij/", "La fille dessine un soleil.", "« Fille » est un nom féminin : une fille, la fille.", "Une fille dessine un soleil.", "personne"),
    ("sœur", "la", "/sœʁ/", "Ma sœur joue au ballon.", "« Sœur » est un nom féminin : une sœur, la sœur.", "Une fille joue avec un ballon.", "famille"),
    ("fils", "le", "/fis/", "Son fils joue dans le jardin.", "« Fils » est un nom masculin ; au singulier, le « s » se prononce.", "Un garçon joue dans un jardin.", "famille"),
    ("tu as", "", "/ty a/", "Tu as une belle idée.", "« As » est la forme du verbe « avoir » avec « tu » au présent.", "Un enfant sourit avec une ampoule au-dessus de sa tête.", "idee"),
    ("oh", "", "/o/", "Oh, le chat dort ici !", "« Oh » est une interjection qui exprime une émotion ou une surprise.", "Un enfant surpris regarde un chat endormi.", "emotion"),
    ("frère", "le", "/fʁɛʁ/", "Mon frère aime le football.", "« Frère » est un nom masculin : un frère, le frère.", "Un garçon joue au football.", "famille"),
    ("tu viens de", "", "/ty vjɛ̃ də/", "Tu viens de Paris, n'est-ce pas ?", "« Viens » est la forme du verbe « venir » avec « tu » au présent ; « venir de » peut indiquer l'origine.", "Un garçon arrive de Paris avec une valise.", "voyage"),
    ("tu viens d'où", "", "/ty vjɛ̃ du/", "Tu viens d'où après l'école ?", "« Tu viens d'où ? » est une question familière pour demander l'origine ou le lieu de départ.", "Deux enfants parlent près d'une école.", "dialogue"),
    ("à bientôt", "", "/a bjɛ̃.to/", "À bientôt, Léa !", "« À bientôt » est une formule pour prendre congé et dire que l'on se reverra prochainement.", "Deux amis se disent au revoir en souriant.", "salutation"),
    ("viens de", "", "/vjɛ̃ də/", "Je viens de Marseille.", "« Viens » est une forme du verbe « venir » au présent ; avec « de » et un lieu, il indique l'origine.", "Une personne arrive de Marseille.", "voyage"),
    ("moi aussi", "", "/mwa o.si/", "Moi aussi, j'aime les histoires.", "« Moi aussi » sert à dire que l'on partage la même idée ou la même situation.", "Deux enfants lisent et aiment le même livre.", "dialogue"),
    ("je", "", "/ʒə/", "Je suis content aujourd'hui.", "« Je » est un pronom personnel sujet de la première personne du singulier.", "Un enfant se montre du doigt en souriant.", "personne"),
    ("et toi", "", "/e twa/", "Moi, ça va bien, et toi ?", "« Et toi ? » sert à poser la même question à une autre personne de façon informelle.", "Deux amis discutent face à face.", "conversation"),
    ("je m'appelle", "", "/ʒə ma.pɛl/", "Bonjour, je m'appelle Léa.", "« Je m'appelle » est la première personne du singulier du verbe pronominal « s'appeler ».", "Une élève se présente devant la classe.", "presentation"),
    ("bien", "", "/bjɛ̃/", "Je vais bien, merci.", "« Bien » est un adverbe ; il peut indiquer qu'une action ou un état est positif.", "Une personne sourit avec le pouce levé.", "emotion"),
    ("ça va", "", "/sa va/", "Bonjour, ça va ?", "« Ça va » est une expression courante pour demander ou dire comment on se sent.", "Deux personnes se saluent dans la rue.", "conversation"),
    ("enchanté", "", "/ɑ̃.ʃɑ̃.te/", "Enchanté, je m'appelle Hugo.", "« Enchanté » exprime le plaisir de rencontrer quelqu'un ; au féminin, on écrit « enchantée ».", "Deux personnes se serrent la main avec le sourire.", "rencontre"),
    ("au revoir", "", "/o ʁə.vwaʁ/", "Au revoir et à bientôt !", "« Au revoir » est une formule de politesse utilisée pour prendre congé.", "Une personne fait un signe de la main en partant.", "salutation"),
    ("parfait", "", "/paʁ.fɛ/", "Parfait, nous sommes prêts !", "« Parfait » est un adjectif masculin ; au féminin, on dit « parfaite ». Il peut aussi servir d’exclamation.", "Une élève sourit devant un exercice réussi.", "reussite"),
    ("ou", "", "/u/", "Tu veux du thé ou du café ?", "« Ou » présente un choix. Il ne faut pas le confondre avec « où », qui indique un lieu.", "Une tasse de thé et une tasse de café côte à côte.", "choix"),
    ("monsieur", "le", "/mə.sjø/", "Bonjour, monsieur Martin.", "« Monsieur » est un nom masculin de politesse ; son pluriel est « messieurs ».", "Un homme porte une veste et sourit.", "personne"),
    ("non", "", "/nɔ̃/", "Non, merci, je ne veux pas de sucre.", "« Non » sert à exprimer une réponse négative ou un refus.", "Une personne secoue doucement la tête.", "reponse"),
    ("sandwich", "le", "/sɑ̃d.witʃ/", "Je voudrais un sandwich, s'il vous plaît.", "« Sandwich » est un nom masculin ; on dit « un sandwich » ou « le sandwich ».", "Un sandwich avec du pain, du fromage et de la salade.", "nourriture"),
    ("merci", "", "/mɛʁ.si/", "Merci pour votre aide.", "« Merci » est une formule de politesse pour exprimer sa gratitude.", "Une personne remercie une autre avec un sourire.", "politesse"),
    ("et", "", "/e/", "Paul et Nina arrivent ensemble.", "« Et » est une conjonction qui relie des mots ou des groupes de mots.", "Deux enfants marchent ensemble.", "association"),
    ("oui", "", "/wi/", "Oui, je comprends.", "« Oui » sert à donner une réponse affirmative.", "Une personne acquiesce avec le sourire.", "reponse"),
    ("je voudrais", "", "/ʒə vu.dʁɛ/", "Je voudrais un croissant, s'il vous plaît.", "« Je voudrais » est le conditionnel présent de « vouloir » à la première personne ; il permet de demander poliment.", "Une cliente commande au comptoir d'une boulangerie.", "commande"),
    ("éclair", "l’", "/e.klɛʁ/", "L'éclair au chocolat est délicieux.", "« Éclair » est un nom masculin ; devant une voyelle, « le » devient « l' ».", "Un éclair au chocolat posé sur une assiette.", "patisserie"),
    ("croissant", "le", "/kʁwa.sɑ̃/", "Le croissant est encore chaud.", "« Croissant » est un nom masculin ; on dit « un croissant » ou « le croissant ».", "Un croissant doré sur une assiette.", "patisserie"),
    ("s'il vous plaît", "", "/sil vu plɛ/", "Un café, s'il vous plaît.", "« S'il vous plaît » est une formule de politesse employée pour faire une demande.", "Une personne commande poliment un café.", "politesse"),
    ("bonjour", "", "/bɔ̃.ʒuʁ/", "Bonjour, comment allez-vous ?", "« Bonjour » est une formule de salutation utilisée pendant la journée.", "Deux voisins se disent bonjour le matin.", "salutation"),
    ("un", "", "/œ̃/", "Un chat dort sur le canapé.", "« Un » est un article indéfini masculin singulier.", "Un chat dort sur un canapé.", "animal"),
    ("madame", "la", "/ma.dam/", "Bonjour, madame Dupont.", "« Madame » est un nom féminin de politesse pour s'adresser à une femme.", "Une femme sourit dans la rue.", "personne"),
    ("café", "le", "/ka.fe/", "Le café est chaud.", "« Café » est un nom masculin ; on dit « un café » ou « le café ».", "Une tasse de café fumante sur une table.", "nourriture"),
    ("thé", "le", "/te/", "Le thé est chaud.", "« Thé » est un nom masculin ; on dit « un thé » ou « le thé ».", "Une tasse de thé fumante sur une table.", "nourriture"),
]


def complete_entry(entry: dict, row: tuple[str, str, str, str, str, str, str]) -> dict:
    word, article, ipa, sentence, rule, image_alt, kind = row
    if entry["word"] != word:
        raise ValueError(f"Order mismatch: expected {word!r}, found {entry['word']!r}")
    identifier = entry["id"]
    entry.update(
        {
            "article": article,
            "ipa": ipa,
            "sentence": sentence,
            "rule": rule,
            "source": "duolingo",
            "learningState": "enrichi",
        }
    )
    entry.setdefault(
        "image",
        {"name": f"{identifier}.svg", "src": f"assets/images/{identifier}.svg", "alt": image_alt},
    )
    entry["image"]["alt"] = image_alt
    entry.setdefault("audio", {"name": f"{identifier}.mp3", "src": f"assets/media/audio/{identifier}.mp3"})
    entry.setdefault(
        "sentenceAudio",
        {"name": f"{identifier}-phrase.mp3", "src": f"assets/media/audio/sentences/{identifier}-phrase.mp3"},
    )
    entry["illustrationKind"] = kind
    return entry


def main() -> None:
    payload = json.loads(CATALOG.read_text(encoding="utf-8"))
    entries = payload["entries"]
    if len(entries) != len(ROWS):
        raise ValueError(f"Expected {len(ROWS)} imported words, found {len(entries)}.")
    payload["version"] = 3
    payload["entries"] = [complete_entry(entry, row) for entry, row in zip(entries, ROWS, strict=True)]
    CATALOG.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Enriched {len(entries)} complete vocabulary cards.")


if __name__ == "__main__":
    main()
