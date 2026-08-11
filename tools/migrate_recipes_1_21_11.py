"""Migrate legacy recipe ingredient objects to the Minecraft 1.21.11 format."""

import json
from pathlib import Path


RECIPE_ROOT = Path("src/main/resources/data/builders_palette/recipe")


def migrate_ingredient(value):
    if isinstance(value, dict):
        if set(value) == {"item"}:
            return value["item"]
        if set(value) == {"tag"}:
            return "#" + value["tag"]
    if isinstance(value, list):
        return [migrate_ingredient(entry) for entry in value]
    return value


def main():
    changed = 0
    for path in RECIPE_ROOT.rglob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        before = json.dumps(data, sort_keys=True)

        if "ingredient" in data:
            data["ingredient"] = migrate_ingredient(data["ingredient"])
        if "ingredients" in data:
            data["ingredients"] = [migrate_ingredient(entry) for entry in data["ingredients"]]
        if "key" in data:
            data["key"] = {
                symbol: migrate_ingredient(value) for symbol, value in data["key"].items()
            }

        if before != json.dumps(data, sort_keys=True):
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            changed += 1

    print(f"Migrated {changed} recipe files.")


if __name__ == "__main__":
    main()
