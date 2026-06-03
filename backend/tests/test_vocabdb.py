from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from vocabdb.api import create_app
from vocabdb.db import connect, init_db
from vocabdb.exporters import build_review_payload, export_review_json
from vocabdb.importers import import_anki_tsv, insert_ai_example
from vocabdb.validation import validate_db


def test_init_db_creates_schema(tmp_path):
    db_path = tmp_path / "vocabulary.db"

    init_db(db_path)

    with connect(db_path) as conn:
        tables = {
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
    assert {
        "words",
        "meanings",
        "examples",
        "wordbook_entries",
        "audio_assets",
        "generation_reviews",
    }.issubset(tables)


def test_import_anki_tsv_and_export_review_json(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    source = tmp_path / "anki.txt"
    source.write_text(
        "\n".join(
            [
                "#separator:tab",
                "#html:true",
                "guid-1\t英→日\t英単語ターゲット1900 6訂版::Section 01\tnote-1\t\t\tcreate\tkriéit\tを創り出す；を引き起こす\tTechnology creates jobs.\t技術は雇用を生む。\t1\t動詞\t[sound:word.mp3]\t\t[sound:example.mp3]\t\tdefinition html\t0001\tTechnology c{{c1::reate}}s jobs.\timportant",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = import_anki_tsv(db_path, source)
    payload = build_review_payload(db_path)

    assert result.rows_seen == 1
    assert result.words_imported == 1
    assert payload["metadata"]["schema"] == "vocabdb.review.v1"
    assert payload["metadata"]["word_count"] == 1
    word = payload["words"][0]
    assert word["headword"] == "create"
    assert word["meanings"][0]["ja"] == "を創り出す；を引き起こす"
    assert word["examples"][0]["review_status"] == "approved"
    assert word["examples"][0]["source"] == "imported"
    assert word["wordbooks"][0]["wordbook_name"] == "英単語ターゲット1900"
    assert word["wordbooks"][0]["edition"] == "6"
    assert word["audio"]["word"][0]["ref"] == "[sound:word.mp3]"
    assert word["audio"]["examples"][0]["ref"] == "[sound:example.mp3]"


def test_export_review_json_writes_file(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    output = tmp_path / "review" / "vocabulary.json"
    init_db(db_path)
    _insert_word(db_path, "draft", word_audio="[sound:word.mp3]", example_audio="[sound:ex.mp3]")

    export_review_json(db_path, output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["metadata"]["word_count"] == 1
    assert data["words"][0]["examples"][0]["review_status"] == "draft"
    assert data["words"][0]["examples"][0]["source"] == "imported"


def test_validate_db_reports_quality_issues(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    init_db(db_path)
    _insert_word(db_path, "approved", headword="create", pronunciation="")
    _insert_word(
        db_path,
        "approved",
        headword="create",
        example_translation="",
        word_audio="",
        example_audio="",
    )

    issues = validate_db(db_path)
    codes = {issue.code for issue in issues}

    assert "duplicate_headword" in codes
    assert "missing_pronunciation" in codes
    assert "missing_example_translation" in codes
    assert "missing_word_audio" in codes
    assert "missing_example_audio" in codes


def test_json_includes_all_review_statuses(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    init_db(db_path)
    _insert_word(db_path, "draft", headword="draftword")
    _insert_word(db_path, "approved", headword="approvedword")
    _insert_word(db_path, "rejected", headword="rejectedword")

    payload = build_review_payload(db_path)
    statuses = {
        word["examples"][0]["review_status"]
        for word in payload["words"]
    }

    assert statuses == {"draft", "approved", "rejected"}


def test_ai_generated_examples_are_distinct_from_imported_examples(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    init_db(db_path)

    with connect(db_path) as conn:
        word_id = conn.execute(
            """
            INSERT INTO words (headword, lemma, pronunciation, part_of_speech)
            VALUES ('distinguish', 'distinguish', 'distíngwiʃ', 'verb')
            """
        ).lastrowid
        meaning_id = conn.execute(
            "INSERT INTO meanings (word_id, ja) VALUES (?, '区別する')",
            (word_id,),
        ).lastrowid
        imported_example_id = conn.execute(
            """
            INSERT INTO examples (word_id, meaning_id, sentence, ja_translation, source, review_status)
            VALUES (?, ?, 'Imported sentence.', '取り込み例文。', 'imported', 'approved')
            """,
            (word_id, meaning_id),
        ).lastrowid
        ai_example_id = insert_ai_example(
            conn,
            word_id,
            meaning_id,
            "AI generated sentence.",
            "AI生成例文。",
        )
        conn.execute(
            """
            INSERT INTO audio_assets (word_id, example_id, asset_type, ref)
            VALUES (?, ?, 'example', '[sound:example.mp3]')
            """,
            (word_id, imported_example_id),
        )
        conn.execute(
            """
            INSERT INTO audio_assets (word_id, example_id, asset_type, ref)
            VALUES (?, ?, 'example', '[sound:example2.mp3]')
            """,
            (word_id, ai_example_id),
        )

    payload = build_review_payload(db_path)
    example_sources = {example["source"] for example in payload["words"][0]["examples"]}

    assert example_sources == {"imported", "ai_generated"}


def test_api_health_returns_ok(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    init_db(db_path)
    client = TestClient(create_app(db_path))

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_lists_words_from_database(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    init_db(db_path)
    _insert_word(db_path, "approved", headword="create")
    _insert_word(db_path, "draft", headword="distinguish")
    client = TestClient(create_app(db_path))

    response = client.get("/api/words")

    assert response.status_code == 200
    data = response.json()
    assert data["metadata"]["word_count"] == 2
    assert [word["headword"] for word in data["words"]] == ["create", "distinguish"]
    assert data["words"][0]["meanings"][0]["ja"] == "意味"
    assert data["words"][0]["examples"][0]["review_status"] == "approved"
    assert data["words"][0]["audio"]["word"][0]["ref"] == "[sound:word.mp3]"


def test_api_gets_word_by_id(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    init_db(db_path)
    _insert_word(db_path, "approved", headword="create")
    client = TestClient(create_app(db_path))

    response = client.get("/api/words/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["headword"] == "create"
    assert data["wordbooks"][0]["wordbook_name"] == "testbook"


def test_api_returns_404_for_missing_word(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    init_db(db_path)
    client = TestClient(create_app(db_path))

    response = client.get("/api/words/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Word not found"}


def test_api_allows_browser_fetch_from_static_frontend(tmp_path):
    db_path = tmp_path / "vocabulary.db"
    init_db(db_path)
    client = TestClient(create_app(db_path))

    response = client.get("/api/words", headers={"Origin": "http://localhost:8000"})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "*"


def test_review_ui_loads_words_from_api():
    app_js = (Path(__file__).parents[2] / "frontend" / "review" / "app.js").read_text(
        encoding="utf-8"
    )

    assert 'new URL("/api/words", apiBaseUrl)' in app_js
    assert "vocabulary.json" not in app_js


def _insert_word(
    db_path,
    review_status,
    headword="test",
    pronunciation="tést",
    example_translation="例文訳",
    word_audio="[sound:word.mp3]",
    example_audio="[sound:example.mp3]",
):
    with connect(db_path) as conn:
        word_id = conn.execute(
            """
            INSERT INTO words (headword, lemma, pronunciation, part_of_speech)
            VALUES (?, ?, ?, 'verb')
            """,
            (headword, headword.lower(), pronunciation),
        ).lastrowid
        meaning_id = conn.execute(
            "INSERT INTO meanings (word_id, ja) VALUES (?, '意味')",
            (word_id,),
        ).lastrowid
        example_id = conn.execute(
            """
            INSERT INTO examples (word_id, meaning_id, sentence, ja_translation, review_status)
            VALUES (?, ?, 'This is a test.', ?, ?)
            """,
            (word_id, meaning_id, example_translation, review_status),
        ).lastrowid
        conn.execute(
            """
            INSERT INTO wordbook_entries (word_id, wordbook_name)
            VALUES (?, 'testbook')
            """,
            (word_id,),
        )
        conn.execute(
            """
            INSERT INTO audio_assets (word_id, asset_type, ref)
            VALUES (?, 'word', ?)
            """,
            (word_id, word_audio),
        )
        conn.execute(
            """
            INSERT INTO audio_assets (word_id, example_id, asset_type, ref)
            VALUES (?, ?, 'example', ?)
            """,
            (word_id, example_id, example_audio),
        )
