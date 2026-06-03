# Test Strategy

## Test Runner

The repository uses pytest. The only pytest configuration currently sets `pythonpath = ["."]`, allowing tests to import the local `vocabdb` package without installing it (`pyproject.toml:1-2`).

Run:

```bash
pytest
```

## Covered Behavior

- Schema creation: `test_init_db_creates_schema` verifies core SQLite tables (`tests/test_vocabdb.py:12-31`).
- Anki TSV import and review payload shape: `test_import_anki_tsv_and_export_review_json` checks imported word fields, wordbook metadata, audio refs, and approved review status (`tests/test_vocabdb.py:34-63`).
- JSON file writing: `test_export_review_json_writes_file` verifies generated JSON contains draft review status (`tests/test_vocabdb.py:66-76`).
- Validation: `test_validate_db_reports_quality_issues` checks duplicate headwords, missing pronunciation, missing example translation, missing word audio, and missing example audio (`tests/test_vocabdb.py:79-99`).
- Review statuses: `test_json_includes_all_review_statuses` verifies `draft`, `approved`, and `rejected` appear in exported review payloads (`tests/test_vocabdb.py:102-115`).

## Unconfirmed

- Coverage thresholds are unconfirmed because no coverage configuration exists.
- CI test execution is unconfirmed because no CI workflow exists.
