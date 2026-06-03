# Repository Structure

## Top-Level Layout

- `backend/`: Python application code. Contains the `vocabdb` package, its tests, the imported Anki TSV source data, and the pytest configuration. Commands are executed from this directory (`backend/vocabdb/cli.py:15-16`, `backend/vocabdb/cli.py:38`).
- `frontend/`: static browser assets. Currently contains only the review UI (`frontend/review/index.html:1-39`).
- `docs/`: repository documentation and the AI repo profile. The profile lists documentation roots and primary docs (`docs/.ai/repo.profile.json:4-10`, `docs/.ai/repo.profile.json:37-40`).
- `README.md`: user-facing feature, command, and architecture summary.
- `AGENTS.md`: AI agent entry-point notes.
- `CLAUDE.md`: AI operation entrypoint for this repository.

## backend/

- `backend/vocabdb/`: Python package implementing the CLI, SQLite schema, import logic, validation, and JSON export. The CLI imports and dispatches functions from `db`, `importers`, `validation`, and `exporters` (`backend/vocabdb/cli.py:9-12`, `backend/vocabdb/cli.py:19-77`). The module entry point is `backend/vocabdb/__main__.py:1-3`.
- `backend/tests/`: pytest test suite. All tests import from the `vocabdb` package (`backend/tests/test_vocabdb.py:5-8`).
- `backend/anki_csv/`: current tracked Anki TSV source data. The importer expects the column order encoded by `ANKI_COLUMNS` (`backend/vocabdb/importers.py:12-34`).
- `backend/pyproject.toml`: pytest configuration only. `pythonpath = ["."]` makes the `vocabdb` package importable when pytest runs from `backend/` (`backend/pyproject.toml:1-2`).

## frontend/

- `frontend/review/`: static review UI. `index.html` declares the search box, status filter, Cards/Table tab strip, and two sibling view sections; `app.js` fetches `vocabulary.json` and dispatches rendering by active view (`frontend/review/index.html:11-35`, `frontend/review/app.js:31-89`).

## Default Paths Across Layers

The CLI assumes it runs from `backend/`. Defaults reflect the relative position of the `frontend/review/` directory:

- `export-json` default output: `../frontend/review/vocabulary.json` (`backend/vocabdb/cli.py:16`, `backend/vocabdb/cli.py:35`).
- `serve-review` default directory: `../frontend/review` (`backend/vocabdb/cli.py:38`).

## Monorepo Check

There is no `apps/` or `packages/` workspace manifest. The `backend/` and `frontend/` split is a flat two-directory partition, not a managed workspace.

## Generated Local Artifacts

`backend/vocabulary.db` and `frontend/review/vocabulary.json` are generated local artifacts and are ignored by git (`.gitignore:17-30`). They may exist locally after running the CLI, but they are not source files.
