# Consistency Checks

## Schema And Import Consistency

- Confirm the schema tables still match what tests expect. `test_init_db_creates_schema` asserts the existence of `words`, `meanings`, `examples`, `wordbook_entries`, `audio_assets`, and `generation_reviews` (`tests/test_vocabdb.py:12-31`), while the schema defines those same tables (`vocabdb/db.py:10-86`).
- Confirm Anki import column order before changing source data. `ANKI_COLUMNS` defines the expected row shape (`vocabdb/importers.py:12-34`), and the current source file starts with Anki metadata headers followed by tab-separated note rows (`anki_csv/target_1900_6th.txt:1-7`).

## Export And UI Consistency

- The web UI expects a generated `vocabulary.json` file in the served directory (`web/review/app.js:12-27`).
- The exporter provides `metadata.schema`, `metadata.word_count`, and `words` (`vocabdb/exporters.py:39-45`), which the UI uses to display the loaded count and render word cards (`web/review/app.js:19-22`, `web/review/app.js:71-99`).
- Review statuses shown by the UI should stay aligned with SQLite CHECK constraints: `draft`, `approved`, and `rejected` (`vocabdb/db.py:41-43`, `web/review/index.html:18-23`).

## Validation Checks

Run:

```bash
python -m vocabdb validate --db vocabulary.db
```

This verifies duplicate headwords, missing pronunciation, missing example translation, missing word audio, and missing example audio (`vocabdb/validation.py:17-106`).

## Test Checks

Run:

```bash
pytest
```

The current tests cover schema initialization, Anki TSV import, JSON export, validation issue reporting, and all review statuses (`tests/test_vocabdb.py:12-166`).

## Documentation Checks

When CLI commands change, update `README.md`, `docs/L2_development/operation_model.md`, and `docs/.ai/repo.profile.json` together. The command list is defined in `vocabdb/cli.py:23-40`, and the module entrypoint is `vocabdb/__main__.py:1-3`.
