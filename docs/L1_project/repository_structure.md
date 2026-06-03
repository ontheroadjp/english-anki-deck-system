# Repository Structure

## Top-Level Structure

- `AGENTS.md`: AI entry-point guidance and role definitions. It instructs agents to read the four specification files first and lists architect, generator, validator, and exporter roles (`AGENTS.md:3-24`).
- `README.md`: project summary and generation flow (`README.md:1-14`).
- `data/`: structured source data used by the generator. The taxonomy YAML contains grammar categories and patterns (`data/grammar_patterns/grammar_taxonomy.yaml:1-18`), and the template YAML contains a sample sentence template with variables and metadata (`data/templates/sample_template.yaml:1-24`).
- `docs/specification/`: existing product and implementation specifications. These define the goal, taxonomy, card schema, and generation pipeline (`docs/specification/L0_philosophy.md:1-6`, `docs/specification/L1_taxonomy.md:1-22`, `docs/specification/L2_card_schema.md:1-19`, `docs/specification/L3_generation_pipeline.md:1-14`).
- `scripts/`: executable generator implementation. `scripts/build_deck.py` reads template YAML files and writes `generated.csv` (`scripts/build_deck.py:5-28`).

## Data Directories

- `data/grammar_patterns/` currently stores `grammar_taxonomy.yaml`, whose root key is `grammar_taxonomy` (`data/grammar_patterns/grammar_taxonomy.yaml:1-18`).
- `data/templates/` currently stores `sample_template.yaml`, which defines `template_id`, `correct`, `incorrect_patterns`, `variables`, and `metadata` (`data/templates/sample_template.yaml:1-24`).

## Monorepo Check

No `apps/`, `packages/`, or package manifests are present in the observed file list. There is no confirmed monorepo structure.

## Unconfirmed

- Test, CI, packaging, and dependency-management responsibilities are unconfirmed because no corresponding files exist in the current repository.
