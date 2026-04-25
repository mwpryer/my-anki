"""Rename audio/<PREFIX>-NNN.mp3 -> audio/<jp>.mp3. Pairs with split_raw.py"""

import re
from pathlib import Path

from utils import parse_text, sanitize

# NOTE: Edit before running
LEAF = ""
TYPE = "vocabulary"
PREFIX = "aud"
# Range (start, stop); None = all items
ITEM_RANGE = None

leaf = Path(LEAF)
items = parse_text(leaf / f"{TYPE}.txt")
if ITEM_RANGE:
    items = items[ITEM_RANGE[0] : ITEM_RANGE[1]]

audio_dir = leaf / "audio"
pat = re.compile(rf"^{re.escape(PREFIX)}-(\d+)\.mp3$")
chunks = sorted(
    (f for f in audio_dir.iterdir() if pat.match(f.name)),
    key=lambda f: int(pat.match(f.name).group(1)),
)
print(f"{len(chunks)} chunks for {len(items)} items")
if len(chunks) < len(items):
    raise SystemExit("not enough chunks")
chunks = chunks[len(chunks) - len(items) :]

for chunk, item in zip(chunks, items, strict=True):
    new = audio_dir / f"{sanitize(item.jyutping)}.mp3"
    chunk.rename(new)
    print(f"  {chunk.name} -> {new.name}")
