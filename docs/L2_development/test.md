# Test Strategy

## Test Runner

The repository uses pytest. The only pytest configuration currently sets `pythonpath = ["."]`, allowing tests to import the local `vocabdb` package without installing it (`backend/pyproject.toml:1-2`). Pytest must run from the `backend/` directory so the configured `pythonpath` resolves to the directory that contains the `vocabdb` package.

Run:

```bash
cd backend && pytest
```

## Covered Behavior

- Schema creation: `test_init_db_creates_schema` verifies core SQLite tables (`backend/tests/test_vocabdb.py:11-30`).
- Anki TSV import and review payload shape: `test_import_anki_tsv_and_export_review_json` checks imported word fields, wordbook metadata, audio refs, and approved review status (`backend/tests/test_vocabdb.py:33-63`).
- JSON file writing: `test_export_review_json_writes_file` verifies generated JSON contains draft review status (`backend/tests/test_vocabdb.py:66-77`).
- Validation: `test_validate_db_reports_quality_issues` checks duplicate headwords, missing pronunciation, missing example translation, missing word audio, and missing example audio (`backend/tests/test_vocabdb.py:80-100`).
- Review statuses: `test_json_includes_all_review_statuses` verifies `draft`, `approved`, and `rejected` appear in exported review payloads (`backend/tests/test_vocabdb.py:103-116`).
- Example source distinction: `test_ai_generated_examples_are_distinct_from_imported_examples` verifies that imported and ai_generated examples coexist on one word with distinct `source` values (`backend/tests/test_vocabdb.py:119-166`).

## Unconfirmed

- Coverage thresholds are unconfirmed because no coverage configuration exists.
- CI test execution is unconfirmed because no CI workflow exists.
