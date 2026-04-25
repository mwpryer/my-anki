# Stage scripts

Edit-and-run. Open the file, set the variables at the top, run from the project root.

```sh
uv run python scripts/<stage>.py
```

| Script | Stage |
| --- | --- |
| `yale2jp.py` | `<type>.yale.txt` -> `<type>.txt` (jyutping from Chinese chars via pycantonese) |
| `split.py` | `source.mp3` + `<type>.txt` -> `audio/<jp>.mp3` (vocab-aware silence split) |
| `split_raw.py` | `source.mp3` -> `audio/aud-NNN.mp3` (bare silence split, fallback) |
| `rename.py` | `audio/aud-NNN.mp3` + `<type>.txt` -> `audio/<jp>.mp3` |
| `join.py` | `raw/<jp>_{m,f}.mp3` -> `audio/<jp>.mp3` (concat male + female, rare) |
| `check.py` | Audit `audio/` against `<type>.txt` |
| `check_chinese.py` | Audit `<type>.txt` jyutping against the Chinese chars |
| `build.py` | Bundle `LEAVES` into `decks/<name>.apkg` |
| `utils.py` | Shared: `parse_text`, `sanitize`, `Item` |

A "leaf" is a directory with `<type>.txt` (and/or `<type>.yale.txt`) for `<type>` in `vocabulary | sentences`.

## Flow per leaf

`yale2jp` (if yale source) -> `split` (or `split_raw` + `rename`) -> `check` -> `build`

Lessons with multiple source tracks: run `split.py` once per source with the appropriate `SOURCE` and `ITEM_RANGE`.

For paired m/f recordings (raw/<jp>_m.mp3 + _f.mp3) when you want only the male recording in the deck:

```sh
for f in <leaf>/raw/*_m.mp3; do
  cp "$f" "$(dirname "$f")/../audio/$(basename "${f%_m.mp3}").mp3"
done
```

Use `join.py` instead if you want both voices on one card.
