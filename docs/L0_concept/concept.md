# Concept

## Purpose

This repository exists to generate an Anki deck for English error-correction practice aimed at university entrance exam preparation. The stated goal is not memorizing English grammar itself, but improving the ability to detect incorrect English sentences (`docs/specification/L0_philosophy.md:1-6`).

## Problem

The source specification says frequently tested university-entrance-exam error patterns should be systematized and delivered as a repeatable Anki deck (`docs/specification/L0_philosophy.md:3-6`). The repository therefore treats grammar errors as structured source data rather than isolated hand-written cards.

## Target User

The confirmed target is learners preparing for university entrance exams who need repeated exposure to English error patterns (`docs/specification/L0_philosophy.md:5-6`, `README.md:1-5`).

## Design Constraints

- Cards must be generated from templates, not written directly (`docs/specification/L3_generation_pipeline.md:10-14`).
- The generation flow starts from taxonomy and templates, then proceeds to sentence generation, validation, deduplication, and CSV export (`docs/specification/L3_generation_pipeline.md:3-8`).
- The current implementation exports CSV because `scripts/build_deck.py` writes `generated.csv` with `pandas.DataFrame.to_csv` (`scripts/build_deck.py:26-28`).

## Unconfirmed

- The repository does not currently contain requirements, lock files, or runtime version declarations, so the supported Python version and exact dependency versions are unconfirmed. Add a `requirements.txt`, `pyproject.toml`, or lock file to make this determinable.
- No Anki import configuration is present, so the exact target note type, deck name, and field mapping are unconfirmed. Add an Anki export/import specification or implementation file to make this determinable.
