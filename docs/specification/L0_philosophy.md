# Vocabulary System Philosophy

The current system is designed to make university-entrance-exam vocabulary data reviewable before downstream use. The implemented flow is SQLite storage, Anki TSV import, validation, optional JSON export, REST API serving, and browser review (`backend/vocabdb/cli.py:20-86`).

The system favors normalized source data over flat card rows. Words, meanings, examples, wordbook metadata, audio refs, and review state are separate tables (`backend/vocabdb/db.py:10-87`) so validators and exporters can reason about each concern directly.

The v1 output priority is SQLite-backed REST API data and a local web UI, not Anki CSV. The CLI can still export review JSON to `../frontend/review/vocabulary.json` when a local artifact is needed, while the UI fetches `/api/words` at runtime (`backend/vocabdb/cli.py:15-17`, `backend/vocabdb/cli.py:34-47`, `frontend/review/app.js:31-48`).
