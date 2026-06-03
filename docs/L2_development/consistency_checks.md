# Consistency Checks

## Schema And Import Consistency

- Confirm the schema tables still match what tests expect. `test_init_db_creates_schema` asserts the existence of `words`, `meanings`, `examples`, `wordbook_entries`, `audio_assets`, and `generation_reviews` (`backend/tests/test_vocabdb.py:11-30`), while the schema defines those same tables (`backend/vocabdb/db.py:10-87`).
- Confirm Anki import column order before changing source data. `ANKI_COLUMNS` defines the expected row shape (`backend/vocabdb/importers.py:12-34`), and the current source file lives at `backend/anki_csv/target_1900_6th.txt`.

## Export And UI Consistency

- The web UI expects a generated `vocabulary.json` file in the served directory (`frontend/review/app.js:31-48`).
- The exporter provides `metadata.schema`, `metadata.word_count`, and `words` (`backend/vocabdb/exporters.py:39-45`), which the UI uses to display the loaded count and to render either word cards or a per-example table (`frontend/review/app.js:38-41`, `frontend/review/app.js:91-138`, `frontend/review/app.js:164-208`).
- Review statuses shown by the UI should stay aligned with SQLite CHECK constraints: `draft`, `approved`, and `rejected` (`backend/vocabdb/db.py:43-44`, `frontend/review/index.html:18-23`).

## Validation Checks

Run:

```bash
cd backend && python -m vocabdb validate --db vocabulary.db
```

This verifies duplicate headwords, missing pronunciation, missing example translation, missing word audio, and missing example audio (`backend/vocabdb/validation.py:17-106`).

## Test Checks

Run:

```bash
cd backend && pytest
```

The current tests cover schema initialization, Anki TSV import, JSON export, validation issue reporting, all review statuses, and the imported vs ai-generated example distinction (`backend/tests/test_vocabdb.py:11-166`).

## Documentation Checks

When CLI commands change, update `README.md`, `docs/L2_development/operation_model.md`, and `docs/.ai/repo.profile.json` together. The command list is defined in `backend/vocabdb/cli.py:23-40`, and the module entrypoint is `backend/vocabdb/__main__.py:1-3`.

When the backend/frontend split or default paths change, also update `docs/L1_project/repository_structure.md` to keep the path map authoritative.
