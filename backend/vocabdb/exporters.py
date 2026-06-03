from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .db import connect


def build_review_payload(db_path: str | Path) -> dict[str, Any]:
    with connect(db_path) as conn:
        words = conn.execute(
            """
            SELECT id, headword, lemma, pronunciation, part_of_speech, eiken, exam_level
            FROM words
            ORDER BY id
            """
        ).fetchall()

        payload_words = []
        for word in words:
            word_id = word["id"]
            payload_words.append(
                {
                    "id": word_id,
                    "headword": word["headword"],
                    "lemma": word["lemma"],
                    "pronunciation": word["pronunciation"],
                    "part_of_speech": word["part_of_speech"],
                    "eiken": word["eiken"],
                    "exam_level": word["exam_level"],
                    "meanings": _meanings(conn, word_id),
                    "examples": _examples(conn, word_id),
                    "wordbooks": _wordbooks(conn, word_id),
                    "audio": _audio(conn, word_id),
                }
            )

    return {
        "metadata": {
            "schema": "vocabdb.review.v1",
            "word_count": len(payload_words),
        },
        "words": payload_words,
    }


def export_review_json(db_path: str | Path, output_path: str | Path) -> None:
    payload = build_review_payload(db_path)
    path = Path(output_path)
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _meanings(conn, word_id: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT id, ja, usage_label, priority
        FROM meanings
        WHERE word_id = ?
        ORDER BY priority, id
        """,
        (word_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def _examples(conn, word_id: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT id, meaning_id, sentence, ja_translation, cloze_sentence,
               english_definition_html, source, review_status
        FROM examples
        WHERE word_id = ?
        ORDER BY id
        """,
        (word_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def _wordbooks(conn, word_id: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT wordbook_name, edition, deck_path, target_number, rank_or_level,
               note_id, guid, note_type
        FROM wordbook_entries
        WHERE word_id = ?
        ORDER BY id
        """,
        (word_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def _audio(conn, word_id: int) -> dict[str, Any]:
    rows = conn.execute(
        """
        SELECT example_id, asset_type, ref, url
        FROM audio_assets
        WHERE word_id = ?
        ORDER BY id
        """,
        (word_id,),
    ).fetchall()
    return {
        "word": [dict(row) for row in rows if row["asset_type"] == "word"],
        "examples": [dict(row) for row in rows if row["asset_type"] == "example"],
    }
