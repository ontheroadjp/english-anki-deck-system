# Specification Summary

## CLI

The implemented CLI is available through `python -m vocabdb` because `backend/vocabdb/__main__.py` imports `main` and raises `SystemExit` with its return code (`backend/vocabdb/__main__.py:1-3`). `backend/vocabdb/cli.py` defines six subcommands: `init-db`, `import-anki`, `validate`, `export-json`, `serve-review`, and `serve-api` (`backend/vocabdb/cli.py:20-47`). All commands assume the working directory is `backend/`; defaults for `--output` and `--directory` use `../frontend/review`, while `serve-api` defaults to `vocabulary.db` on `localhost:8001` (`backend/vocabdb/cli.py:15-17`, `backend/vocabdb/cli.py:34-47`).

## Database Layer

The SQLite schema is stored as a SQL string in `backend/vocabdb/db.py` and executed by `init_db` (`backend/vocabdb/db.py:7-87`, `backend/vocabdb/db.py:98-103`). The connection helper enables foreign keys and returns rows as `sqlite3.Row` objects (`backend/vocabdb/db.py:91-95`). This matters because import, validation, and export code all access columns by name.

## Import Logic

`import_anki_tsv` initializes the DB, skips Anki metadata header lines beginning with `#`, parses rows with `csv.DictReader(..., delimiter="\t")`, and inserts one normalized vocabulary record per non-empty headword row (`backend/vocabdb/importers.py:43-61`). Each row inserts:

- a word with headword, lemma, pronunciation, part of speech, and exam level (`backend/vocabdb/importers.py:64-78`)
- a meaning (`backend/vocabdb/importers.py:80-86`)
- an imported example with `source = 'imported'` and `review_status = 'approved'` (`backend/vocabdb/importers.py:88-110`)
- source wordbook metadata (`backend/vocabdb/importers.py:112-139`)
- word and example audio refs (`backend/vocabdb/importers.py:141-142`, `backend/vocabdb/importers.py:181-194`)

`insert_ai_example` provides the AI-generated path. It forces `source = 'ai_generated'` and defaults `review_status = 'draft'` (`backend/vocabdb/importers.py:145-178`).

## Validation Logic

`validate_db` returns `ValidationIssue` records for duplicate normalized headwords, missing pronunciation, missing example translation, missing word audio, and missing example audio (`backend/vocabdb/validation.py:9-17`, `backend/vocabdb/validation.py:20-106`). The CLI prints those issues and returns a non-zero exit status when any issue exists (`backend/vocabdb/cli.py:54-65`).

## JSON Export

`build_review_payload` queries words and adds nested `meanings`, `examples`, `wordbooks`, and `audio` arrays for each word (`backend/vocabdb/exporters.py:10-45`, `backend/vocabdb/exporters.py:59-113`). `export_review_json` writes that payload as UTF-8 JSON (`backend/vocabdb/exporters.py:48-56`). The payload schema name is `vocabdb.review.v1` (`backend/vocabdb/exporters.py:39-45`). Audio is exposed at word level, split into `audio.word` and `audio.examples`, with each example audio entry carrying `example_id` so the UI can join by example (`backend/vocabdb/exporters.py:100-113`).

## REST API

`backend/vocabdb/api.py` defines `create_app(db_path)`, which returns a FastAPI application, enables browser GET access through CORS middleware, and stores the SQLite path on `app.state.db_path` (`backend/vocabdb/api.py:10-19`). The API surface is read-only and uses API-specific SQLite queries instead of calling the review JSON exporter (`backend/vocabdb/api.py:21-147`).

Implemented endpoints:

- `GET /api/health`: returns `{"status": "ok"}` (`backend/vocabdb/api.py:21-23`).
- `GET /api/words`: returns `metadata.word_count` and a `words` array ordered by word id (`backend/vocabdb/api.py:25-38`).
- `GET /api/words/{lookup}`: returns one word record by numeric word id or by case-insensitive headword, and raises HTTP 404 with `detail = "Word not found"` when no matching record exists (`backend/vocabdb/api.py:40-73`).

Each word response includes the word fields plus nested `meanings`, `examples`, `wordbooks`, and `audio` data assembled from the normalized SQLite tables (`backend/vocabdb/api.py:78-147`). The `serve-api` CLI command imports Uvicorn and the FastAPI app factory at runtime, then runs the app with the configured host and port (`backend/vocabdb/cli.py:93-101`).

## Web Review UI

The static UI declares a search box, a review-status filter, and a Cards / Table tab strip in HTML, with two sibling view sections (`frontend/review/index.html:11-35`). JavaScript fetches `/api/words` from the configured API base, stores words in memory, filters by text and review status, and dispatches rendering by active view (`frontend/review/app.js:31-92`). The default API base is `http://localhost:8001`, and callers can override it with the `api` query parameter (`frontend/review/app.js:31-32`). The card renderer outputs one card per word with meanings, examples, wordbook labels, and word audio refs (`frontend/review/app.js:167-211`). The table renderer outputs one row per example with twelve columns including headword, pronunciation, part of speech, exam level, meanings, example sentence, example translation, source badge, status badge, wordbook label, word audio refs, and example audio refs (`frontend/review/app.js:94-141`). Example audio in the table view is joined from `word.audio.examples` by `example_id` (`frontend/review/app.js:120-124`).

## Dependency Metadata

`backend/pyproject.toml` declares the backend package name, Python version requirement, FastAPI and Uvicorn runtime dependencies, optional test dependencies for httpx and pytest, setuptools package discovery limited to `vocabdb*`, and pytest `pythonpath` configuration (`backend/pyproject.toml:1-20`).

## CI/CD and Server Configuration

`.github/workflows/ci-cd.yml` defines the GitHub Actions automation as a three-job pipeline. The `test` job runs on pull requests and `main` pushes, sets up Python 3.11, installs the backend package with the `test` extra from `backend/`, and runs `pytest` from `backend/` (`.github/workflows/ci-cd.yml:14-37`). The `build` job runs only for `main` push events after `test` succeeds, installs the backend, runs `vocabdb init-db` + `vocabdb import-anki` to produce `backend/vocabulary.db`, stages a slim `payload/backend/{vocabdb,pyproject.toml,vocabulary.db}` directory, and uploads it as a `deploy-payload` artifact (`.github/workflows/ci-cd.yml:39-82`). The `deploy` job runs after `build`, downloads the artifact, configures the SSH key, `rsync -avz --delete` ships the payload into `$DEPLOY_PATH/` using `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, and `DEPLOY_PATH` (preserving `.env`, `.venv/`, and `backend/*.egg-info/` on the host), ssh-bootstraps `.venv` if absent, installs the backend package, and restarts `dict-english` (`.github/workflows/ci-cd.yml:84-129`).

Server-side configuration sample templates are tracked under `server/` for manual installation. `server/nginx/dict-english.conf.example` is a location snippet that proxies `/dict/english/` to the local backend API process (`server/nginx/dict-english.conf.example:1-29`). `server/systemd/dict-english.service.example` defines `DEPLOY_PATH`, loads `$DEPLOY_PATH/.env`, changes into `$DEPLOY_PATH/backend`, and runs `vocabdb serve-api` via `$DEPLOY_PATH/.venv/bin/python` with DB, host, and port values from the env file. Copy each `.example` to the live filename on the host (the live versions are gitignored as host-specific). `.env.example` is the commented template for that `.env` file (`server/systemd/dict-english.service.example:1-32`, `.env.example:1-12`).

## Generated Artifacts

`backend/vocabulary.db`, `frontend/review/vocabulary.json`, and Python `*.egg-info/` metadata are generated local artifacts and are excluded from git (`.gitignore:5-30`).

## Unconfirmed

- No migration versioning system is implemented beyond the idempotent schema string in `backend/vocabdb/db.py`.
- VPS-side nginx and systemd installation is manual and not automated by the repository.
