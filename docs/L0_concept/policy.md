# Policy

## Source Of Truth

SQLite is the implemented source of truth for vocabulary records. The schema is defined in code and applied with `init_db`, not by a migration file or ORM (`vocabdb/db.py:7-102`). Generated databases are local artifacts and are ignored by git (`.gitignore:17-30`).

## Data Modeling

Vocabulary records should remain normalized across words, meanings, examples, source wordbook metadata, audio assets, and generation review state. This is required by the current schema and importer: one imported row creates a word, a meaning, an example, a wordbook entry, and word/example audio refs (`vocabdb/db.py:10-86`, `vocabdb/importers.py:64-142`).

## Review State

Example review state must use the existing `draft`, `approved`, and `rejected` values. Both `examples.review_status` and `generation_reviews.status` enforce those values through SQLite CHECK constraints (`vocabdb/db.py:41-43`, `vocabdb/db.py:77-86`).

## Output Policy

Review JSON is generated output, not source data. The exporter writes JSON with `ensure_ascii=False` and `indent=2`, and `.gitignore` excludes `web/review/vocabulary.json` (`vocabdb/exporters.py:48-56`, `.gitignore:28-30`). The static UI should consume that generated file rather than embedding generated vocabulary data into tracked frontend files (`web/review/app.js:12-27`).

## Dependency Policy

The application code currently uses Python standard-library modules only: `sqlite3`, `csv`, `json`, `argparse`, `http.server`, `socketserver`, and `pathlib` are imported by implementation files (`vocabdb/db.py:3-4`, `vocabdb/importers.py:3-7`, `vocabdb/exporters.py:3-5`, `vocabdb/cli.py:3-7`). `pytest` is used for tests, but no dependency manifest or lock file pins versions (`pyproject.toml:1-2`, `tests/test_vocabdb.py:12-166`).

## Security And Data Rights

No network API, credential store, or remote database integration is implemented. The only server code is a local `SimpleHTTPRequestHandler` wrapper for the review directory (`vocabdb/cli.py:80-84`). Imported wordbook content should be treated as local source data with unconfirmed licensing unless a license/source-rights file is added.
