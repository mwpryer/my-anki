# Anki Study Tools

Per-stage Python scripts for turning textbook content (text + audio) into Anki decks.

## Setup

```sh
# Fetches the private content repo (requires access)
git clone --recurse-submodules https://github.com/mwpryer/my-anki.git
uv sync
```

## Workflow

Stages: `yale2jp` -> `split` (or `split_raw` + `rename`, or `join`) -> `check` -> `build`.

Each script is edit-and-run from the project root. See [`scripts/README.md`](scripts/README.md).
