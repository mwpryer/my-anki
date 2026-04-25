"""Bundle leaves into a .apkg. Each leaf becomes a sub-deck under TOP_DECK.

GUIDs are content-derived and deck IDs name-derived, so re-importing merges
into the existing Anki deck without duplicates. Media is prefixed with the
leaf path to avoid cross-lesson collisions
"""

import hashlib
import shutil
import tempfile
from pathlib import Path

import genanki
from utils import parse_text, sanitize

# NOTE: Edit before running
LANGUAGE = ""
TOP_DECK = ""
LEAVES = []
OUTPUT = ""

CANTO_CARD_MODEL = genanki.Model(
    1672841930,
    f"{LANGUAGE}",
    fields=[{"name": n} for n in ("Jyutping", "English", "Chinese", "Audio")],
    templates=[
        {
            "name": "Comprehension (Chinese)",
            "qfmt": '<span class="zh">{{Chinese}}</span><br>\n'
            "{{Audio}}\n[sound:_silence.mp3]",
            "afmt": '<span class="zh">{{Chinese}}</span><br><br>\n\n'
            "{{English}}<br><br>\n\n{{Jyutping}}<br>\n{{Audio}}\n[sound:_silence.mp3]",
        },
        {
            "name": "Production (Jyutping)",
            "qfmt": "{{English}}",
            "afmt": "{{English}}<br><br>\n\n"
            "{{Jyutping}}<br>\n{{Audio}}\n[sound:_silence.mp3]<br><br>\n\n"
            '<span class="zh">{{Chinese}}</span>',
        },
    ],
    css=".card { font-family: arial; font-size: 32px; text-align: center; }\n"
    ".zh { font-family: 'PingFang HK', 'Microsoft JhengHei',"
    " 'Noto Sans HK', 'MingLiU_HKSCS', SimSun, sans-serif; }\n"
    ".hover { opacity: 0; padding: 0 0.5rem; }\n"
    ".hover:hover { opacity: 1; }",
)


def deck_id(name: str) -> int:
    return int.from_bytes(hashlib.md5(name.encode()).digest()[:4], "big")


decks = []
media = []

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    for leaf_str in LEAVES:
        leaf = Path(leaf_str)
        type_ = "vocabulary" if (leaf / "vocabulary.txt").exists() else "sentences"
        items = parse_text(leaf / f"{type_}.txt")

        # Path parts: ('content', '<book>', '<unit>', '<type>', [<extras>...])
        sub = "::".join([TOP_DECK, *leaf.parts[2:]])
        prefix = "_".join(leaf.parts[1:])
        tags = list(leaf.parts[1:])

        deck = genanki.Deck(deck_id(sub), sub)
        for it in items:
            fn = f"{sanitize(it.jyutping)}.mp3"
            src = leaf / "audio" / fn
            if not src.exists():
                raise SystemExit(f"missing audio: {src}")
            dst = tmp / f"{prefix}_{fn}"
            shutil.copyfile(src, dst)
            media.append(str(dst))
            deck.add_note(
                genanki.Note(
                    model=CANTO_CARD_MODEL,
                    fields=[it.jyutping, it.english, it.chinese, f"[sound:{dst.name}]"],
                    tags=tags,
                )
            )
        decks.append(deck)
        print(f"  {sub}: {len(items)} notes")

    Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    pkg = genanki.Package(decks)
    pkg.media_files = media
    pkg.write_to_file(OUTPUT)

print(f"Wrote {sum(len(d.notes) for d in decks)} notes -> {OUTPUT}")
