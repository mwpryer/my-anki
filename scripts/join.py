"""Concat raw/<jp>_m.mp3 + silence + raw/<jp>_f.mp3 -> audio/<jp>.mp3. One-off"""

from pathlib import Path

from pydub import AudioSegment
from utils import parse_text, sanitize

# NOTE: Edit before running
LEAF = ""
TYPE = "vocabulary"
GAP_MS = 300

leaf = Path(LEAF)
items = parse_text(leaf / f"{TYPE}.txt")
out = leaf / "audio"
out.mkdir(parents=True, exist_ok=True)
silence = AudioSegment.silent(duration=GAP_MS)

for item in items:
    stem = sanitize(item.jyutping)
    a = AudioSegment.from_mp3(str(leaf / "raw" / f"{stem}_m.mp3"))
    b = AudioSegment.from_mp3(str(leaf / "raw" / f"{stem}_f.mp3"))
    (a + silence + b).export(str(out / f"{stem}.mp3"), format="mp3")
    print(f"  -> {stem}.mp3")
