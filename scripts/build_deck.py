from __future__ import annotations

import sys


MESSAGE = """The old grammar deck generator has been replaced.

Use the vocabulary database CLI instead:

  python -m vocabdb init-db --db vocabulary.db
  python -m vocabdb import-anki anki_csv/target_1900_6th.txt --db vocabulary.db
  python -m vocabdb export-json --db vocabulary.db --output web/review/vocabulary.json
  python -m vocabdb serve-review
"""


def main() -> int:
    print(MESSAGE, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
