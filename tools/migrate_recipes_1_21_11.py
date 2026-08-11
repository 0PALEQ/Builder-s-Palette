#!/usr/bin/env python3
"""Migrate and validate Builder's Palette recipes for Minecraft 1.21.11."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def basic_ingredient(value: object, owner: Path) -> object:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return [basic_ingredient(entry, owner) for entry in value]
    if isinstance(value, dict) and set(value) == {"item"} and isinstance(value["item"], str):
        return value["item"]
    if isinstance(value, dict) and set(value) == {"tag"} and isinstance(value["tag"], str):
        return f"#{value['tag']}"
    raise ValueError(f"Unsupported ingredient in {owner}: {value!r}")


def migrate(recipe: dict[str, object], owner: Path) -> dict[str, object]:
    if "ingredient" in recipe:
        recipe["ingredient"] = basic_ingredient(recipe["ingredient"], owner)
    if "ingredients" in recipe:
        ingredients = recipe["ingredients"]
        if not isinstance(ingredients, list):
            raise ValueError(f"ingredients must be a list in {owner}")
        recipe["ingredients"] = [basic_ingredient(value, owner) for value in ingredients]
    if "key" in recipe:
        key = recipe["key"]
        if not isinstance(key, dict):
            raise ValueError(f"key must be an object in {owner}")
        recipe["key"] = {symbol: basic_ingredient(value, owner) for symbol, value in key.items()}

    result = recipe.get("result")
    if not isinstance(result, dict) or not isinstance(result.get("id"), str):
        raise ValueError(f"result.id is required in {owner}")
    return recipe


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    recipes = root / "src/main/resources/data/builders_palette/recipe"
    stale: list[tuple[Path, str]] = []

    for path in sorted(recipes.rglob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"Recipe root must be an object: {path}")
        content = json.dumps(migrate(value, path), indent=2) + "\n"
        if path.read_text(encoding="utf-8") != content:
            stale.append((path, content))

    if args.check:
        for path, _ in stale:
            print(f"missing-or-stale: {path.relative_to(root)}")
        print(f"recipes={sum(1 for _ in recipes.rglob('*.json'))} missing-or-stale={len(stale)}")
        return 1 if stale else 0

    for path, content in stale:
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"recipes={sum(1 for _ in recipes.rglob('*.json'))} written={len(stale)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
