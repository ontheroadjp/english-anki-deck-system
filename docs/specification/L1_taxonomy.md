# Vocabulary Taxonomy

## Implemented Classification Fields

The current implementation does not include a standalone taxonomy file. Classification is stored as fields on imported records:

- `part_of_speech` on `words` (`backend/vocabdb/db.py:10-19`)
- `eiken` on `words` (`backend/vocabdb/db.py:10-19`)
- `exam_level` on `words` (`backend/vocabdb/db.py:10-19`)
- `rank_or_level`, `target_number`, and wordbook metadata on `wordbook_entries` (`backend/vocabdb/db.py:51-62`)

## Source Mapping

The Anki TSV importer maps source columns to these fields. `word_rank_or_level` is inserted as `exam_level` on `words` and `rank_or_level` on `wordbook_entries`; `part_of_speech` is inserted on `words`; target number and deck metadata are inserted into `wordbook_entries` (`backend/vocabdb/importers.py:64-78`, `backend/vocabdb/importers.py:112-139`).

## Unconfirmed

- A canonical EIKEN mapping is unconfirmed because the current importer does not populate `eiken`.
- A separate vocabulary taxonomy source file is unconfirmed because no such file exists in the current repository structure.
