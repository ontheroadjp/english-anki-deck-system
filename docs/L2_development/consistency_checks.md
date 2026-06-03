# Consistency Checks

## Current Checks

Before changing generation behavior, compare these source-of-truth layers:

- Product goal: `docs/specification/L0_philosophy.md` defines the learning objective (`docs/specification/L0_philosophy.md:1-6`).
- Taxonomy: `docs/specification/L1_taxonomy.md` lists intended grammar categories (`docs/specification/L1_taxonomy.md:3-14`), while `data/grammar_patterns/grammar_taxonomy.yaml` contains implemented taxonomy data (`data/grammar_patterns/grammar_taxonomy.yaml:1-18`).
- Card schema: `docs/specification/L2_card_schema.md` defines the desired card fields (`docs/specification/L2_card_schema.md:3-19`).
- Generator output: `scripts/build_deck.py` currently exports five fields (`scripts/build_deck.py:18-24`).

## Known Gaps To Check

- Schema coverage: the implementation does not currently emit every field listed in the card schema (`docs/specification/L2_card_schema.md:3-19`, `scripts/build_deck.py:18-24`).
- Pipeline coverage: the specification includes validator and dedupe phases (`docs/specification/L3_generation_pipeline.md:3-8`), but no separate validator or dedupe implementation is present in the observed file list.
- Template metadata usage: `sample_template.yaml` contains `error_category` and `error_pattern` (`data/templates/sample_template.yaml:19-24`), but the current exporter does not include them in `cards.append` (`scripts/build_deck.py:18-24`).

## Suggested Manual Verification

Run the generator from the repository root:

```bash
python scripts/build_deck.py
```

Then inspect `generated.csv` and verify that its columns match the fields intentionally supported by the current implementation (`scripts/build_deck.py:18-28`).

## Unconfirmed

- Automated consistency checks are unconfirmed because no test runner, test files, or CI workflow exists.
