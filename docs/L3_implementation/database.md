# Database

## Schema Definition

The SQLite schema is defined in `backend/vocabdb/db.py` as `SCHEMA` and applied by `init_db` (`backend/vocabdb/db.py:7-87`, `backend/vocabdb/db.py:98-103`). There is no separate migrations directory or migration version table.

## Tables

- `words`: stores headword, lemma, pronunciation, part of speech, EIKEN level, exam level, and creation timestamp (`backend/vocabdb/db.py:10-19`).
- `meanings`: stores Japanese meanings per word with optional usage label and priority (`backend/vocabdb/db.py:23-29`).
- `examples`: stores example sentences, translations, cloze sentence, English definition HTML, source, and review status (`backend/vocabdb/db.py:33-46`).
- `wordbook_entries`: stores source wordbook metadata including deck path, target number, rank/level, note ID, guid, and note type (`backend/vocabdb/db.py:51-62`).
- `audio_assets`: stores word/example audio refs or URLs; `asset_type` is constrained to `word` or `example` (`backend/vocabdb/db.py:66-73`).
- `generation_reviews`: stores review metadata for generated examples, including provider, prompt, status, notes, and timestamp (`backend/vocabdb/db.py:78-87`).

## Relationships

`meanings`, `examples`, `wordbook_entries`, and `audio_assets` reference `words`. `examples.meaning_id` references `meanings`, and `audio_assets.example_id` can reference `examples` (`backend/vocabdb/db.py:23-76`). Foreign keys are enabled on each connection (`backend/vocabdb/db.py:91-95`).

## Source And Status Constraints

The `examples.source` column is constrained to `imported` or `ai_generated` and defaults to `imported` (`backend/vocabdb/db.py:41-42`). Example and generation review statuses are constrained to `draft`, `approved`, or `rejected` (`backend/vocabdb/db.py:43-44`, `backend/vocabdb/db.py:82-84`). Imported examples are inserted as `imported`/`approved` because they come from the Anki TSV importer rather than from an AI draft path (`backend/vocabdb/importers.py:88-110`). AI-generated examples are inserted via `insert_ai_example`, which forces `source = 'ai_generated'` and defaults `review_status = 'draft'` (`backend/vocabdb/importers.py:145-178`).

## Initialization

Run from `backend/`:

```bash
cd backend && python -m vocabdb init-db --db vocabulary.db
```

The CLI command delegates to `init_db` (`backend/vocabdb/cli.py:44-47`).

## Unconfirmed

- Migration rollback and versioning are unconfirmed because no migration framework exists.
- Database concurrency behavior is unconfirmed because no multi-process access pattern is implemented.
