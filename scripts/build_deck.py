import pandas as pd
import yaml
from pathlib import Path

templates = Path("data/templates").glob("*.yaml")
cards = []

for t in templates:
    data = yaml.safe_load(open(t, encoding="utf-8"))

    for noun in data.get("variables", {}).get("noun", []):
        correct = data["correct"].format(noun=noun)

        for p in data["incorrect_patterns"]:
            for k, v in p.items():
                incorrect = v.format(noun=noun)

                cards.append({
                    "incorrect_sentence": incorrect,
                    "correct_sentence": correct,
                    "grammar_unit": data["metadata"]["grammar_unit"],
                    "difficulty": data["metadata"]["difficulty"],
                    "eiken": data["metadata"]["eiken"],
                })

df = pd.DataFrame(cards)
df.to_csv("generated.csv", index=False, encoding="utf-8-sig")
print("generated.csv created")
