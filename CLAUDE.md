# CLAUDE.md

このファイルは AI 運用の起点となる情報をまとめる。このリポジトリで作業する際は、まず `AGENTS.md` と `README.md` を読み、次に `docs/L0_concept/` と `docs/L1_project/`、必要に応じて `docs/L3_implementation/` を確認する。

## このリポジトリについて

このリポジトリは、大学受験向け英単語データを SQLite に保存し、レビュー用 JSON とブラウザ表示を生成する語彙 DB システムである。現在の実装は `python -m vocabdb` を入口に、DB 初期化、Anki TSV import、validation、JSON export、local review UI serving を行う。

作業開始時に `README.md` の以下のセクションを読むこと:

- `## Features`
- `## Installation`
- `## Usage`
- `## Design Principles`
- `## Architecture`

## Custom / Command の使い分け（AI向けルール）

- task.md: ドキュメント変更を伴う実装に特化。issue 自動生成〜実装〜ドラフト PR 作成まで。docs/* は変更しない。
- patch.md: ドキュメント変更を伴わない軽微な修正に特化。issue/PR 不要。branch + commit → ユーザーが main へマージ。スコープが広がった場合は /task へエスカレーション。
- docs-sync.md: git diff を事実として docs を最小更新し、ドラフト PR を公開する。HARD STOP 時は /init-docs を要求して終了する。
- init-docs.md: repo の実態把握と設計ドキュメント再構築。重い初期化。docs-sync が説明不能になった時点でここに戻る。

## 重要な設計原則

- SQLite を語彙データの source of truth として扱う。生成された `vocabulary.db` は git 管理しない。
- v1 の出力は review JSON と静的 Web review UI である。Anki CSV export は現在の実装には存在しない。
- `frontend/review/vocabulary.json` は生成物であり、DB から再生成する。
- Anki の `[sound:...]` は URL として扱わず、audio ref として保存する。
- 例文レビュー状態は `draft` / `approved` / `rejected` に揃える。

## 実行コマンド

すべて `backend/` をカレントとして実行する。

```bash
cd backend
python -m vocabdb init-db --db vocabulary.db
python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db
python -m vocabdb validate --db vocabulary.db
python -m vocabdb export-json --db vocabulary.db
python -m vocabdb serve-review
pytest
```

`export-json` の出力先は既定で `../frontend/review/vocabulary.json`、`serve-review` の配信ディレクトリは既定で `../frontend/review` を指す。

## 未確認事項

- CI は未定義。
- 本番デプロイ先は未定義。
- 依存関係のlock fileは未定義。
