# Generation Pipeline

The implemented pipeline is vocabulary review generation, not grammar-card generation. All steps run from the `backend/` directory.

1. Initialize SQLite schema with `cd backend && python -m vocabdb init-db --db vocabulary.db` (`backend/vocabdb/cli.py:44-47`, `backend/vocabdb/db.py:98-103`).
2. Import Anki TSV source data with `cd backend && python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db` (`backend/vocabdb/cli.py:49-52`, `backend/vocabdb/importers.py:43-61`).
3. Validate imported records with `cd backend && python -m vocabdb validate --db vocabulary.db` (`backend/vocabdb/cli.py:54-65`, `backend/vocabdb/validation.py:17-106`).
4. Export review JSON with `cd backend && python -m vocabdb export-json --db vocabulary.db` when a local JSON artifact is needed (default output `../frontend/review/vocabulary.json`) (`backend/vocabdb/cli.py:67-70`, `backend/vocabdb/exporters.py:48-56`).
5. Serve the REST API with `cd backend && python -m vocabdb serve-api --db vocabulary.db` (default API base `http://localhost:8001`) (`backend/vocabdb/cli.py:76-79`, `backend/vocabdb/api.py:21-52`).
6. Serve the static review UI with `cd backend && python -m vocabdb serve-review` (default served directory `../frontend/review`) (`backend/vocabdb/cli.py:72-74`, `backend/vocabdb/cli.py:80-84`).

## Rule

SQLite is the source of truth for v1 review data. The review UI reads SQLite-backed data through the REST API, while `frontend/review/vocabulary.json` remains an ignored local export artifact that can be regenerated when needed (`frontend/review/app.js:31-48`, `.gitignore:28-30`, `backend/vocabdb/exporters.py:48-56`).
