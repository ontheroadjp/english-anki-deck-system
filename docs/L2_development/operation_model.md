# Operation Model

## Local Workflow

Run commands from the repository root.

1. Initialize a SQLite database:

   ```bash
   python -m vocabdb init-db --db vocabulary.db
   ```

   This calls `init_db`, which creates parent directories as needed and executes the schema (`vocabdb/cli.py:44-47`, `vocabdb/db.py:97-102`).

2. Import the current Anki TSV source:

   ```bash
   python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db
   ```

   The importer skips lines beginning with `#`, parses tab-separated rows with the configured Anki columns, and inserts normalized records (`vocabdb/importers.py:12-61`, `vocabdb/importers.py:64-142`).

3. Validate data quality:

   ```bash
   python -m vocabdb validate --db vocabulary.db
   ```

   The command prints each validation issue and exits with status `1` when issues exist (`vocabdb/cli.py:54-65`).

4. Export review JSON:

   ```bash
   python -m vocabdb export-json --db vocabulary.db --output web/review/vocabulary.json
   ```

   The exporter writes formatted UTF-8 JSON with `ensure_ascii=False` (`vocabdb/exporters.py:48-56`).

5. Serve the review UI:

   ```bash
   python -m vocabdb serve-review
   ```

   The default host and port are `127.0.0.1` and `8000`, and the default served directory is `web/review` (`vocabdb/cli.py:37-40`, `vocabdb/cli.py:80-84`).

## Test Command

```bash
pytest
```

The test suite imports the local `vocabdb` package because `pyproject.toml` sets `pythonpath = ["."]` for pytest (`pyproject.toml:1-2`).

## Generated Files

The database and review JSON are local generated files and should not be committed (`.gitignore:17-30`).

## Unconfirmed

- CI execution is unconfirmed because no `.github/workflows/` directory exists.
- Reproducible environment setup is unconfirmed because no lock file or dependency manifest pins pytest or Python versions.
