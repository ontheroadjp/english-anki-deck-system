# Project Overview

## Purpose

This repository implements a SQLite-backed English vocabulary database and local review workflow. The implemented CLI can initialize a database, import Anki TSV data, validate records, export review JSON, and serve a static browser review UI (`backend/vocabdb/cli.py:19-77`).

## Technology Stack

- Language: Python, confirmed by the `backend/vocabdb/*.py` package and `backend/tests/test_vocabdb.py` (`backend/vocabdb/cli.py:1-84`, `backend/tests/test_vocabdb.py:1-8`).
- Database: SQLite through Python's `sqlite3` module (`backend/vocabdb/db.py:3-4`, `backend/vocabdb/db.py:91-95`).
- Frontend: static HTML, CSS, and JavaScript under `frontend/review/` (`frontend/review/index.html:1-39`, `frontend/review/app.js:1-241`, `frontend/review/styles.css:1`).
- Test runner: pytest is configured to add the `backend/` directory to Python import paths (`backend/pyproject.toml:1-2`); tests live in `backend/tests/test_vocabdb.py` (`backend/tests/test_vocabdb.py:1-8`).

## Repository Split

- `backend/` holds the Python package, its tests, and the imported TSV source.
- `frontend/` holds static browser assets (currently the review UI).
- `docs/`, `README.md`, `AGENTS.md`, and `CLAUDE.md` stay at the repository root.

## Implemented Features

- Database initialization creates tables for words, meanings, examples, wordbook entries, audio assets, and generation reviews (`backend/vocabdb/db.py:10-87`, `backend/vocabdb/db.py:98-103`).
- Anki TSV import reads tab-separated note rows after skipping Anki metadata headers and inserts normalized vocabulary data (`backend/vocabdb/importers.py:43-61`, `backend/vocabdb/importers.py:64-142`).
- Validation reports duplicate headwords, missing pronunciation, missing example translations, missing word audio, and missing example audio (`backend/vocabdb/validation.py:17-106`).
- JSON review export returns `metadata.schema = vocabdb.review.v1`, word count, and nested word records with meanings, examples, wordbooks, and audio refs (`backend/vocabdb/exporters.py:10-45`).
- The web review UI loads `vocabulary.json`, supports text search, filters by example review status, and renders the data either as word cards or as a per-example table selectable via a tab strip (`frontend/review/index.html:27-35`, `frontend/review/app.js:31-138`).

## Commands

The CLI is exposed through `python -m vocabdb` because `backend/vocabdb/__main__.py` delegates to `vocabdb.cli.main` (`backend/vocabdb/__main__.py:1-3`). All commands assume the working directory is `backend/`.

- `cd backend && python -m vocabdb init-db --db vocabulary.db`
- `cd backend && python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db`
- `cd backend && python -m vocabdb validate --db vocabulary.db`
- `cd backend && python -m vocabdb export-json --db vocabulary.db` (default output: `../frontend/review/vocabulary.json`)
- `cd backend && python -m vocabdb serve-review` (default served directory: `../frontend/review`)
- `cd backend && pytest`

## Unconfirmed

- CI behavior is unconfirmed because `.github/` does not exist.
- Package installation behavior is unconfirmed because no dependency manifest or lock file defines installable runtime dependencies.
