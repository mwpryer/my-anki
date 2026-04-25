"""Bare silence split: <SOURCE>.mp3 -> audio/<PREFIX>-NNN.mp3. Pair with rename.py"""

from pathlib import Path

from pydub import AudioSegment
from pydub.silence import split_on_silence

# NOTE: Edit before running
LEAF = ""
SOURCE = "source.mp3"
PREFIX = "aud"

MIN_SILENCE_LEN = 700
SILENCE_THRESH = -40
KEEP_SILENCE = 500

leaf = Path(LEAF)
out = leaf / "audio"
out.mkdir(parents=True, exist_ok=True)

audio = AudioSegment.from_mp3(str(leaf / SOURCE))
chunks = split_on_silence(
    audio, MIN_SILENCE_LEN, SILENCE_THRESH, keep_silence=KEEP_SILENCE
)
for i, chunk in enumerate(chunks, 1):
    chunk.export(str(out / f"{PREFIX}-{i:03d}.mp3"), format="mp3")
print(f"Wrote {len(chunks)} chunks to {out}")
