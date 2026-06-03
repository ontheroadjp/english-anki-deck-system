# Specification Summary

## CLI

The implemented CLI is available through `python -m vocabdb` because `vocabdb/__main__.py` imports `main` and exits with its return code (`vocabdb/__main__.py:1-3`). `vocabdb/cli.py` defines five subcommands: `init-db`, `import-anki`, `validate`, `export-json`, and `serve-review` (`vocabdb/cli.py:19-40`).

## Database Layer

The SQLite schema is stored as a SQL string in `vocabdb/db.py` and executed by `init_db` (`vocabdb/db.py:7-87`, `vocabdb/db.py:97-102`). The connection helper enables foreign keys and returns rows as `sqlite3.Row` objects (`vocabdb/db.py:90-94`). This matters because import, validation, and export code all access columns by name.

## Import Logic

`import_anki_tsv` initializes the DB, skips Anki metadata header lines beginning with `#`, parses rows with `csv.DictReader(..., delimiter="\t")`, and inserts one normalized vocabulary record per non-empty headword row (`vocabdb/importers.py:43-61`). Each row inserts:

- a word with headword, lemma, pronunciation, part of speech, and exam level (`vocabdb/importers.py:64-78`)
- a meaning (`vocabdb/importers.py:80-86`)
- an approved imported example (`vocabdb/importers.py:88-110`)
- source wordbook metadata (`vocabdb/importers.py:112-139`)
- word and example audio refs (`vocabdb/importers.py:141-158`)

## Validation Logic

`validate_db` returns `ValidationIssue` records for duplicate normalized headwords, missing pronunciation, missing example translation, missing word audio, and missing example audio (`vocabdb/validation.py:9-17`, `vocabdb/validation.py:20-106`). The CLI prints those issues and returns a non-zero exit status when any issue exists (`vocabdb/cli.py:54-65`).

## JSON Export

`build_review_payload` queries words and adds nested `meanings`, `examples`, `wordbooks`, and `audio` arrays for each word (`vocabdb/exporters.py:10-45`, `vocabdb/exporters.py:59-113`). `export_review_json` writes that payload as UTF-8 JSON (`vocabdb/exporters.py:48-56`). The payload schema name is `vocabdb.review.v1` (`vocabdb/exporters.py:39-45`).

## Web Review UI

The static UI declares a search box, a review-status filter, and a Cards / Table tab strip in HTML, with two sibling view sections (`web/review/index.html:11-35`). JavaScript fetches `vocabulary.json`, stores words in memory, filters by text and review status, and dispatches rendering by active view (`web/review/app.js:31-89`). The card renderer outputs one card per word with meanings, examples, wordbook labels, and word audio refs (`web/review/app.js:164-208`). The table renderer outputs one row per example with twelve columns including headword, pronunciation, part of speech, exam level, meanings, example sentence, example translation, source badge, status badge, wordbook label, word audio refs, and example audio refs (`web/review/app.js:91-138`). CSS provides card, tab, and table styles plus a responsive layout that stacks header and card controls under `760px` (`web/review/styles.css:265-297`).

## Generated Artifacts

`vocabulary.db` and `web/review/vocabulary.json` are generated local artifacts and are excluded from git (`.gitignore:17-30`).

## Unconfirmed

- No API endpoints are implemented.
- No production deployment mechanism is implemented.
- No migration versioning system is implemented beyond the idempotent schema string in `vocabdb/db.py`.
