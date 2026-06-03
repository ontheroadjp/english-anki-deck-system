# Project Overview

## Purpose

This repository implements a SQLite-backed English vocabulary database, local review workflow, and REST API. The implemented CLI can initialize a database, import Anki TSV data, validate records, export review JSON, serve a static browser review UI, and serve a FastAPI REST API (`backend/vocabdb/cli.py:20-86`).

## Technology Stack

- Language: Python, confirmed by the `backend/vocabdb/*.py` package and `backend/tests/test_vocabdb.py` (`backend/vocabdb/cli.py:1-84`, `backend/tests/test_vocabdb.py:1-8`).
- Database: SQLite through Python's `sqlite3` module (`backend/vocabdb/db.py:3-4`, `backend/vocabdb/db.py:91-95`).
- API framework: FastAPI with Uvicorn serving, declared in backend package metadata (`backend/pyproject.toml:1-10`, `backend/vocabdb/api.py:5-45`, `backend/vocabdb/cli.py:93-101`).
- Frontend: static HTML, CSS, and JavaScript under `frontend/review/`; the UI fetches word data from the REST API (`frontend/review/index.html:1-39`, `frontend/review/app.js:1-244`, `frontend/review/styles.css:1`).
- Test runner: pytest is configured to add the `backend/` directory to Python import paths, with pytest and httpx declared as optional test dependencies (`backend/pyproject.toml:12-20`); tests live in `backend/tests/test_vocabdb.py` (`backend/tests/test_vocabdb.py:1-296`).
- CI/CD: GitHub Actions runs backend pytest on pull requests and `main` pushes, then deploys the backend API to a VPS over SSH on successful `main` pushes (`.github/workflows/ci-cd.yml:1-64`).

## Repository Split

- `backend/` holds the Python package, its tests, and the imported TSV source.
- `frontend/` holds static browser assets (currently the review UI).
- `.github/workflows/` holds GitHub Actions automation.
- `server/` holds manually applied nginx and systemd samples for the `dict-english` backend API service.
- `docs/`, `README.md`, `AGENTS.md`, and `CLAUDE.md` stay at the repository root.

## Implemented Features

- Database initialization creates tables for words, meanings, examples, wordbook entries, audio assets, and generation reviews (`backend/vocabdb/db.py:10-87`, `backend/vocabdb/db.py:98-103`).
- Anki TSV import reads tab-separated note rows after skipping Anki metadata headers and inserts normalized vocabulary data (`backend/vocabdb/importers.py:43-61`, `backend/vocabdb/importers.py:64-142`).
- Validation reports duplicate headwords, missing pronunciation, missing example translations, missing word audio, and missing example audio (`backend/vocabdb/validation.py:17-106`).
- JSON review export returns `metadata.schema = vocabdb.review.v1`, word count, and nested word records with meanings, examples, wordbooks, and audio refs (`backend/vocabdb/exporters.py:10-45`).
- The FastAPI REST API returns health status, a word list, and individual word records from API-specific SQLite queries, and allows browser GET access for the static review UI (`backend/vocabdb/api.py:10-131`).
- The web review UI loads words from `/api/words`, supports text search, filters by example review status, and renders the data either as word cards or as a per-example table selectable via a tab strip (`frontend/review/index.html:27-35`, `frontend/review/app.js:31-141`).
- CI/CD runs backend tests and deploys the backend API service named `dict-english` to a VPS using GitHub Secrets and SSH (`.github/workflows/ci-cd.yml:1-129`, `server/systemd/dict-english.service.example:1-32`).

## Commands

The CLI is exposed through `python -m vocabdb` because `backend/vocabdb/__main__.py` delegates to `vocabdb.cli.main` (`backend/vocabdb/__main__.py:1-3`). All commands assume the working directory is `backend/`.

- `cd backend && python -m vocabdb init-db --db vocabulary.db`
- `cd backend && python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db`
- `cd backend && python -m vocabdb validate --db vocabulary.db`
- `cd backend && python -m vocabdb export-json --db vocabulary.db` (default output: `../frontend/review/vocabulary.json`)
- `cd backend && python -m vocabdb serve-review` (default served directory: `../frontend/review`)
- `cd backend && python -m vocabdb serve-api --db vocabulary.db` (default bind: `localhost:8001`)
- `cd backend && pytest`

## Unconfirmed

- GitHub repository secret values are not stored in the repository.
- VPS-side nginx and systemd installation remains a manual operation using the samples in `server/`.
