# Vocabulary System Philosophy

The current system is designed to make university-entrance-exam vocabulary data reviewable before downstream use. The implemented flow is SQLite storage, Anki TSV import, validation, JSON export, and browser review (`backend/vocabdb/cli.py:19-77`).

The system favors normalized source data over flat card rows. Words, meanings, examples, wordbook metadata, audio refs, and review state are separate tables (`backend/vocabdb/db.py:10-87`) so validators and exporters can reason about each concern directly.

The v1 output priority is review JSON and a local web UI, not Anki CSV. The CLI default JSON target is `../frontend/review/vocabulary.json` (relative to `backend/`), and the UI fetches that file at runtime (`backend/vocabdb/cli.py:15-16`, `frontend/review/app.js:31-48`).
