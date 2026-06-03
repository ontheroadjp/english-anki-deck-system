# Repository Structure

## Top-Level Layout

- `backend/`: Python application code. Contains the `vocabdb` package, its tests, the imported Anki TSV source data, and Python package/test configuration. Commands are executed from this directory (`backend/vocabdb/cli.py:15-18`, `backend/vocabdb/cli.py:38-47`).
- `frontend/`: static browser assets. Currently contains only the review UI (`frontend/review/index.html:1-39`).
- `.github/workflows/`: GitHub Actions automation. `ci-cd.yml` runs backend tests and deploys the backend API on successful `main` pushes (`.github/workflows/ci-cd.yml:1-64`).
- `server/`: manually applied VPS configuration samples. `server/nginx/` contains the reverse proxy sample, and `server/systemd/` contains the `dict-english` service (`server/nginx/dict-english.conf:1-17`, `server/systemd/dict-english.service:1-16`).
- `.env.example`: commented template for the server-side `.env` loaded from `$DEPLOY_PATH/english/.env` (`.env.example:1-8`).
- `docs/`: repository documentation and the AI repo profile. The profile lists documentation roots and primary docs (`docs/.ai/repo.profile.json:4-10`, `docs/.ai/repo.profile.json:37-40`).
- `README.md`: user-facing feature, command, and architecture summary.
- `AGENTS.md`: AI agent entry-point notes.
- `CLAUDE.md`: AI operation entrypoint for this repository.

## backend/

- `backend/vocabdb/`: Python package implementing the CLI, SQLite schema, import logic, validation, JSON export, and FastAPI REST API. The CLI imports and dispatches functions from `db`, `importers`, `validation`, and `exporters`, and imports the API app factory only when serving the API (`backend/vocabdb/cli.py:9-12`, `backend/vocabdb/cli.py:20-101`). The module entry point is `backend/vocabdb/__main__.py:1-3`.
- `backend/vocabdb/api.py`: FastAPI app factory, browser CORS middleware, and API-specific SQLite serialization for `/api/health`, `/api/words`, and `/api/words/{lookup}`. The lookup path accepts either a numeric word id or a headword (`backend/vocabdb/api.py:10-147`).
- `backend/tests/`: pytest test suite. Tests import from the `vocabdb` package and use FastAPI's `TestClient` for API coverage (`backend/tests/test_vocabdb.py:5-11`, `backend/tests/test_vocabdb.py:170-244`).
- `backend/anki_csv/`: current tracked Anki TSV source data. The importer expects the column order encoded by `ANKI_COLUMNS` (`backend/vocabdb/importers.py:12-34`).
- `backend/pyproject.toml`: backend package metadata, runtime dependencies, optional test dependencies, package discovery, and pytest configuration. `pythonpath = ["."]` makes the `vocabdb` package importable when pytest runs from `backend/` (`backend/pyproject.toml:1-20`).

## frontend/

- `frontend/review/`: static review UI. `index.html` declares the search box, status filter, Cards/Table tab strip, and two sibling view sections; `app.js` fetches `/api/words` from the configured API base and dispatches rendering by active view (`frontend/review/index.html:11-35`, `frontend/review/app.js:31-92`).

## CI/CD and server/

- `.github/workflows/ci-cd.yml`: runs `pytest` from `backend/` on pull requests and `main` pushes. On successful `main` pushes, it connects to the VPS using `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, and `DEPLOY_PATH`, runs `git pull --ff-only`, installs the backend package, and restarts `dict-english` (`.github/workflows/ci-cd.yml:1-64`).
- `server/nginx/dict-english.conf`: sample nginx server block that redirects `/dict/english` to `/dict/english/` and proxies `/dict/english/` to the local backend API (`server/nginx/dict-english.conf:1-17`).
- `server/systemd/dict-english.service`: sample systemd service for the backend API. It defines `DEPLOY_PATH`, loads `$DEPLOY_PATH/english/.env`, changes into `$DEPLOY_PATH/english/backend`, and runs `python3 -m vocabdb serve-api` (`server/systemd/dict-english.service:1-16`).
- `.env.example`: sample environment values consumed by the systemd service from `$DEPLOY_PATH/english/.env` (`.env.example:1-8`).

## Default Paths Across Layers

The CLI assumes it runs from `backend/`. Defaults reflect the relative position of the `frontend/review/` directory:

- `export-json` default output: `../frontend/review/vocabulary.json` (`backend/vocabdb/cli.py:16`, `backend/vocabdb/cli.py:35`).
- `serve-review` default directory: `../frontend/review` (`backend/vocabdb/cli.py:38`).
- `serve-api` default DB path: `vocabulary.db`; default bind: `localhost:8001`. The static review UI defaults to that API base and can be pointed elsewhere with the `api` query parameter (`backend/vocabdb/cli.py:15-17`, `backend/vocabdb/cli.py:43-47`, `frontend/review/app.js:31-32`).

## Monorepo Check

There is no `apps/` or `packages/` workspace manifest. The `backend/` and `frontend/` split is a flat two-directory partition, not a managed workspace.

## Generated Local Artifacts

`backend/vocabulary.db`, `frontend/review/vocabulary.json`, and Python `*.egg-info/` metadata are generated local artifacts and are ignored by git (`.gitignore:5-30`). They may exist locally after running the CLI or editable installs, but they are not source files.
