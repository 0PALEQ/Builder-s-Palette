#!/usr/bin/env python3
"""Generate the 1.21+ item definition for every Builder's Palette item model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


NAMESPACE = "builders_palette"


def definition(model_id: str) -> str:
    value = {
        "model": {
            "type": "minecraft:model",
            "model": f"{NAMESPACE}:item/{model_id}",
        }
    }
    return json.dumps(value, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report missing or stale files without writing")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    assets = root / "src/main/resources/assets" / NAMESPACE
    models = assets / "models/item"
    definitions = assets / "items"
    expected: dict[Path, str] = {}

    for model in sorted(models.rglob("*.json")):
        model_id = model.relative_to(models).with_suffix("").as_posix()
        expected[definitions / f"{model_id}.json"] = definition(model_id)

    stale = [path for path, content in expected.items() if not path.is_file() or path.read_text(encoding="utf-8") != content]
    orphaned = sorted(path for path in definitions.rglob("*.json") if path not in expected)

    if args.check:
        for path in stale:
            print(f"missing-or-stale: {path.relative_to(root)}")
        for path in orphaned:
            print(f"orphaned: {path.relative_to(root)}")
        print(f"item models={len(expected)} missing-or-stale={len(stale)} orphaned={len(orphaned)}")
        return 1 if stale or orphaned else 0

    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected[path], encoding="utf-8", newline="\n")

    print(f"item models={len(expected)} written={len(stale)} orphaned={len(orphaned)}")
    return 1 if orphaned else 0


if __name__ == "__main__":
    raise SystemExit(main())
