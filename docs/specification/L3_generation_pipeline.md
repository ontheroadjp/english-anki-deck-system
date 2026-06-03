# Generation Pipeline

The implemented pipeline is vocabulary review generation, not grammar-card generation. All steps run from the `backend/` directory.

1. Initialize SQLite schema with `cd backend && python -m vocabdb init-db --db vocabulary.db` (`backend/vocabdb/cli.py:44-47`, `backend/vocabdb/db.py:98-103`).
2. Import Anki TSV source data with `cd backend && python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db` (`backend/vocabdb/cli.py:49-52`, `backend/vocabdb/importers.py:43-61`).
3. Validate imported records with `cd backend && python -m vocabdb validate --db vocabulary.db` (`backend/vocabdb/cli.py:54-65`, `backend/vocabdb/validation.py:17-106`).
4. Export review JSON with `cd backend && python -m vocabdb export-json --db vocabulary.db` (default output `../frontend/review/vocabulary.json`) (`backend/vocabdb/cli.py:67-70`, `backend/vocabdb/exporters.py:48-56`).
5. Serve the static review UI with `cd backend && python -m vocabdb serve-review` (default served directory `../frontend/review`) (`backend/vocabdb/cli.py:72-74`, `backend/vocabdb/cli.py:80-84`).

## Rule

The source-of-truth output for v1 review is generated JSON. `frontend/review/vocabulary.json` is ignored by git and should be regenerated from SQLite (`.gitignore:28-30`, `backend/vocabdb/exporters.py:48-56`).
