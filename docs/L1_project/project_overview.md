# Project Overview

## Purpose

English Anki Deck Generator is a system for generating a university-entrance-exam English error-correction Anki deck (`README.md:1-5`). Its documented learning objective is improving incorrect-sentence detection rather than memorizing grammar descriptions (`docs/specification/L0_philosophy.md:1-6`).

## Confirmed Technology Stack

- Language: Python is confirmed by the `.py` implementation file and Python syntax in `scripts/build_deck.py` (`scripts/build_deck.py:1-28`).
- Libraries used by implementation: `pandas` and `yaml` are imported by the generator script (`scripts/build_deck.py:1-2`).
- Data format: grammar taxonomy and templates are YAML (`data/grammar_patterns/grammar_taxonomy.yaml:1-18`, `data/templates/sample_template.yaml:1-24`).
- Output format: CSV encoded as `utf-8-sig` (`scripts/build_deck.py:26-28`).

## Confirmed Features

- Grammar taxonomy definition: categories and subpatterns are stored in `data/grammar_patterns/grammar_taxonomy.yaml` (`data/grammar_patterns/grammar_taxonomy.yaml:1-18`).
- Template-based sentence generation: the generator reads every `*.yaml` file in `data/templates` (`scripts/build_deck.py:5-9`).
- Variable expansion: the current script expands the `noun` variable from template data (`scripts/build_deck.py:11-17`).
- CSV export: generated cards are written to `generated.csv` (`scripts/build_deck.py:26-28`).

## Current Limitations

- The full card schema in the specification contains fields such as `id`, `ja_translation`, `explanation`, `error_category`, and `source_template` (`docs/specification/L2_card_schema.md:3-19`), but the current script exports only `incorrect_sentence`, `correct_sentence`, `grammar_unit`, `difficulty`, and `eiken` (`scripts/build_deck.py:18-24`).
- The generation specification includes validator and dedupe steps (`docs/specification/L3_generation_pipeline.md:3-8`), but no validator or dedupe implementation exists in the current file list.

## Unconfirmed

- Python runtime version is unconfirmed because no version file, package manifest, CI workflow, or lock file exists.
- Dependency versions are unconfirmed because no dependency manifest or lock file exists.
