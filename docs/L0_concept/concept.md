# Concept

## Product Purpose

This repository manages an English vocabulary database for university entrance exam learners. The current implemented workflow stores vocabulary data in SQLite, imports Anki TSV source data, validates the stored data, exports review JSON, and displays that JSON in a local browser review UI (`vocabdb/db.py:7-102`, `vocabdb/importers.py:43-61`, `vocabdb/validation.py:17-106`, `vocabdb/exporters.py:10-56`, `web/review/index.html:11-31`).

## Target Users

The implemented data source is an Anki export for an English wordbook deck, and the importer maps fields such as headword, pronunciation, Japanese meaning, example sentence, example translation, wordbook metadata, and audio references into the database (`anki_csv/target_1900_6th.txt:1-7`, `vocabdb/importers.py:12-34`, `vocabdb/importers.py:64-142`). The practical target user is therefore a maintainer reviewing exam-oriented vocabulary entries before downstream export or study use.

## Problem Solved

The project provides a structured review pipeline instead of treating cards as a flat CSV. The schema separates words, meanings, examples, wordbook entries, audio assets, and generation review records (`vocabdb/db.py:10-86`). This separation exists so import, validation, JSON export, and visual review can operate on normalized data rather than a single denormalized note row.

## Current Output Priority

The current output surface is review JSON plus a static web UI. The CLI exports `web/review/vocabulary.json` by default (`vocabdb/cli.py:15-16`, `vocabdb/cli.py:33-35`), and the web app fetches `vocabulary.json` and renders word cards with search and review-status filtering (`web/review/app.js:12-27`, `web/review/app.js:39-68`).

## Unconfirmed

- A production deployment target is unconfirmed because no CI, hosting configuration, or deployment files exist in the repository.
- A public license for the imported Anki TSV content is unconfirmed because no license file or source-rights metadata is present.
