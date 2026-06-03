# English Vocabulary DB System

大学受験向け英単語データを SQLite に保存し、レビュー用 JSON とブラウザ表示を生成する語彙 DB システム。

このリポジトリは `DB layer -> logic layer -> output layer` の構造で管理する。DB 層は SQLite スキーマと接続、ロジック層は Anki TSV import・validation・review payload assembly、出力層は JSON export と静的 Web review UI を担当する。

## Features

- SQLite schema for words, meanings, examples, wordbook entries, audio assets, and AI generation review state (`vocabdb/db.py:7-87`).
- Anki TSV import for the current source data in `anki_csv/target_1900_6th.txt` (`vocabdb/importers.py:12-61`).
- Data validation for duplicate headwords, missing pronunciation, missing example translations, and missing audio refs (`vocabdb/validation.py:17-106`).
- Review JSON export with `vocabdb.review.v1` metadata and nested word data (`vocabdb/exporters.py:10-56`).
- Static browser review UI that loads `vocabulary.json`, supports text search, and filters examples by review status (`web/review/index.html:11-31`, `web/review/app.js:12-68`).

## Installation

No install command is defined. The implementation uses Python standard-library modules for the application code, and the repository currently defines only pytest path configuration in `pyproject.toml` (`pyproject.toml:1-2`).

For local testing, install `pytest` in your Python environment if it is not already available.

## Usage

Run from the repository root.

Initialize the SQLite database:

```bash
python -m vocabdb init-db --db vocabulary.db
```

Import the current Anki TSV source:

```bash
python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db
```

Validate imported vocabulary data:

```bash
python -m vocabdb validate --db vocabulary.db
```

Export review JSON for the web UI:

```bash
python -m vocabdb export-json --db vocabulary.db --output web/review/vocabulary.json
```

Serve the review UI locally:

```bash
python -m vocabdb serve-review
```

The default review server binds to `127.0.0.1:8000` and serves `web/review/` (`vocabdb/cli.py:37-40`, `vocabdb/cli.py:80-84`).

Run tests:

```bash
pytest
```

## Design Principles

- SQLite is the source of truth for normalized vocabulary data. The schema keeps words, meanings, examples, source wordbook metadata, audio refs, and generation review status separate so review and export logic can query them consistently (`vocabdb/db.py:10-86`).
- JSON review output is the v1 output surface. Generated SQLite files and review JSON are ignored because they are local artifacts (`.gitignore:17-30`).
- Imported Anki audio values are preserved as refs, not treated as public URLs. The audio schema has both `ref` and `url`, and the importer stores Anki sound fields in `ref` (`vocabdb/db.py:65-72`, `vocabdb/importers.py:141-158`).
- AI-generated example review is represented as explicit status values: `draft`, `approved`, and `rejected` (`vocabdb/db.py:41-43`, `vocabdb/db.py:77-86`).

## Architecture

1. DB layer: `vocabdb/db.py` creates SQLite tables and connection helpers.
2. Logic layer: `vocabdb/importers.py` imports Anki TSV data, and `vocabdb/validation.py` checks data quality.
3. Output layer: `vocabdb/exporters.py` writes review JSON, and `web/review/` renders that JSON in the browser.
4. CLI entrypoint: `python -m vocabdb` dispatches `init-db`, `import-anki`, `validate`, `export-json`, and `serve-review` (`vocabdb/__main__.py:1-3`, `vocabdb/cli.py:19-77`).
