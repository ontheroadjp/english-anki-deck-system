from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .db import connect


def create_app(db_path: str | Path) -> FastAPI:
    app = FastAPI(title="Vocabulary DB API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.state.db_path = Path(db_path)

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/words")
    def list_words() -> dict[str, Any]:
        with connect(app.state.db_path) as conn:
            word_rows = conn.execute(
                """
                SELECT id, headword, lemma, pronunciation, part_of_speech, eiken, exam_level
                FROM words
                ORDER BY id
                """
            ).fetchall()
            words = [_build_word(conn, word["id"], word) for word in word_rows]

        return {
            "metadata": {"word_count": len(words)},
            "words": words,
        }

    @app.get("/api/words/{word_id}")
    def get_word(word_id: int) -> dict[str, Any]:
        with connect(app.state.db_path) as conn:
            word = conn.execute(
                """
                SELECT id, headword, lemma, pronunciation, part_of_speech, eiken, exam_level
                FROM words
                WHERE id = ?
                """,
                (word_id,),
            ).fetchone()
            if word is None:
                raise HTTPException(status_code=404, detail="Word not found")
            return _build_word(conn, word_id, word)

    return app


def _build_word(conn, word_id: int, word) -> dict[str, Any]:
    return {
        "id": word["id"],
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
