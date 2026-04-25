"""Audit audio/<jp>.mp3 against <type>.txt. Reports missing and extra files"""

from pathlib import Path

from utils import parse_text, sanitize

# NOTE: Edit before running
LEAF = ""
TYPE = "vocabulary"

leaf = Path(LEAF)
items = parse_text(leaf / f"{TYPE}.txt")
audio_dir = leaf / "audio"
expected = {f"{sanitize(it.jyutping)}.mp3" for it in items}
actual = (
    {f.name for f in audio_dir.iterdir() if f.suffix == ".mp3"}
    if audio_dir.exists()
    else set()
)

print(f"{leaf} ({len(items)} items, {len(actual)} mp3s)")
for fn in sorted(expected - actual):
    print(f"  - {fn}")
for fn in sorted(actual - expected):
    print(f"  + {fn}")
if expected == actual:
    print("OK")
