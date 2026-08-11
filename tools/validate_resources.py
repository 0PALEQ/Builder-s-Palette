"""Validate Builder's Palette resource references for Minecraft 1.21.11."""

import json
import re
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "src/main/resources"
ASSETS = RESOURCES / "assets/builders_palette"
DATA = RESOURCES / "data/builders_palette"
JAVA = ROOT / "src/main/java/com/cookiecraftmods/builderspalette"
NAMESPACE = "builders_palette"


class Validation:
    def __init__(self):
        self.errors = []

    def require(self, condition, message):
        if not condition:
            self.errors.append(message)


def read_json(path, validation):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        validation.errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {error}")
        return None


def local_path(identifier, category, suffix=".json"):
    if ":" in identifier:
        namespace, path = identifier.split(":", 1)
    else:
        namespace, path = "minecraft", identifier
    if namespace != NAMESPACE:
        return None
    return ASSETS / category / f"{path}{suffix}"


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for entry in value:
            yield from strings(entry)
    elif isinstance(value, dict):
        for entry in value.values():
            yield from strings(entry)


def registered_ids(kind):
    source = (JAVA / "init" / f"BuildersPaletteMod{kind}.java").read_text(encoding="utf-8")
    ids = {
        match.group(1).lower()
        for match in re.finditer(rf"public static final RegistryObject<{kind[:-1]}>\s+([A-Z0-9_]+)\s*=", source)
    }
    generated = (JAVA / "init/GeneratedPastelConcrete.java").read_text(encoding="utf-8")
    for base in re.findall(r'registerFamily\("([a-z0-9_]+)"', generated):
        ids.update((base, f"{base}_stairs", f"{base}_slab", f"{base}_wall"))
    return ids


def validate_png(path, validation):
    data = path.read_bytes()
    validation.require(data.startswith(b"\x89PNG\r\n\x1a\n"), f"Invalid PNG signature: {path.relative_to(ROOT)}")
    if len(data) >= 24:
        width, height = struct.unpack(">II", data[16:24])
        validation.require(width > 0 and height > 0, f"Invalid PNG dimensions: {path.relative_to(ROOT)}")


def main():
    validation = Validation()
    json_files = list(RESOURCES.rglob("*.json"))
    parsed = {path: read_json(path, validation) for path in json_files}

    item_defs = {path.stem for path in (ASSETS / "items").glob("*.json")}
    item_models = {path.stem for path in (ASSETS / "models/item").glob("*.json")}
    blockstates = {path.stem for path in (ASSETS / "blockstates").glob("*.json")}
    block_loot = {path.stem for path in (DATA / "loot_table/blocks").glob("*.json")}
    expected_blocks = registered_ids("Blocks")
    expected_items = registered_ids("Items")

    validation.require(item_defs == item_models, "Item definition and item model file names differ")
    validation.require(blockstates == block_loot, "Blockstate and block loot-table file names differ")
    validation.require(blockstates == expected_blocks, f"Block resources differ from registrations: missing={sorted(expected_blocks - blockstates)}, extra={sorted(blockstates - expected_blocks)}")
    validation.require(item_defs == expected_items, f"Item resources differ from registrations: missing={sorted(expected_items - item_defs)}, extra={sorted(item_defs - expected_items)}")

    for path in (ASSETS / "items").glob("*.json"):
        data = parsed[path]
        if data is None:
            continue
        model = data.get("model", {})
        validation.require(model.get("type") == "minecraft:model", f"Unexpected item definition type: {path.relative_to(ROOT)}")
        target = local_path(model.get("model", ""), "models")
        validation.require(target is not None and target.is_file(), f"Missing item model referenced by {path.relative_to(ROOT)}")

    for path in (ASSETS / "blockstates").glob("*.json"):
        data = parsed[path]
        if data is None:
            continue
        for model_id in (value for value in strings(data) if ":block/" in value):
            target = local_path(model_id, "models")
            validation.require(target is None or target.is_file(), f"Missing block model {model_id} referenced by {path.relative_to(ROOT)}")

    for path in (ASSETS / "models").rglob("*.json"):
        data = parsed[path]
        if data is None:
            continue
        parent = data.get("parent")
        if parent:
            target = local_path(parent, "models")
            validation.require(target is None or target.is_file(), f"Missing parent model {parent} referenced by {path.relative_to(ROOT)}")
        for texture_id in data.get("textures", {}).values():
            if not isinstance(texture_id, str) or texture_id.startswith("#"):
                continue
            target = local_path(texture_id, "textures", ".png")
            validation.require(target is None or target.is_file(), f"Missing texture {texture_id} referenced by {path.relative_to(ROOT)}")

    languages = {}
    for language in ("en_us", "pl_pl"):
        path = ASSETS / f"lang/{language}.json"
        languages[language] = parsed[path] or {}
        for block_id in expected_blocks:
            validation.require(f"block.{NAMESPACE}.{block_id}" in languages[language], f"Missing {language} block name: {block_id}")
        for item_id in expected_items - expected_blocks:
            validation.require(f"item.{NAMESPACE}.{item_id}" in languages[language], f"Missing {language} item name: {item_id}")

    recipe_files = list((DATA / "recipe").rglob("*.json"))
    for path in recipe_files:
        data = parsed[path]
        if data is None:
            continue
        result = data.get("result", {})
        result_id = result.get("id") if isinstance(result, dict) else result
        if isinstance(result_id, str) and result_id.startswith(f"{NAMESPACE}:"):
            validation.require(result_id.split(":", 1)[1] in expected_items, f"Unknown recipe result {result_id} in {path.relative_to(ROOT)}")
        ingredient_values = []
        if "ingredient" in data:
            ingredient_values.append(data["ingredient"])
        ingredient_values.extend(data.get("ingredients", []))
        ingredient_values.extend(data.get("key", {}).values())
        for ingredient in ingredient_values:
            validation.require(not isinstance(ingredient, dict), f"Legacy ingredient object in {path.relative_to(ROOT)}")
            for identifier in strings(ingredient):
                if identifier.startswith(f"{NAMESPACE}:"):
                    validation.require(identifier.split(":", 1)[1] in expected_items, f"Unknown recipe ingredient {identifier} in {path.relative_to(ROOT)}")

    legacy_dirs = (
        DATA / "recipes",
        DATA / "loot_tables",
        RESOURCES / "data/minecraft/tags/blocks",
        RESOURCES / "data/minecraft/tags/items",
    )
    for path in legacy_dirs:
        validation.require(not path.exists(), f"Legacy 1.21.1 resource directory remains: {path.relative_to(ROOT)}")

    for path in RESOURCES.rglob("*.png"):
        validate_png(path, validation)
    validation.require((RESOURCES / "logo.png").is_file(), "Missing mod logo.png")
    metadata = (RESOURCES / "META-INF/neoforge.mods.toml").read_text(encoding="utf-8")
    logo_match = re.search(r'^logoFile="([^"]+)"', metadata, re.MULTILINE)
    validation.require(logo_match is not None and (RESOURCES / logo_match.group(1)).is_file(), "neoforge.mods.toml logoFile does not resolve")

    print(f"JSON files: {len(json_files)}")
    print(f"Registered/resources: {len(expected_blocks)} blocks, {len(expected_items)} items")
    print(f"Recipes: {len(recipe_files)}")
    print(f"PNG images: {len(list(RESOURCES.rglob('*.png')))}")
    if validation.errors:
        for error in validation.errors:
            print(f"ERROR: {error}")
        raise SystemExit(f"Resource validation failed with {len(validation.errors)} error(s).")
    print("All resource references validated successfully.")


if __name__ == "__main__":
    main()
