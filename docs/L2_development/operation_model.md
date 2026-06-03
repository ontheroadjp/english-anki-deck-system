# Operation Model

## Confirmed Command

Run the current generator from the repository root:

```bash
python scripts/build_deck.py
```

This command is grounded in the generator implementation: it reads YAML templates from `data/templates` and writes `generated.csv` in the current working directory (`scripts/build_deck.py:5-28`).

## Expected Inputs

- Template YAML files must exist under `data/templates` because the script glob is `Path("data/templates").glob("*.yaml")` (`scripts/build_deck.py:5`).
- Each template must provide `correct`, `incorrect_patterns`, `variables.noun`, and `metadata` fields used by the script (`scripts/build_deck.py:11-24`). The sample template provides those fields (`data/templates/sample_template.yaml:1-24`).

## Expected Output

The script writes `generated.csv` with UTF-8 BOM encoding (`utf-8-sig`) and prints `generated.csv created` (`scripts/build_deck.py:26-28`).

## Installation

No install command is confirmed. The script imports `pandas` and `yaml` (`scripts/build_deck.py:1-2`), but the repository does not include a dependency manifest or lock file.

## Build And Test

No CI workflow, package script, test directory, or test command is present in the observed repository. The only confirmed runnable command is `python scripts/build_deck.py`.

## Unconfirmed

- Exact setup command is unconfirmed because dependency files are absent. Add `requirements.txt` or `pyproject.toml` to make installation reproducible.
- Test command is unconfirmed because no test files or CI test steps exist.
