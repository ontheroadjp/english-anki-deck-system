# Review JSON Schema

The current v1 output schema is review JSON, not Anki CSV. `build_review_payload` returns a top-level object with `metadata` and `words` (`backend/vocabdb/exporters.py:39-45`).

## Top-Level Fields

| field | source |
|---|---|
| `metadata.schema` | fixed value `vocabdb.review.v1` (`backend/vocabdb/exporters.py:39-45`) |
| `metadata.word_count` | number of exported word objects (`backend/vocabdb/exporters.py:39-45`) |
| `words` | list of exported word records (`backend/vocabdb/exporters.py:20-45`) |

## Word Fields

Each word record includes:

- `id`, `headword`, `lemma`, `pronunciation`, `part_of_speech`, `eiken`, and `exam_level` from `words` (`backend/vocabdb/exporters.py:12-31`)
- `meanings` from `meanings` (`backend/vocabdb/exporters.py:59-69`)
- `examples` from `examples` (including `source` and `review_status`) (`backend/vocabdb/exporters.py:72-83`)
- `wordbooks` from `wordbook_entries` (`backend/vocabdb/exporters.py:86-97`)
- `audio.word` and `audio.examples` from `audio_assets`; example audio entries carry `example_id` for client-side join (`backend/vocabdb/exporters.py:100-113`)

## Example Source

Example `source` values are `imported` or `ai_generated` by database constraint (`backend/vocabdb/db.py:41-42`).

## Review Status

Example review status values are `draft`, `approved`, and `rejected` by database constraint (`backend/vocabdb/db.py:43-44`). The UI exposes these same statuses in the filter control (`frontend/review/index.html:18-23`).
