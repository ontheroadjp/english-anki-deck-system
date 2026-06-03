# Operation Model

## Local Workflow

All CLI invocations assume the working directory is `backend/`. The defaults for `--output` and `--directory` are relative to `backend/` (`backend/vocabdb/cli.py:15-16`, `backend/vocabdb/cli.py:38`).

1. Initialize a SQLite database:

   ```bash
   cd backend && python -m vocabdb init-db --db vocabulary.db
   ```

   This calls `init_db`, which creates parent directories as needed and executes the schema (`backend/vocabdb/cli.py:44-47`, `backend/vocabdb/db.py:98-103`).

2. Import the current Anki TSV source:

   ```bash
   cd backend && python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db
   ```

   The importer skips lines beginning with `#`, parses tab-separated rows with the configured Anki columns, and inserts normalized records (`backend/vocabdb/importers.py:12-61`, `backend/vocabdb/importers.py:64-142`).

3. Validate data quality:

   ```bash
   cd backend && python -m vocabdb validate --db vocabulary.db
   ```

   The command prints each validation issue and exits with status `1` when issues exist (`backend/vocabdb/cli.py:54-65`).

4. Export review JSON when a local JSON artifact is needed:

   ```bash
   cd backend && python -m vocabdb export-json --db vocabulary.db
   ```

   The default output path is `../frontend/review/vocabulary.json` (`backend/vocabdb/cli.py:16`, `backend/vocabdb/cli.py:35`). The exporter writes formatted UTF-8 JSON with `ensure_ascii=False` (`backend/vocabdb/exporters.py:48-56`).

5. Serve the REST API:

   ```bash
   cd backend && python -m vocabdb serve-api --db vocabulary.db
   ```

   The default API base is `http://localhost:8001`, and the API exposes `/api/health`, `/api/words`, and `/api/words/{lookup}`. `lookup` can be a numeric word id or a headword (`backend/vocabdb/cli.py:43-47`, `backend/vocabdb/api.py:14-73`).

6. Serve the review UI in another terminal:

   ```bash
   cd backend && python -m vocabdb serve-review
   ```

   The default served directory is `../frontend/review`. The static UI fetches word data from the API base and supports overriding that base with the `api` query parameter (`backend/vocabdb/cli.py:37-40`, `backend/vocabdb/cli.py:80-84`, `frontend/review/app.js:31-48`).

## Test Command

```bash
cd backend && pytest
```

The test suite imports the local `vocabdb` package because `backend/pyproject.toml` sets `pythonpath = ["."]` for pytest, and it uses FastAPI's `TestClient` for API coverage (`backend/pyproject.toml:19-20`, `backend/tests/test_vocabdb.py:5-11`).

## CI/CD

GitHub Actions runs backend tests on pull requests and `main` pushes. The workflow checks out the repository, sets up Python 3.11, installs the backend with test dependencies from `backend/`, and runs `pytest` from `backend/` (`.github/workflows/ci-cd.yml:14-37`).

On successful `main` pushes, the `build` job installs the backend, runs `vocabdb init-db` + `vocabdb import-anki` to produce `backend/vocabulary.db`, stages a slim `payload/backend/{vocabdb,pyproject.toml,vocabulary.db}` directory, and uploads it as a `deploy-payload` artifact (`.github/workflows/ci-cd.yml:39-82`). The `deploy` job then downloads the artifact, configures the SSH key, `rsync -avz --delete --exclude='.env' --exclude='.venv/' --exclude='server/' --exclude='backend/*.egg-info/'` ships the payload into `$DEPLOY_PATH/` using `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, and `DEPLOY_PATH`, ssh-bootstraps `.venv` if absent, installs the backend package, and restarts the `dict-english` systemd service (`.github/workflows/ci-cd.yml:84-130`).

The repository provides server-side sample templates but does not install them automatically. `server/nginx/dict-english.conf.example` is a location snippet that proxies `/dict/english/` to the local API process, while `server/systemd/dict-english.service.example` defines `DEPLOY_PATH`, reads `$DEPLOY_PATH/.env`, and runs `vocabdb serve-api` via `$DEPLOY_PATH/.venv/bin/python` from `$DEPLOY_PATH/backend`. Copy each `.example` to the live filename on the host (the live versions are gitignored as host-specific). `.env.example` is the commented template for the server-side `.env` file (`server/nginx/dict-english.conf.example:1-29`, `server/systemd/dict-english.service.example:1-32`, `.env.example:1-12`).

## Generated Files

The database, review JSON, and Python egg-info metadata are local generated files and should not be committed (`.gitignore:5-30`).

## Unconfirmed

- Reproducible environment setup is unconfirmed because no lock file pins dependency versions.
- VPS-side nginx and systemd installation is manual and not performed by GitHub Actions.
