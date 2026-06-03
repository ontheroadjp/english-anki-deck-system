from __future__ import annotations

import csv
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .db import connect, init_db


ANKI_COLUMNS = [
    "guid",
    "note_type",
    "deck",
    "note_id",
    "image_html",
    "related_words_html",
    "headword",
    "pronunciation",
    "japanese_meaning",
    "example_sentence",
    "example_translation",
    "word_rank_or_level",
    "part_of_speech",
    "headword_audio",
    "reserved_1",
    "example_audio",
    "reserved_2",
    "english_definition_html",
    "target_number",
    "cloze_example_sentence",
    "tags",
]


@dataclass(frozen=True)
class ImportResult:
    rows_seen: int
    words_imported: int


def import_anki_tsv(db_path: str | Path, source_path: str | Path) -> ImportResult:
    init_db(db_path)
    source = Path(source_path)
    rows_seen = 0
    imported = 0

    with source.open("r", encoding="utf-8-sig", newline="") as f:
        data_lines = [line for line in f if not line.startswith("#")]

    with connect(db_path) as conn:
        reader = csv.DictReader(data_lines, fieldnames=ANKI_COLUMNS, delimiter="\t")
        for row in reader:
            rows_seen += 1
            if not row.get("headword"):
                continue
            _insert_anki_row(conn, row)
            imported += 1

    return ImportResult(rows_seen=rows_seen, words_imported=imported)


def _insert_anki_row(conn: sqlite3.Connection, row: dict[str, str | None]) -> None:
    headword = _clean(row.get("headword"))
    word_id = conn.execute(
        """
        INSERT INTO words (headword, lemma, pronunciation, part_of_speech, exam_level)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            headword,
            headword.lower(),
            _clean(row.get("pronunciation")),
            _clean(row.get("part_of_speech")),
            _clean(row.get("word_rank_or_level")),
        ),
    ).lastrowid

    meaning_id = conn.execute(
        """
        INSERT INTO meanings (word_id, ja, priority)
        VALUES (?, ?, 1)
        """,
        (word_id, _clean(row.get("japanese_meaning")) or "(missing meaning)"),
    ).lastrowid

    example_id = conn.execute(
        """
        INSERT INTO examples (
            word_id,
            meaning_id,
            sentence,
            ja_translation,
            cloze_sentence,
            english_definition_html,
            source,
            review_status
        )
        VALUES (?, ?, ?, ?, ?, ?, 'imported', 'approved')
        """,
        (
            word_id,
            meaning_id,
            _clean(row.get("example_sentence")) or "(missing example)",
            _clean(row.get("example_translation")),
            _clean(row.get("cloze_example_sentence")),
            _clean(row.get("english_definition_html")),
        ),
    ).lastrowid

    wordbook_name, edition = _parse_wordbook(_clean(row.get("deck")))
    conn.execute(
        """
        INSERT INTO wordbook_entries (
            word_id,
            wordbook_name,
            edition,
            deck_path,
            target_number,
            rank_or_level,
            note_id,
            guid,
            note_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            word_id,
            wordbook_name,
            edition,
            _clean(row.get("deck")),
            _clean(row.get("target_number")),
            _clean(row.get("word_rank_or_level")),
            _clean(row.get("note_id")),
            _clean(row.get("guid")),
            _clean(row.get("note_type")),
        ),
    )

    _insert_audio(conn, word_id, None, "word", _clean(row.get("headword_audio")))
    _insert_audio(conn, word_id, example_id, "example", _clean(row.get("example_audio")))


def insert_ai_example(
    conn: sqlite3.Connection,
    word_id: int,
    meaning_id: int | None,
    sentence: str,
    ja_translation: str | None,
    cloze_sentence: str | None = None,
    english_definition_html: str | None = None,
    review_status: str = "draft",
) -> int:
    return conn.execute(
        """
        INSERT INTO examples (
            word_id,
            meaning_id,
            sentence,
            ja_translation,
            cloze_sentence,
            english_definition_html,
            source,
            review_status
        )
        VALUES (?, ?, ?, ?, ?, ?, 'ai_generated', ?)
        """,
        (
            word_id,
            meaning_id,
            sentence,
            ja_translation,
            cloze_sentence,
            english_definition_html,
            review_status,
        ),
    ).lastrowid


def _insert_audio(
    conn: sqlite3.Connection,
    word_id: int,
    example_id: int | None,
    asset_type: str,
    ref: str,
) -> None:
    conn.execute(
        """
        INSERT INTO audio_assets (word_id, example_id, asset_type, ref, url)
        VALUES (?, ?, ?, ?, NULL)
        """,
        (word_id, example_id, asset_type, ref),
    )


def _parse_wordbook(deck: str) -> tuple[str, str | None]:
    if not deck:
        return ("unknown", None)
    first = deck.split("::", 1)[0]
    edition_match = re.search(r"(\d+)\s*訂版", first)
    edition = edition_match.group(1) if edition_match else None
    name = re.sub(r"\s*\d+\s*訂版", "", first).strip()
    return (name or first, edition)


def _clean(value: str | None) -> str:
    return (value or "").strip()
