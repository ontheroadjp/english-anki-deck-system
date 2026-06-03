# Project Overview

## Purpose

This repository implements a SQLite-backed English vocabulary database and local review workflow. The implemented CLI can initialize a database, import Anki TSV data, validate records, export review JSON, and serve a static browser review UI (`vocabdb/cli.py:19-77`).

## Technology Stack

- Language: Python, confirmed by the `vocabdb/*.py` package and `tests/test_vocabdb.py` (`vocabdb/cli.py:1-84`, `tests/test_vocabdb.py:1-166`).
- Database: SQLite through Python's `sqlite3` module (`vocabdb/db.py:3-4`, `vocabdb/db.py:90-102`).
- Frontend: static HTML, CSS, and JavaScript under `web/review/` (`web/review/index.html:1-33`, `web/review/app.js:1-141`, `web/review/styles.css:1-202`).
- Test runner: pytest is configured to include the repository root in Python import paths (`pyproject.toml:1-2`), and tests live in `tests/test_vocabdb.py` (`tests/test_vocabdb.py:12-166`).

## Implemented Features

- Database initialization creates tables for words, meanings, examples, wordbook entries, audio assets, and generation reviews (`vocabdb/db.py:10-86`, `vocabdb/db.py:97-102`).
- Anki TSV import reads tab-separated note rows after skipping Anki metadata headers and inserts normalized vocabulary data (`vocabdb/importers.py:43-61`, `vocabdb/importers.py:64-142`).
- Validation reports duplicate headwords, missing pronunciation, missing example translations, missing word audio, and missing example audio (`vocabdb/validation.py:17-106`).
- JSON review export returns `metadata.schema = vocabdb.review.v1`, word count, and nested word records with meanings, examples, wordbooks, and audio refs (`vocabdb/exporters.py:10-45`).
- The web review UI loads `vocabulary.json`, renders cards, supports text search, and filters by example review status (`web/review/app.js:12-68`, `web/review/app.js:71-141`).

## Commands

The CLI is exposed through `python -m vocabdb` because `vocabdb/__main__.py` delegates to `vocabdb.cli.main` (`vocabdb/__main__.py:1-3`).

- `python -m vocabdb init-db --db vocabulary.db`
- `python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db`
- `python -m vocabdb validate --db vocabulary.db`
- `python -m vocabdb export-json --db vocabulary.db --output web/review/vocabulary.json`
- `python -m vocabdb serve-review`
- `pytest`

## Unconfirmed

- CI behavior is unconfirmed because `.github/` does not exist.
- Package installation behavior is unconfirmed because no dependency manifest or lock file defines installable runtime dependencies.
