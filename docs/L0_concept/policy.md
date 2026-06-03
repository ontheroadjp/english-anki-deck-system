# Policy

## Source Of Truth

SQLite is the implemented source of truth for vocabulary records. The schema is defined in code and applied with `init_db`, not by a migration file or ORM (`backend/vocabdb/db.py:7-103`). Generated databases are local artifacts and are ignored by git (`.gitignore:17-30`).

## Data Modeling

Vocabulary records should remain normalized across words, meanings, examples, source wordbook metadata, audio assets, and generation review state. This is required by the current schema and importer: one imported row creates a word, a meaning, an example, a wordbook entry, and word/example audio refs (`backend/vocabdb/db.py:10-87`, `backend/vocabdb/importers.py:64-142`).

## Review State

Example review state must use the existing `draft`, `approved`, and `rejected` values. Both `examples.review_status` and `generation_reviews.status` enforce those values through SQLite CHECK constraints (`backend/vocabdb/db.py:43-44`, `backend/vocabdb/db.py:78-87`). Example source must use the existing `imported` and `ai_generated` values (`backend/vocabdb/db.py:41-42`).

## Output Policy

Review JSON is generated output, not source data. The exporter writes JSON with `ensure_ascii=False` and `indent=2`, and `.gitignore` excludes `frontend/review/vocabulary.json` (`backend/vocabdb/exporters.py:48-56`, `.gitignore:28-30`). The static UI should consume that generated file rather than embedding generated vocabulary data into tracked frontend files (`frontend/review/app.js:31-48`).

## Layer Separation

The repository is split into `backend/` (Python implementation, tests, source TSV) and `frontend/` (static browser assets). Cross-layer paths are expressed relative to `backend/` because the CLI runs from there (`backend/vocabdb/cli.py:15-16`, `backend/vocabdb/cli.py:38`). Documentation, AI profile, and top-level READMEs stay at the repository root.

## Dependency Policy

The application code currently uses Python standard-library modules only: `sqlite3`, `csv`, `json`, `argparse`, `http.server`, `socketserver`, and `pathlib` are imported by implementation files (`backend/vocabdb/db.py:3-4`, `backend/vocabdb/importers.py:3-7`, `backend/vocabdb/exporters.py:3-5`, `backend/vocabdb/cli.py:3-7`). `pytest` is used for tests, but no dependency manifest or lock file pins versions (`backend/pyproject.toml:1-2`, `backend/tests/test_vocabdb.py:1-8`).

## Security And Data Rights

No network API, credential store, or remote database integration is implemented. The only server code is a local `SimpleHTTPRequestHandler` wrapper for the review directory (`backend/vocabdb/cli.py:80-84`). Imported wordbook content should be treated as local source data with unconfirmed licensing unless a license/source-rights file is added.
