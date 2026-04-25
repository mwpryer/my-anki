"""Derive <type>.txt from <type>.yale.txt by running pycantonese on the Chinese chars"""

import re
from pathlib import Path

import pycantonese

from utils import SECTION_MARK, parse_text

# NOTE: Edit before running
LEAF = ""
# Or "sentences"
TYPE = "vocabulary"

KEEP = set("？！。，、：；「」『』（）?!.,")
SYLLABLE = re.compile(r"[a-z]+[1-6]")


def to_jyutping(zh: str) -> str:
    out = []
    for chars, jp in pycantonese.characters_to_jyutping(zh):
        if jp:
            out.extend(SYLLABLE.findall(jp))
        else:
            # V4 segments first; unmapped chunks may be multi-char
            # Flag non-punct chars for manual review
            out.extend(c if c in KEEP else f"[{c}]" for c in chars)
    return " ".join(out)


leaf = Path(LEAF)
items = parse_text(leaf / f"{TYPE}.yale.txt")
jp_lines = [to_jyutping(it.chinese) for it in items]

dst = leaf / f"{TYPE}.txt"
dst.write_text(
    "\n".join(jp_lines)
    + f"\n{SECTION_MARK}\n"
    + "\n".join(it.english for it in items)
    + f"\n{SECTION_MARK}\n"
    + "\n".join(it.chinese for it in items)
    + "\n",
    encoding="utf-8",
)

for i, (it, jp) in enumerate(zip(items, jp_lines, strict=True), 1):
    print(f"{i:3}. {it.chinese} -> {jp}")
print(f"Wrote {len(items)} items to {dst}")
