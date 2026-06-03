from __future__ import annotations

import argparse
import functools
import http.server
import socketserver
from pathlib import Path

from .db import init_db
from .exporters import export_review_json
from .importers import import_anki_tsv
from .validation import validate_db


DEFAULT_DB = Path("vocabulary.db")
DEFAULT_REVIEW_JSON = Path("../frontend/review/vocabulary.json")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vocabdb")
    subcommands = parser.add_subparsers(dest="command", required=True)

    init_parser = subcommands.add_parser("init-db", help="Initialize a SQLite DB.")
    init_parser.add_argument("--db", default=DEFAULT_DB)

    import_parser = subcommands.add_parser("import-anki", help="Import an Anki TSV export.")
    import_parser.add_argument("source")
    import_parser.add_argument("--db", default=DEFAULT_DB)

    validate_parser = subcommands.add_parser("validate", help="Validate vocabulary data.")
    validate_parser.add_argument("--db", default=DEFAULT_DB)

    export_parser = subcommands.add_parser("export-json", help="Export review JSON.")
    export_parser.add_argument("--db", default=DEFAULT_DB)
    export_parser.add_argument("--output", default=DEFAULT_REVIEW_JSON)

    serve_parser = subcommands.add_parser("serve-review", help="Serve the static review UI.")
    serve_parser.add_argument("--directory", default="../frontend/review")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)

    if args.command == "init-db":
        init_db(args.db)
        print(f"Initialized {args.db}")
        return 0

    if args.command == "import-anki":
        result = import_anki_tsv(args.db, args.source)
        print(f"Imported {result.words_imported} words from {result.rows_seen} rows")
        return 0

    if args.command == "validate":
        issues = validate_db(args.db)
        for issue in issues:
            location = []
            if issue.word_id is not None:
                location.append(f"word_id={issue.word_id}")
            if issue.example_id is not None:
                location.append(f"example_id={issue.example_id}")
            suffix = f" ({', '.join(location)})" if location else ""
            print(f"{issue.code}: {issue.message}{suffix}")
        print(f"{len(issues)} issue(s)")
        return 1 if issues else 0

    if args.command == "export-json":
        export_review_json(args.db, args.output)
        print(f"Exported {args.output}")
        return 0

    if args.command == "serve-review":
        serve_review(args.directory, args.host, args.port)
        return 0

    parser.error("Unknown command")
    return 2


def serve_review(directory: str | Path, host: str, port: int) -> None:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    with socketserver.TCPServer((host, port), handler) as server:
        print(f"Serving review UI at http://{host}:{port}/")
        server.serve_forever()
