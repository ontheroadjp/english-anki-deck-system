# Generation Pipeline

The implemented pipeline is vocabulary review generation, not grammar-card generation.

1. Initialize SQLite schema with `python -m vocabdb init-db --db vocabulary.db` (`vocabdb/cli.py:44-47`, `vocabdb/db.py:97-102`).
2. Import Anki TSV source data with `python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db` (`vocabdb/cli.py:49-52`, `vocabdb/importers.py:43-61`).
3. Validate imported records with `python -m vocabdb validate --db vocabulary.db` (`vocabdb/cli.py:54-65`, `vocabdb/validation.py:17-106`).
4. Export review JSON with `python -m vocabdb export-json --db vocabulary.db --output web/review/vocabulary.json` (`vocabdb/cli.py:67-70`, `vocabdb/exporters.py:48-56`).
5. Serve the static review UI with `python -m vocabdb serve-review` (`vocabdb/cli.py:72-74`, `vocabdb/cli.py:80-84`).

## Rule

The source-of-truth output for v1 review is generated JSON. `web/review/vocabulary.json` is ignored by git and should be regenerated from SQLite (`.gitignore:28-30`, `vocabdb/exporters.py:48-56`).
