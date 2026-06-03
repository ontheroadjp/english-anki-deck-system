from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    headword TEXT NOT NULL,
    lemma TEXT NOT NULL,
    pronunciation TEXT,
    part_of_speech TEXT,
    eiken TEXT,
    exam_level TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_words_headword ON words(headword);

CREATE TABLE IF NOT EXISTS meanings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    ja TEXT NOT NULL,
    usage_label TEXT,
    priority INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_meanings_word_id ON meanings(word_id);

CREATE TABLE IF NOT EXISTS examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    meaning_id INTEGER REFERENCES meanings(id) ON DELETE SET NULL,
    sentence TEXT NOT NULL,
    ja_translation TEXT,
    cloze_sentence TEXT,
    english_definition_html TEXT,
    source TEXT NOT NULL DEFAULT 'imported'
        CHECK (source IN ('imported', 'ai_generated')),
    review_status TEXT NOT NULL DEFAULT 'draft'
        CHECK (review_status IN ('draft', 'approved', 'rejected')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_examples_word_id ON examples(word_id);
CREATE INDEX IF NOT EXISTS idx_examples_review_status ON examples(review_status);

CREATE TABLE IF NOT EXISTS wordbook_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    wordbook_name TEXT NOT NULL,
    edition TEXT,
    deck_path TEXT,
    target_number TEXT,
    rank_or_level TEXT,
    note_id TEXT,
    guid TEXT,
    note_type TEXT
);

CREATE INDEX IF NOT EXISTS idx_wordbook_entries_word_id ON wordbook_entries(word_id);

CREATE TABLE IF NOT EXISTS audio_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
    example_id INTEGER REFERENCES examples(id) ON DELETE CASCADE,
    asset_type TEXT NOT NULL CHECK (asset_type IN ('word', 'example')),
    ref TEXT,
    url TEXT
);

CREATE INDEX IF NOT EXISTS idx_audio_assets_word_id ON audio_assets(word_id);
CREATE INDEX IF NOT EXISTS idx_audio_assets_example_id ON audio_assets(example_id);

CREATE TABLE IF NOT EXISTS generation_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    example_id INTEGER NOT NULL REFERENCES examples(id) ON DELETE CASCADE,
    provider TEXT,
    prompt TEXT,
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'approved', 'rejected')),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(Path(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str | Path) -> None:
    path = Path(db_path)
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as conn:
        conn.executescript(SCHEMA)
