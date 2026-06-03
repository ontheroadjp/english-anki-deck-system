# Operation Model

## Local Workflow

All CLI invocations assume the working directory is `backend/`. The defaults for `--output` and `--directory` are relative to `backend/` (`backend/vocabdb/cli.py:15-16`, `backend/vocabdb/cli.py:38`).

1. Initialize a SQLite database:

   ```bash
   cd backend && python -m vocabdb init-db --db vocabulary.db
   ```

   This calls `init_db`, which creates parent directories as needed and executes the schema (`backend/vocabdb/cli.py:44-47`, `backend/vocabdb/db.py:98-103`).

2. Import the current Anki TSV source:

   ```bash
   cd backend && python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db
   ```

   The importer skips lines beginning with `#`, parses tab-separated rows with the configured Anki columns, and inserts normalized records (`backend/vocabdb/importers.py:12-61`, `backend/vocabdb/importers.py:64-142`).

3. Validate data quality:

   ```bash
   cd backend && python -m vocabdb validate --db vocabulary.db
   ```

   The command prints each validation issue and exits with status `1` when issues exist (`backend/vocabdb/cli.py:54-65`).

4. Export review JSON:

   ```bash
   cd backend && python -m vocabdb export-json --db vocabulary.db
   ```

   The default output path is `../frontend/review/vocabulary.json` (`backend/vocabdb/cli.py:16`, `backend/vocabdb/cli.py:35`). The exporter writes formatted UTF-8 JSON with `ensure_ascii=False` (`backend/vocabdb/exporters.py:48-56`).

5. Serve the review UI:

   ```bash
   cd backend && python -m vocabdb serve-review
   ```

   The default host and port are `127.0.0.1` and `8000`, and the default served directory is `../frontend/review` (`backend/vocabdb/cli.py:37-40`, `backend/vocabdb/cli.py:80-84`).

## Test Command

```bash
cd backend && pytest
```

The test suite imports the local `vocabdb` package because `backend/pyproject.toml` sets `pythonpath = ["."]` for pytest (`backend/pyproject.toml:1-2`).

## Generated Files

The database and review JSON are local generated files and should not be committed (`.gitignore:17-30`).

## Unconfirmed

- CI execution is unconfirmed because no `.github/workflows/` directory exists.
- Reproducible environment setup is unconfirmed because no lock file or dependency manifest pins pytest or Python versions.
