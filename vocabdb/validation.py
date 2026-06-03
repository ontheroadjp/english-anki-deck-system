from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .db import connect


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    word_id: int | None = None
    example_id: int | None = None


def validate_db(db_path: str | Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    with connect(db_path) as conn:
        duplicate_rows = conn.execute(
            """
            SELECT lower(headword) AS normalized, COUNT(*) AS count
            FROM words
            GROUP BY lower(headword)
            HAVING COUNT(*) > 1
            """
        ).fetchall()
        for row in duplicate_rows:
            issues.append(
                ValidationIssue(
                    "duplicate_headword",
                    f"Duplicate headword: {row['normalized']} ({row['count']} rows)",
                )
            )

        for row in conn.execute(
            "SELECT id, headword FROM words WHERE pronunciation IS NULL OR pronunciation = ''"
        ):
            issues.append(
                ValidationIssue(
                    "missing_pronunciation",
                    f"Missing pronunciation: {row['headword']}",
                    word_id=row["id"],
                )
            )

        for row in conn.execute(
            """
            SELECT e.id AS example_id, w.id AS word_id, w.headword
            FROM examples e
            JOIN words w ON w.id = e.word_id
            WHERE e.ja_translation IS NULL OR e.ja_translation = ''
            """
        ):
            issues.append(
                ValidationIssue(
                    "missing_example_translation",
                    f"Missing example translation: {row['headword']}",
                    word_id=row["word_id"],
                    example_id=row["example_id"],
                )
            )

        for row in conn.execute(
            """
            SELECT w.id, w.headword
            FROM words w
            WHERE NOT EXISTS (
                SELECT 1 FROM audio_assets a
                WHERE a.word_id = w.id
                  AND a.asset_type = 'word'
                  AND (a.ref IS NOT NULL AND a.ref != '' OR a.url IS NOT NULL AND a.url != '')
            )
            """
        ):
            issues.append(
                ValidationIssue(
                    "missing_word_audio",
                    f"Missing word audio: {row['headword']}",
                    word_id=row["id"],
                )
            )

        for row in conn.execute(
            """
            SELECT e.id AS example_id, w.id AS word_id, w.headword
            FROM examples e
            JOIN words w ON w.id = e.word_id
            WHERE NOT EXISTS (
                SELECT 1 FROM audio_assets a
                WHERE a.example_id = e.id
                  AND a.asset_type = 'example'
                  AND (a.ref IS NOT NULL AND a.ref != '' OR a.url IS NOT NULL AND a.url != '')
            )
            """
        ):
            issues.append(
                ValidationIssue(
                    "missing_example_audio",
                    f"Missing example audio: {row['headword']}",
                    word_id=row["word_id"],
                    example_id=row["example_id"],
                )
            )

    return issues
