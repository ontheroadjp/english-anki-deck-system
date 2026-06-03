# Policy

## Source Of Truth

The repository uses specification documents and YAML source data as the current source of truth for grammar taxonomy, card schema, and generation flow (`AGENTS.md:3-10`, `docs/specification/L1_taxonomy.md:1-22`, `docs/specification/L2_card_schema.md:1-19`, `docs/specification/L3_generation_pipeline.md:1-14`).

## Generation Policy

Cards should remain template-derived. This is required because the generation specification explicitly prohibits direct card generation and requires template-based generation (`docs/specification/L3_generation_pipeline.md:10-14`). The current script follows this direction by reading YAML templates from `data/templates` and formatting sentences from template variables (`scripts/build_deck.py:5-17`).

## Data Policy

Grammar categories and patterns should be represented as structured data. The existing taxonomy is stored under `grammar_taxonomy` in YAML (`data/grammar_patterns/grammar_taxonomy.yaml:1-18`), and the sample template stores correct sentence text, incorrect patterns, variables, and metadata as YAML fields (`data/templates/sample_template.yaml:1-24`).

## Dependency Policy

The implementation imports `pandas` and `yaml` (`scripts/build_deck.py:1-2`), but no dependency manifest or lock file exists. Until dependency files are added, dependency versions must be treated as unconfirmed and should not be asserted in docs.

## Security And Performance

No network, credential, database, or external service integration is implemented in the current repository. The only confirmed script reads local YAML files and writes a local CSV file (`scripts/build_deck.py:5-28`).

## Unconfirmed

- Security requirements beyond local file generation are unconfirmed because no deployment, authentication, or external API code exists. Add implementation or policy files if those become part of the system.
- Performance requirements are unconfirmed because no benchmarks, data volume targets, or CI checks exist. Add benchmark or acceptance criteria files to make them reviewable.
