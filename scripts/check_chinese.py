"""Audit Chinese characters against jyutping using pycantonese. Walks ROOT recursively"""

import re
from pathlib import Path

import pycantonese

from utils import parse_text

# NOTE: Edit before running
ROOT = ""

SYLLABLE = re.compile(r"[a-z]+[1-6]")


def syllables(jp: str) -> list[str]:
    return SYLLABLE.findall(jp.lower())


def expected_from_chinese(zh: str) -> list[str]:
    out: list[str] = []
    for _, jp in pycantonese.characters_to_jyutping(zh):
        if jp:
            out.extend(syllables(jp))
    return out


root = Path(ROOT)
total = 0
mismatches = 0
for txt in sorted(root.rglob("*.txt")):
    if txt.name == "dialogue.txt":
        continue
    items = parse_text(txt)
    leaf_issues: list[tuple[int, str, list[str], list[str]]] = []
    for i, item in enumerate(items, 1):
        total += 1
        got = syllables(item.jyutping)
        want = expected_from_chinese(item.chinese)
        if got != want:
            leaf_issues.append((i, item.chinese, got, want))
    if leaf_issues:
        print(f"\n{txt}")
        for i, zh, got, want in leaf_issues:
            print(f"  line {i}: {zh}")
            print(f"    txt:        {' '.join(got)}")
            print(f"    pycantonese:{' '.join(want)}")
        mismatches += len(leaf_issues)

print(f"\n{total} items checked, {mismatches} mismatches")
