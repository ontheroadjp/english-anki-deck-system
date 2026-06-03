# Vocabulary System Philosophy

The current system is designed to make university-entrance-exam vocabulary data reviewable before downstream use. The implemented flow is SQLite storage, Anki TSV import, validation, JSON export, and browser review (`vocabdb/cli.py:19-77`).

The system favors normalized source data over flat card rows. Words, meanings, examples, wordbook metadata, audio refs, and review state are separate tables (`vocabdb/db.py:10-86`) so validators and exporters can reason about each concern directly.

The v1 output priority is review JSON and a local web UI, not Anki CSV. The CLI default JSON target is `web/review/vocabulary.json`, and the UI fetches that file at runtime (`vocabdb/cli.py:15-16`, `web/review/app.js:12-27`).
