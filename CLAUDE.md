# CLAUDE.md

このファイルは AI 運用の起点となる情報をまとめる。このリポジトリで作業する際は、まず `AGENTS.md` と `README.md` を読み、次に `docs/specification/` と `docs/L0_concept/` を確認する。

## このリポジトリについて

このリポジトリは、大学受験向け英語誤文訂正 Anki デッキを生成するためのシステムである。目的は英文法暗記ではなく、誤文検知能力を高めることにある。

作業開始時に `README.md` の以下のセクションを読むこと:

- `## Features`
- `## Usage`
- `## Design Principles`
- `## Architecture`

## Custom / Command の使い分け（AI向けルール）

- task.md: ドキュメント変更を伴う実装に特化。issue 自動生成〜実装〜ドラフト PR 作成まで。docs/* は変更しない。
- patch.md: ドキュメント変更を伴わない軽微な修正に特化。issue/PR 不要。branch + commit → ユーザーが main へマージ。スコープが広がった場合は /task へエスカレーション。
- docs-sync.md: git diff を事実として docs を最小更新し、ドラフト PR を公開する。HARD STOP 時は /init-docs を要求して終了する。
- init-docs.md: repo の実態把握と設計ドキュメント再構築。重い初期化。docs-sync が説明不能になった時点でここに戻る。

## 重要な設計原則

- カードはテンプレートから生成する。`docs/specification/L3_generation_pipeline.md` は直接カード生成を禁止している。
- Taxonomy / template / schema を SSOT として扱い、実装変更時は `docs/specification/` と `docs/L*_*/` の整合性を確認する。
- 現在の実装は `scripts/build_deck.py` が `data/templates/*.yaml` を読み、`generated.csv` を出力する構成である。
- 依存関係ファイルがないため、Python バージョンや依存ライブラリのバージョンは断定しない。

## 実行コマンド

現時点で確認できる実行コマンド:

```bash
python scripts/build_deck.py
```

このコマンドは `generated.csv` を生成する。テストコマンド、CI、依存関係インストールコマンドは未定義。
