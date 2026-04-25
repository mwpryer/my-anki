"""Vocab-aware silence split: <SOURCE>.mp3 -> audio/<jp>.mp3.

Drops leading chunks when split produces more chunks than items (intro narration).
For lessons with multiple source files, set ITEM_RANGE and run once per source
"""

from pathlib import Path

from pydub import AudioSegment
from pydub.silence import split_on_silence
from utils import parse_text, sanitize

# NOTE: Edit before running
LEAF = ""
TYPE = "vocabulary"
SOURCE = "source.mp3"
# Range (start, stop) for partial splits e.g. (0, 17); None = all items
ITEM_RANGE = None

MIN_SILENCE_LEN = 1200
SILENCE_THRESH = -40
KEEP_SILENCE = 500

leaf = Path(LEAF)
items = parse_text(leaf / f"{TYPE}.txt")
if ITEM_RANGE:
    items = items[ITEM_RANGE[0] : ITEM_RANGE[1]]

audio = AudioSegment.from_mp3(str(leaf / SOURCE))
chunks = split_on_silence(
    audio, MIN_SILENCE_LEN, SILENCE_THRESH, keep_silence=KEEP_SILENCE
)
print(f"{SOURCE}: {len(chunks)} chunks for {len(items)} items")
if len(chunks) < len(items):
    raise SystemExit("not enough chunks — adjust silence knobs")
chunks = chunks[len(chunks) - len(items) :]

out = leaf / "audio"
out.mkdir(parents=True, exist_ok=True)
for chunk, item in zip(chunks, items, strict=True):
    path = out / f"{sanitize(item.jyutping)}.mp3"
    chunk.export(str(path), format="mp3")
    print(f"  -> {path.name}")
