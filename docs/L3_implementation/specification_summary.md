# Specification Summary

## Implemented Generator

`scripts/build_deck.py` is the only confirmed executable implementation. It imports `pandas`, `yaml`, and `Path` (`scripts/build_deck.py:1-3`), reads all YAML templates under `data/templates` (`scripts/build_deck.py:5-9`), expands template sentences with each configured noun (`scripts/build_deck.py:11-17`), appends card dictionaries (`scripts/build_deck.py:18-24`), and exports them to `generated.csv` (`scripts/build_deck.py:26-28`).

## Template Contract

The current implementation expects these fields:

- `correct`: sentence template formatted with `{noun}` (`scripts/build_deck.py:12`, `data/templates/sample_template.yaml:3-4`).
- `incorrect_patterns`: list of mappings whose values are incorrect sentence templates (`scripts/build_deck.py:14-17`, `data/templates/sample_template.yaml:6-11`).
- `variables.noun`: list of nouns used for expansion (`scripts/build_deck.py:11`, `data/templates/sample_template.yaml:13-17`).
- `metadata.grammar_unit`, `metadata.difficulty`, and `metadata.eiken`: values copied into each generated card (`scripts/build_deck.py:21-23`, `data/templates/sample_template.yaml:19-24`).

## Output Contract

The current CSV output contains these columns because those are the keys appended to each card:

- `incorrect_sentence` (`scripts/build_deck.py:18-20`)
- `correct_sentence` (`scripts/build_deck.py:18-20`)
- `grammar_unit` (`scripts/build_deck.py:21`)
- `difficulty` (`scripts/build_deck.py:22`)
- `eiken` (`scripts/build_deck.py:23`)

The output file path is `generated.csv`, and the encoding is `utf-8-sig` (`scripts/build_deck.py:26-28`).

## Data Model

The intended card schema is broader than the implemented output. The specification lists fields from `id` through `source_template` (`docs/specification/L2_card_schema.md:3-19`), but the implementation currently writes only five fields (`scripts/build_deck.py:18-24`).

## Pipeline Coverage

The specified pipeline is taxonomy definition, template creation, sentence generation, validator, dedupe, and CSV export (`docs/specification/L3_generation_pipeline.md:3-8`). The current implementation covers template reading, sentence generation, and CSV export (`scripts/build_deck.py:5-28`). Validator and dedupe are not implemented in the observed repository files.

## Unconfirmed

- API endpoints are unconfirmed because no server, routing, or API files exist.
- Database behavior is unconfirmed because no schema, migration, or database access code exists.
- Validation and deduplication behavior is unconfirmed because no implementation files for those phases exist.
