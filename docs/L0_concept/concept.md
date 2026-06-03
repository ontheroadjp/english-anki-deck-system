# Concept

## Product Purpose

This repository manages an English vocabulary database for university entrance exam learners. The current implemented workflow stores vocabulary data in SQLite, imports Anki TSV source data, validates the stored data, exports review JSON, and displays that JSON in a local browser review UI (`backend/vocabdb/db.py:7-103`, `backend/vocabdb/importers.py:43-61`, `backend/vocabdb/validation.py:17-106`, `backend/vocabdb/exporters.py:10-56`, `frontend/review/index.html:11-35`).

## Target Users

The implemented data source is an Anki export for an English wordbook deck, and the importer maps fields such as headword, pronunciation, Japanese meaning, example sentence, example translation, wordbook metadata, and audio references into the database (`backend/anki_csv/target_1900_6th.txt`, `backend/vocabdb/importers.py:12-34`, `backend/vocabdb/importers.py:64-142`). The practical target user is therefore a maintainer reviewing exam-oriented vocabulary entries before downstream export or study use.

## Problem Solved

The project provides a structured review pipeline instead of treating cards as a flat CSV. The schema separates words, meanings, examples, wordbook entries, audio assets, and generation review records (`backend/vocabdb/db.py:10-87`). This separation exists so import, validation, JSON export, and visual review can operate on normalized data rather than a single denormalized note row.

## Current Output Priority

The current output surface is review JSON plus a static web UI. The CLI exports to `../frontend/review/vocabulary.json` by default when run from `backend/` (`backend/vocabdb/cli.py:15-16`, `backend/vocabdb/cli.py:33-35`), and the web app fetches `vocabulary.json` and renders word cards or a per-example table with search and review-status filtering (`frontend/review/app.js:31-89`, `frontend/review/app.js:91-138`).

## Unconfirmed

- A production deployment target is unconfirmed because no CI, hosting configuration, or deployment files exist in the repository.
- A public license for the imported Anki TSV content is unconfirmed because no license file or source-rights metadata is present.
