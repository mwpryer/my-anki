"""Shared bits: 3-section text parser, jyutping -> filename sanitiser, Item dataclass"""

import re
from dataclasses import dataclass
from pathlib import Path

SECTION_MARK = "##"
_PUNCT = re.compile(r'[\\/:"*?<>|？！。，、：；「」『』（）]+')


@dataclass(frozen=True)
class Item:
    jyutping: str
    english: str
    chinese: str


def parse_text(path) -> list[Item]:
    sections = [[]]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.rstrip()
        if line.strip() == SECTION_MARK:
            sections.append([])
        elif line:
            sections[-1].append(line)
    if len(sections) != 3:
        raise ValueError(f"{path}: expected 3 sections, got {len(sections)}")
    jp, en, zh = sections
    if not (len(jp) == len(en) == len(zh)):
        raise ValueError(
            f"{path}: section lengths differ ({len(jp)}/{len(en)}/{len(zh)})"
        )
    return [Item(j, e, c) for j, e, c in zip(jp, en, zh, strict=True)]


def sanitize(jyutping: str) -> str:
    """`jat1 baak3` -> `jat1_baak3`"""
    return _PUNCT.sub("", jyutping).strip().replace(" ", "_")
