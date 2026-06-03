# Database

## Schema Definition

The SQLite schema is defined in `vocabdb/db.py` as `SCHEMA` and applied by `init_db` (`vocabdb/db.py:7-87`, `vocabdb/db.py:97-102`). There is no separate migrations directory or migration version table.

## Tables

- `words`: stores headword, lemma, pronunciation, part of speech, EIKEN level, exam level, and creation timestamp (`vocabdb/db.py:10-19`).
- `meanings`: stores Japanese meanings per word with optional usage label and priority (`vocabdb/db.py:23-29`).
- `examples`: stores example sentences, translations, cloze sentence, English definition HTML, source, and review status (`vocabdb/db.py:33-45`).
- `wordbook_entries`: stores source wordbook metadata including deck path, target number, rank/level, note ID, guid, and note type (`vocabdb/db.py:50-61`).
- `audio_assets`: stores word/example audio refs or URLs; `asset_type` is constrained to `word` or `example` (`vocabdb/db.py:65-72`).
- `generation_reviews`: stores review metadata for generated examples, including provider, prompt, status, notes, and timestamp (`vocabdb/db.py:77-86`).

## Relationships

`meanings`, `examples`, `wordbook_entries`, and `audio_assets` reference `words`. `examples.meaning_id` references `meanings`, and `audio_assets.example_id` can reference `examples` (`vocabdb/db.py:23-75`). Foreign keys are enabled on each connection (`vocabdb/db.py:90-94`).

## Status Constraints

Example and generation review statuses are constrained to `draft`, `approved`, or `rejected` (`vocabdb/db.py:41-43`, `vocabdb/db.py:81-83`). Imported examples are inserted as `approved` because they come from the Anki TSV importer rather than from an AI draft path (`vocabdb/importers.py:88-110`).

## Initialization

Run:

```bash
python -m vocabdb init-db --db vocabulary.db
```

The CLI command delegates to `init_db` (`vocabdb/cli.py:44-47`).

## Unconfirmed

- Migration rollback and versioning are unconfirmed because no migration framework exists.
- Database concurrency behavior is unconfirmed because no multi-process access pattern is implemented.
