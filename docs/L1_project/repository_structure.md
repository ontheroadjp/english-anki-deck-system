# Repository Structure

## Top-Level Structure

- `vocabdb/`: Python package for the CLI, SQLite schema, import logic, validation, and JSON export. The CLI imports and dispatches functions from `db`, `importers`, `validation`, and `exporters` (`vocabdb/cli.py:9-12`, `vocabdb/cli.py:19-77`).
- `web/review/`: static browser review UI. `index.html` loads `styles.css` and `app.js`, and `app.js` fetches generated `vocabulary.json` (`web/review/index.html:7-37`, `web/review/app.js:31-48`).
- `tests/`: pytest test suite for schema creation, import, JSON export, validation, and review status handling (`tests/test_vocabdb.py:12-166`).
- `anki_csv/`: current tracked Anki TSV source data. The importer is designed for the column order represented by `ANKI_COLUMNS` (`anki_csv/target_1900_6th.txt:1-7`, `vocabdb/importers.py:12-34`).
- `docs/`: repository documentation and AI repo profile. The profile lists documentation roots and primary docs for investigation/structure (`docs/.ai/repo.profile.json:4-10`, `docs/.ai/repo.profile.json:37-40`).
- `README.md`: user-facing feature, command, and architecture summary.
- `CLAUDE.md`: AI operation entrypoint for this repository.
- `pyproject.toml`: pytest configuration only (`pyproject.toml:1-2`).

## Removed Legacy Structure

The previous grammar taxonomy/template directories and the old `scripts/build_deck.py` entrypoint are no longer present in the current working tree. The current source file list contains no `data/` or `scripts/` directory, while the implemented entrypoint is `vocabdb/__main__.py` (`vocabdb/__main__.py:1-3`).

## Monorepo Check

No `apps/`, `packages/`, or workspace manifest exists in the observed repository file list. No package manager workspace is confirmed.

## Generated Local Artifacts

`vocabulary.db` and `web/review/vocabulary.json` are generated local artifacts and are ignored by git (`.gitignore:17-30`). They may exist locally after running the CLI, but they are not source files.
