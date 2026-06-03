# English Vocabulary DB System

大学受験向け英単語データを SQLite に保存し、レビュー用 JSON、ブラウザ表示、REST API を生成する語彙 DB システム。

このリポジトリは `backend/` と `frontend/` の二層構成で管理する。`backend/` は SQLite スキーマ、Anki TSV import、validation、JSON export、local review UI serving、REST API serving を担当する Python 実装と、その pytest テストおよびソース TSV を含む。`frontend/` は静的レビュー UI を含む。`docs/` と `README.md` などのドキュメント類はルートに置く。

## Features

- SQLite schema for words, meanings, examples, wordbook entries, audio assets, and AI generation review state (`backend/vocabdb/db.py:7-87`).
- Anki TSV import for the current source data in `backend/anki_csv/target_1900_6th.txt` (`backend/vocabdb/importers.py:12-61`).
- Data validation for duplicate headwords, missing pronunciation, missing example translations, and missing audio refs (`backend/vocabdb/validation.py:17-106`).
- Review JSON export with `vocabdb.review.v1` metadata and nested word data (`backend/vocabdb/exporters.py:10-56`).
- FastAPI REST API with `/api/health`, `/api/words`, and `/api/words/{word_id}` endpoints backed by API-specific SQLite queries (`backend/vocabdb/api.py:10-124`).
- Static browser review UI that loads words from the REST API, supports text search, filters examples by review status, and offers card and table views selectable via a tab strip (`frontend/review/index.html:11-35`, `frontend/review/app.js:31-141`).

## Installation

The backend defines package metadata and runtime dependencies in `backend/pyproject.toml`: FastAPI and Uvicorn for the REST API, plus optional test dependencies for httpx and pytest (`backend/pyproject.toml:1-17`).

Install the backend with test dependencies from the `backend/` directory:

```bash
cd backend && python -m pip install -e '.[test]'
```

## Usage

Run all backend commands from the `backend/` directory. The default output paths point at `../frontend/review/`.

Initialize the SQLite database:

```bash
cd backend && python -m vocabdb init-db --db vocabulary.db
```

Import the current Anki TSV source:

```bash
cd backend && python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db
```

Validate imported vocabulary data:

```bash
cd backend && python -m vocabdb validate --db vocabulary.db
```

Export review JSON as a local artifact (defaults to `../frontend/review/vocabulary.json`):

```bash
cd backend && python -m vocabdb export-json --db vocabulary.db
```

Serve the REST API locally:

```bash
cd backend && python -m vocabdb serve-api --db vocabulary.db
```

The default API server binds to `localhost:8001` and exposes `/api/health`, `/api/words`, and `/api/words/{word_id}` (`backend/vocabdb/cli.py:17`, `backend/vocabdb/cli.py:43-47`, `backend/vocabdb/api.py:14-52`).

Serve the review UI locally in a second terminal (defaults to serving `../frontend/review`):

```bash
cd backend && python -m vocabdb serve-review
```

The default review server serves `../frontend/review/`, and the UI fetches API data from `http://localhost:8001/api/words` by default. Add `?api=<base-url>` to the review UI URL to point at a different API base (`backend/vocabdb/cli.py:37-40`, `backend/vocabdb/cli.py:80-84`, `frontend/review/app.js:31-32`).

Run tests:

```bash
cd backend && pytest
```

## Design Principles

- SQLite is the source of truth for normalized vocabulary data. The schema keeps words, meanings, examples, source wordbook metadata, audio refs, and generation review status separate so review and export logic can query them consistently (`backend/vocabdb/db.py:10-87`).
- JSON review output is the v1 output surface. Generated SQLite files and review JSON are ignored because they are local artifacts (`.gitignore:17-30`).
- The REST API is a separate serving surface from the review JSON exporter and uses API-specific SQLite queries (`backend/vocabdb/api.py:10-124`).
- Imported Anki audio values are preserved as refs, not treated as public URLs. The audio schema has both `ref` and `url`, and the importer stores Anki sound fields in `ref` (`backend/vocabdb/db.py:66-73`, `backend/vocabdb/importers.py:141-142`, `backend/vocabdb/importers.py:181-194`).
- AI-generated example review is represented as explicit status values: `draft`, `approved`, and `rejected` (`backend/vocabdb/db.py:43-44`, `backend/vocabdb/db.py:78-87`).

## Architecture

1. Backend (`backend/`):
   - DB layer: `backend/vocabdb/db.py` creates SQLite tables and connection helpers.
   - Logic layer: `backend/vocabdb/importers.py` imports Anki TSV data, and `backend/vocabdb/validation.py` checks data quality.
   - Output layer: `backend/vocabdb/exporters.py` writes review JSON.
   - API layer: `backend/vocabdb/api.py` creates the FastAPI app and serializes SQLite records for REST responses.
   - CLI entrypoint: `python -m vocabdb` dispatches `init-db`, `import-anki`, `validate`, `export-json`, `serve-review`, and `serve-api` (`backend/vocabdb/__main__.py:1-3`, `backend/vocabdb/cli.py:20-86`).
2. Frontend (`frontend/`):
   - `frontend/review/` renders REST API word data in the browser (`frontend/review/index.html:1-39`, `frontend/review/app.js:31-141`).
3. Tests: `backend/tests/test_vocabdb.py` (`backend/tests/test_vocabdb.py:1-296`).
