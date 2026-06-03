# English Anki Deck Generator

大学受験向け英語誤文訂正Ankiデッキ生成システム。

SSOT → Generator → CSV Export の構造で管理する。

## Features

- Grammar taxonomy is stored as YAML in `data/grammar_patterns/grammar_taxonomy.yaml`.
- Sentence templates are stored as YAML in `data/templates/`.
- `scripts/build_deck.py` expands templates and exports `generated.csv`.

## Installation

No reproducible installation command is defined yet. The generator imports `pandas` and `yaml`, but this repository does not currently include `requirements.txt`, `pyproject.toml`, or a lock file.

## Usage

Run from the repository root:

```bash
python scripts/build_deck.py
```

The command reads `data/templates/*.yaml` and writes `generated.csv`.

## Design Principles

- The goal is to improve English incorrect-sentence detection, not to create a grammar memorization list.
- Cards are generated from templates; direct card generation is outside the current documented pipeline.
- Taxonomy, templates, and card schema should remain structured data so validation and deduplication can be added consistently.

## Architecture

1. Taxonomy definition
2. Grammar pattern definition
3. Template definition
4. Sentence generation
5. Validation
6. Deduplication
7. CSV export

The current implementation covers template-based sentence generation and CSV export. Validator and dedupe phases are specified but not implemented yet.
