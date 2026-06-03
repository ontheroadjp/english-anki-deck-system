# Specification Summary

## CLI

The implemented CLI is available through `python -m vocabdb` because `backend/vocabdb/__main__.py` imports `main` and raises `SystemExit` with its return code (`backend/vocabdb/__main__.py:1-3`). `backend/vocabdb/cli.py` defines five subcommands: `init-db`, `import-anki`, `validate`, `export-json`, and `serve-review` (`backend/vocabdb/cli.py:19-40`). All commands assume the working directory is `backend/`; defaults for `--output` and `--directory` use `../frontend/review` (`backend/vocabdb/cli.py:15-16`, `backend/vocabdb/cli.py:38`).

## Database Layer

The SQLite schema is stored as a SQL string in `backend/vocabdb/db.py` and executed by `init_db` (`backend/vocabdb/db.py:7-87`, `backend/vocabdb/db.py:98-103`). The connection helper enables foreign keys and returns rows as `sqlite3.Row` objects (`backend/vocabdb/db.py:91-95`). This matters because import, validation, and export code all access columns by name.

## Import Logic

`import_anki_tsv` initializes the DB, skips Anki metadata header lines beginning with `#`, parses rows with `csv.DictReader(..., delimiter="\t")`, and inserts one normalized vocabulary record per non-empty headword row (`backend/vocabdb/importers.py:43-61`). Each row inserts:

- a word with headword, lemma, pronunciation, part of speech, and exam level (`backend/vocabdb/importers.py:64-78`)
- a meaning (`backend/vocabdb/importers.py:80-86`)
- an imported example with `source = 'imported'` and `review_status = 'approved'` (`backend/vocabdb/importers.py:88-110`)
- source wordbook metadata (`backend/vocabdb/importers.py:112-139`)
- word and example audio refs (`backend/vocabdb/importers.py:141-142`, `backend/vocabdb/importers.py:181-194`)

`insert_ai_example` provides the AI-generated path. It forces `source = 'ai_generated'` and defaults `review_status = 'draft'` (`backend/vocabdb/importers.py:145-178`).

## Validation Logic

`validate_db` returns `ValidationIssue` records for duplicate normalized headwords, missing pronunciation, missing example translation, missing word audio, and missing example audio (`backend/vocabdb/validation.py:9-17`, `backend/vocabdb/validation.py:20-106`). The CLI prints those issues and returns a non-zero exit status when any issue exists (`backend/vocabdb/cli.py:54-65`).

## JSON Export

`build_review_payload` queries words and adds nested `meanings`, `examples`, `wordbooks`, and `audio` arrays for each word (`backend/vocabdb/exporters.py:10-45`, `backend/vocabdb/exporters.py:59-113`). `export_review_json` writes that payload as UTF-8 JSON (`backend/vocabdb/exporters.py:48-56`). The payload schema name is `vocabdb.review.v1` (`backend/vocabdb/exporters.py:39-45`). Audio is exposed at word level, split into `audio.word` and `audio.examples`, with each example audio entry carrying `example_id` so the UI can join by example (`backend/vocabdb/exporters.py:100-113`).

## Web Review UI

The static UI declares a search box, a review-status filter, and a Cards / Table tab strip in HTML, with two sibling view sections (`frontend/review/index.html:11-35`). JavaScript fetches `vocabulary.json`, stores words in memory, filters by text and review status, and dispatches rendering by active view (`frontend/review/app.js:31-89`). The card renderer outputs one card per word with meanings, examples, wordbook labels, and word audio refs (`frontend/review/app.js:164-208`). The table renderer outputs one row per example with twelve columns including headword, pronunciation, part of speech, exam level, meanings, example sentence, example translation, source badge, status badge, wordbook label, word audio refs, and example audio refs (`frontend/review/app.js:91-138`). Example audio in the table view is joined from `word.audio.examples` by `example_id` (`frontend/review/app.js:117-121`).

## Generated Artifacts

`backend/vocabulary.db` and `frontend/review/vocabulary.json` are generated local artifacts and are excluded from git (`.gitignore:17-30`).

## Unconfirmed

- No API endpoints are implemented.
- No production deployment mechanism is implemented.
- No migration versioning system is implemented beyond the idempotent schema string in `backend/vocabdb/db.py`.
