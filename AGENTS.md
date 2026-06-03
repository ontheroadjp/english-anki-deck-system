# AGENTS

## Entry Point

最初に以下を読む:

1. `README.md`
2. `docs/L0_concept/concept.md`
3. `docs/L0_concept/policy.md`
4. `docs/L1_project/project_overview.md`
5. `docs/L1_project/repository_structure.md`
6. 必要に応じて `docs/L3_implementation/specification_summary.md` と `docs/L3_implementation/database.md`

## Roles

### architect-agent

SQLite schema / JSON review schema / vocabulary data model 設計。

### importer-agent

Anki TSV source から SQLite 語彙 DB への取り込み。

### validator-agent

重複・欠損発音・欠損例文訳・欠損音声 ref の検査。

### exporter-agent

SQLite DB から review JSON を出力。

### review-ui-agent

`frontend/review/` の静的レビュー UI を保守。
