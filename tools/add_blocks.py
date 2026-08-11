#!/usr/bin/env python3
"""Generate compact block-family registrations and Minecraft resources.

The script intentionally uses only Python's standard library.  Its state file
records exactly which standalone files and tag/lang entries it owns, allowing
safe idempotent updates without touching legacy resources.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


NAMESPACE = "builders_palette"
ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
VALID_VARIANTS = {"block", "stairs", "slab", "wall"}
VALID_TOOLS = {"none", "pickaxe", "axe", "shovel", "hoe"}
VALID_SOUNDS = {
    "STONE",
    "WOOD",
    "GRAVEL",
    "SAND",
    "GLASS",
    "METAL",
    "WOOL",
    "SNOW",
    "NETHERITE",
    "NETHER_BRICKS",
    "CALCITE",
    "TUFF",
    "MUD",
    "MUD_BRICKS",
    "PACKED_MUD",
    "BAMBOO",
    "BAMBOO_WOOD",
    "CHERRY_WOOD",
}

JAVA_PATH = Path(
    "src/main/java/com/cookiecraftmods/builderspalette/init/GeneratedBlockFamilies.java"
)
LANG_PATH = Path(f"src/main/resources/assets/{NAMESPACE}/lang/en_us.json")
STATE_PATH = Path("tools/block_generator_state.json")
START_MARKER = "\t\t// GENERATED BLOCK FAMILIES START"
END_MARKER = "\t\t// GENERATED BLOCK FAMILIES END"


class GeneratorError(RuntimeError):
    pass


@dataclass(frozen=True)
class Family:
    block_id: str
    display_name: str
    variants: tuple[str, ...]
    sound: str
    hardness: float
    resistance: float
    requires_tool: bool
    tool: str
    render_type: str
    textures: dict[str, Path]

    @property
    def block_ids(self) -> list[str]:
        result = [self.block_id]
        for variant in ("stairs", "slab", "wall"):
            if variant in self.variants:
                result.append(f"{self.block_id}_{variant}")
        return result


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GeneratorError(f"Missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GeneratorError(f"Invalid JSON in {path}: {exc}") from exc


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def load_state(root: Path) -> dict[str, Any]:
    path = root / STATE_PATH
    if not path.exists():
        return {"schema_version": 1, "owned_files": [], "lang_keys": [], "tag_values": {}}
    state = read_json(path)
    if state.get("schema_version") != 1:
        raise GeneratorError(f"Unsupported generator state version in {path}")
    return state


def number(value: Any, field: str, family_id: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GeneratorError(f"{family_id}.{field} must be a number")
    result = float(value)
    if result < 0:
        raise GeneratorError(f"{family_id}.{field} cannot be negative")
    return result


def resolve_textures(raw: dict[str, Any], manifest_dir: Path, family_id: str) -> dict[str, Path]:
    if "texture" in raw and "textures" in raw:
        raise GeneratorError(f"{family_id} must use either 'texture' or 'textures', not both")

    if "texture" in raw:
        texture = raw["texture"]
        if not isinstance(texture, str) or not texture.strip():
            raise GeneratorError(f"{family_id}.texture must be a non-empty path")
        values = {"all": texture}
    else:
        values = raw.get("textures")
        if not isinstance(values, dict):
            raise GeneratorError(f"{family_id} requires 'texture' or a 'textures' object")
        keys = set(values)
        if keys != {"side", "top", "bottom"}:
            raise GeneratorError(
                f"{family_id}.textures must contain exactly side, top, and bottom"
            )

    result: dict[str, Path] = {}
    for key, value in values.items():
        if not isinstance(value, str) or not value.strip():
            raise GeneratorError(f"{family_id}.textures.{key} must be a non-empty path")
        path = Path(value)
        if not path.is_absolute():
            path = manifest_dir / path
        result[key] = path.resolve()
    return result


def validate_png(path: Path, label: str) -> bytes:
    try:
        data = path.read_bytes()
    except FileNotFoundError as exc:
        raise GeneratorError(f"Texture for {label} does not exist: {path}") from exc
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise GeneratorError(f"Texture for {label} is not a valid PNG: {path}")
    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        raise GeneratorError(f"Texture for {label} has invalid dimensions: {path}")
    return data


def load_manifest(path: Path) -> list[Family]:
    raw = read_json(path)
    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise GeneratorError("Manifest must be an object with schema_version 1")
    entries = raw.get("families")
    if not isinstance(entries, list):
        raise GeneratorError("Manifest 'families' must be an array")

    families: list[Family] = []
    used_ids: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise GeneratorError(f"families[{index}] must be an object")
        block_id = entry.get("id")
        if not isinstance(block_id, str) or not ID_PATTERN.fullmatch(block_id):
            raise GeneratorError(
                f"families[{index}].id must be a lowercase snake_case Minecraft identifier"
            )
        display_name = entry.get("display_name")
        if not isinstance(display_name, str) or not display_name.strip():
            raise GeneratorError(f"{block_id}.display_name must be non-empty")

        variants_raw = entry.get("variants", ["block"])
        if not isinstance(variants_raw, list) or not variants_raw:
            raise GeneratorError(f"{block_id}.variants must be a non-empty array")
        variants = tuple(variants_raw)
        if any(not isinstance(item, str) for item in variants):
            raise GeneratorError(f"{block_id}.variants must contain strings")
        unknown = set(variants) - VALID_VARIANTS
        if unknown:
            raise GeneratorError(f"{block_id}.variants contains unsupported values: {sorted(unknown)}")
        if "block" not in variants:
            raise GeneratorError(f"{block_id}.variants must include 'block'")
        if len(set(variants)) != len(variants):
            raise GeneratorError(f"{block_id}.variants contains duplicates")

        sound = entry.get("sound", "STONE")
        if sound not in VALID_SOUNDS:
            raise GeneratorError(f"{block_id}.sound must be one of {sorted(VALID_SOUNDS)}")
        tool = entry.get("tool", "pickaxe")
        if tool not in VALID_TOOLS:
            raise GeneratorError(f"{block_id}.tool must be one of {sorted(VALID_TOOLS)}")
        requires_tool = entry.get("requires_tool", True)
        if not isinstance(requires_tool, bool):
            raise GeneratorError(f"{block_id}.requires_tool must be true or false")
        if requires_tool and tool == "none":
            raise GeneratorError(f"{block_id} requires a tool but tool is 'none'")
        render_type = entry.get("render_type", "solid")
        if render_type != "solid":
            raise GeneratorError(
                f"{block_id}.render_type currently supports only 'solid'; transparent blocks need client setup"
            )

        family = Family(
            block_id=block_id,
            display_name=display_name.strip(),
            variants=variants,
            sound=sound,
            hardness=number(entry.get("hardness", 1.5), "hardness", block_id),
            resistance=number(entry.get("resistance", 6.0), "resistance", block_id),
            requires_tool=requires_tool,
            tool=tool,
            render_type=render_type,
            textures=resolve_textures(entry, path.parent, block_id),
        )
        for generated_id in family.block_ids:
            if generated_id in used_ids:
                raise GeneratorError(f"Duplicate generated block id: {generated_id}")
            used_ids.add(generated_id)
        families.append(family)
    return families


def replace_strings(value: Any, old: str, new: str) -> Any:
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [replace_strings(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item, old, new) for key, item in value.items()}
    return value


def variant_blockstate(root: Path, variant: str, block_id: str) -> dict[str, Any]:
    template = root / f"src/main/resources/assets/{NAMESPACE}/blockstates/blue_bricks_{variant}.json"
    data = read_json(template)
    return replace_strings(
        data,
        f"{NAMESPACE}:block/blue_bricks",
        f"{NAMESPACE}:block/{block_id}",
    )


def texture_outputs(family: Family, resource_root: Path) -> tuple[dict[Path, bytes], dict[str, str]]:
    outputs: dict[Path, bytes] = {}
    refs: dict[str, str] = {}
    if "all" in family.textures:
        destination = resource_root / "textures/block" / f"{family.block_id}.png"
        outputs[destination] = validate_png(family.textures["all"], family.block_id)
        ref = f"{NAMESPACE}:block/{family.block_id}"
        refs = {"all": ref, "side": ref, "top": ref, "bottom": ref, "particle": ref}
    else:
        for key in ("side", "top", "bottom"):
            destination = resource_root / "textures/block" / f"{family.block_id}_{key}.png"
            outputs[destination] = validate_png(family.textures[key], f"{family.block_id}.{key}")
            refs[key] = f"{NAMESPACE}:block/{family.block_id}_{key}"
        refs["particle"] = refs["side"]
    return outputs, refs


def model(parent: str, textures: dict[str, str], render_type: str) -> dict[str, Any]:
    return {"parent": parent, "textures": textures, "render_type": render_type}


def self_drop(block_id: str) -> dict[str, Any]:
    full_id = f"{NAMESPACE}:{block_id}"
    return {
        "type": "minecraft:block",
        "random_sequence": f"{NAMESPACE}:blocks/{block_id}",
        "pools": [
            {
                "rolls": 1.0,
                "conditions": [{"condition": "minecraft:survives_explosion"}],
                "entries": [{"type": "minecraft:item", "name": full_id}],
            }
        ],
    }


def add_json_output(outputs: dict[Path, bytes], path: Path, value: Any) -> None:
    outputs[path] = json_bytes(value)


def family_outputs(root: Path, family: Family) -> dict[Path, bytes]:
    resources = root / "src/main/resources"
    assets = resources / f"assets/{NAMESPACE}"
    data = resources / f"data/{NAMESPACE}"
    outputs, refs = texture_outputs(family, assets)

    blockstates = assets / "blockstates"
    block_models = assets / "models/block"
    item_models = assets / "models/item"
    item_defs = assets / "items"
    loot = data / "loot_table/blocks"
    block_id = family.block_id

    if "all" in family.textures:
        base_model = model(
            "block/cube_all",
            {"all": refs["all"], "particle": refs["particle"]},
            family.render_type,
        )
    else:
        base_model = model(
            "block/cube_bottom_top",
            {
                "bottom": refs["bottom"],
                "top": refs["top"],
                "side": refs["side"],
                "particle": refs["particle"],
            },
            family.render_type,
        )

    add_json_output(outputs, blockstates / f"{block_id}.json", {
        "variants": {"": {"model": f"{NAMESPACE}:block/{block_id}"}}
    })
    add_json_output(outputs, block_models / f"{block_id}.json", base_model)
    add_json_output(outputs, item_models / f"{block_id}.json", {
        "parent": f"{NAMESPACE}:block/{block_id}"
    })
    add_json_output(outputs, item_defs / f"{block_id}.json", {
        "model": {"type": "minecraft:model", "model": f"{NAMESPACE}:item/{block_id}"}
    })
    add_json_output(outputs, loot / f"{block_id}.json", self_drop(block_id))

    shape_textures = {
        "particle": refs["particle"],
        "bottom": refs["bottom"],
        "top": refs["top"],
        "side": refs["side"],
    }
    if "stairs" in family.variants:
        shape_id = f"{block_id}_stairs"
        add_json_output(outputs, blockstates / f"{shape_id}.json", variant_blockstate(root, "stairs", block_id))
        for suffix, parent in (("", "block/stairs"), ("_inner", "block/inner_stairs"), ("_outer", "block/outer_stairs")):
            add_json_output(outputs, block_models / f"{shape_id}{suffix}.json", model(parent, shape_textures, family.render_type))
        add_json_output(outputs, item_models / f"{shape_id}.json", {"parent": f"{NAMESPACE}:block/{shape_id}"})
        add_json_output(outputs, item_defs / f"{shape_id}.json", {
            "model": {"type": "minecraft:model", "model": f"{NAMESPACE}:item/{shape_id}"}
        })
        add_json_output(outputs, loot / f"{shape_id}.json", self_drop(shape_id))

    if "slab" in family.variants:
        shape_id = f"{block_id}_slab"
        add_json_output(outputs, blockstates / f"{shape_id}.json", variant_blockstate(root, "slab", block_id))
        for suffix, parent in (("", "block/slab"), ("_top", "block/slab_top"), ("_full", "block/cube_bottom_top")):
            add_json_output(outputs, block_models / f"{shape_id}{suffix}.json", model(parent, shape_textures, family.render_type))
        add_json_output(outputs, item_models / f"{shape_id}.json", {"parent": f"{NAMESPACE}:block/{shape_id}"})
        add_json_output(outputs, item_defs / f"{shape_id}.json", {
            "model": {"type": "minecraft:model", "model": f"{NAMESPACE}:item/{shape_id}"}
        })
        add_json_output(outputs, loot / f"{shape_id}.json", self_drop(shape_id))

    if "wall" in family.variants:
        shape_id = f"{block_id}_wall"
        add_json_output(outputs, blockstates / f"{shape_id}.json", variant_blockstate(root, "wall", block_id))
        wall_textures = {"wall": refs["side"], "particle": refs["particle"]}
        for suffix, parent in (
            ("", "block/template_wall_side"),
            ("_post", "block/template_wall_post"),
            ("_side_tall", "block/template_wall_side_tall"),
            ("_inventory", "block/wall_inventory"),
        ):
            add_json_output(outputs, block_models / f"{shape_id}{suffix}.json", model(parent, wall_textures, family.render_type))
        add_json_output(outputs, item_models / f"{shape_id}.json", {
            "parent": f"{NAMESPACE}:block/{shape_id}_inventory"
        })
        add_json_output(outputs, item_defs / f"{shape_id}.json", {
            "model": {"type": "minecraft:model", "model": f"{NAMESPACE}:item/{shape_id}"}
        })
        add_json_output(outputs, loot / f"{shape_id}.json", self_drop(shape_id))

    return outputs


def java_float(value: float) -> str:
    text = format(value, ".9g")
    if "." not in text and "e" not in text.lower():
        text += ".0"
    return text + "f"


def generated_java(root: Path, families: list[Family]) -> bytes:
    path = root / JAVA_PATH
    source = path.read_text(encoding="utf-8")
    if source.count(START_MARKER) != 1 or source.count(END_MARKER) != 1:
        raise GeneratorError(f"Generated markers are missing or duplicated in {path}")
    statements = []
    for family in families:
        statements.append(
            "\t\tregisterFamily("
            f'"{family.block_id}", {java_float(family.hardness)}, {java_float(family.resistance)}, '
            f"BlockSoundGroup.{family.sound}, {str(family.requires_tool).lower()}, "
            f"{str('stairs' in family.variants).lower()}, "
            f"{str('slab' in family.variants).lower()}, "
            f"{str('wall' in family.variants).lower()});"
        )
    middle = "\n".join(statements)
    replacement = START_MARKER + ("\n" + middle if middle else "") + "\n" + END_MARKER
    before, remainder = source.split(START_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    return (before + replacement + after).encode("utf-8")


def tag_additions(families: Iterable[Family]) -> dict[Path, list[str]]:
    result: dict[Path, list[str]] = {}

    def add(path: str, block_id: str) -> None:
        result.setdefault(Path(path), []).append(f"{NAMESPACE}:{block_id}")

    for family in families:
        if family.tool != "none":
            for block_id in family.block_ids:
                add(f"src/main/resources/data/minecraft/tags/block/mineable/{family.tool}.json", block_id)
        for variant, plural in (("stairs", "stairs"), ("slab", "slabs"), ("wall", "walls")):
            if variant in family.variants:
                block_id = f"{family.block_id}_{variant}"
                add(f"src/main/resources/data/minecraft/tags/block/{plural}.json", block_id)
                add(f"src/main/resources/data/minecraft/tags/item/{plural}.json", block_id)
    return result


def updated_lang(root: Path, families: list[Family], old_keys: set[str]) -> tuple[bytes, list[str]]:
    data = read_json(root / LANG_PATH)
    if not isinstance(data, dict):
        raise GeneratorError(f"{root / LANG_PATH} must contain a JSON object")
    for key in old_keys:
        data.pop(key, None)

    keys: list[str] = []
    suffix_names = {"stairs": "Stairs", "slab": "Slab", "wall": "Wall"}
    for family in families:
        entries = [(family.block_id, family.display_name)]
        for variant in ("stairs", "slab", "wall"):
            if variant in family.variants:
                entries.append((f"{family.block_id}_{variant}", f"{family.display_name} {suffix_names[variant]}"))
        for block_id, display_name in entries:
            key = f"block.{NAMESPACE}.{block_id}"
            if key in data:
                raise GeneratorError(f"Language key already exists and is not generator-owned: {key}")
            data[key] = display_name
            keys.append(key)
    return json_bytes(data), keys


def updated_tags(
    root: Path,
    additions: dict[Path, list[str]],
    old_values: dict[str, list[str]],
) -> tuple[dict[Path, bytes], dict[str, list[str]]]:
    all_paths = set(additions) | {Path(path) for path in old_values}
    outputs: dict[Path, bytes] = {}
    state_values: dict[str, list[str]] = {}
    for relative in sorted(all_paths, key=str):
        path = root / relative
        if path.exists():
            data = read_json(path)
            if not isinstance(data, dict) or not isinstance(data.get("values"), list):
                raise GeneratorError(f"Tag file has an unsupported structure: {path}")
        else:
            data = {"replace": False, "values": []}
        old = set(old_values.get(relative.as_posix(), old_values.get(str(relative), [])))
        values = [value for value in data["values"] if value not in old]
        for value in additions.get(relative, []):
            if value in values:
                raise GeneratorError(f"Tag value already exists and is not generator-owned: {relative}: {value}")
            values.append(value)
        data["values"] = values
        outputs[path] = json_bytes(data)
        if additions.get(relative):
            state_values[relative.as_posix()] = additions[relative]
    return outputs, state_values


def relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise GeneratorError(f"Refusing to manage a file outside the project: {path}") from exc


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def build_plan(root: Path, manifest: Path) -> tuple[dict[Path, bytes], set[Path], dict[str, Any]]:
    state = load_state(root)
    families = load_manifest(manifest)
    previous_owned = {root / Path(path) for path in state.get("owned_files", [])}

    owned_outputs: dict[Path, bytes] = {}
    for family in families:
        for path, data in family_outputs(root, family).items():
            if path in owned_outputs:
                raise GeneratorError(f"Two generated outputs target the same file: {path}")
            owned_outputs[path] = data

    for path in owned_outputs:
        if path.exists() and path not in previous_owned:
            raise GeneratorError(f"Refusing to overwrite a file not owned by the generator: {path}")

    lang_data, lang_keys = updated_lang(root, families, set(state.get("lang_keys", [])))
    additions = tag_additions(families)
    tag_data, tag_state = updated_tags(root, additions, state.get("tag_values", {}))

    outputs = dict(owned_outputs)
    outputs[root / JAVA_PATH] = generated_java(root, families)
    if families or state.get("lang_keys"):
        outputs[root / LANG_PATH] = lang_data
    outputs.update(tag_data)

    new_state = {
        "schema_version": 1,
        "owned_files": sorted(relative_to_root(path, root) for path in owned_outputs),
        "lang_keys": sorted(lang_keys),
        "tag_values": {key: tag_state[key] for key in sorted(tag_state)},
    }
    outputs[root / STATE_PATH] = json_bytes(new_state)
    stale = previous_owned - set(owned_outputs)
    return outputs, stale, new_state


def changed(path: Path, expected: bytes) -> bool:
    try:
        return path.read_bytes() != expected
    except FileNotFoundError:
        return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "manifest",
        nargs="?",
        type=Path,
        help="JSON manifest (default: tools/block_families.json)",
    )
    parser.add_argument("--project-root", type=Path, help=argparse.SUPPRESS)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="validate and show changes without writing")
    mode.add_argument("--check", action="store_true", help="fail if generated outputs are not current")
    args = parser.parse_args(argv)

    root = (args.project_root or Path(__file__).resolve().parents[1]).resolve()
    manifest = args.manifest or (root / "tools/block_families.json")
    if not manifest.is_absolute():
        manifest = (Path.cwd() / manifest).resolve()

    try:
        outputs, stale, _ = build_plan(root, manifest)
    except GeneratorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    modifications = sorted((path for path, data in outputs.items() if changed(path, data)), key=str)
    stale_existing = sorted((path for path in stale if path.exists()), key=str)

    if args.check:
        if modifications or stale_existing:
            for path in modifications:
                print(f"outdated: {relative_to_root(path, root)}")
            for path in stale_existing:
                print(f"stale: {relative_to_root(path, root)}")
            return 1
        print("Generated block files are up to date.")
        return 0

    if args.dry_run:
        for path in modifications:
            print(f"would write: {relative_to_root(path, root)}")
        for path in stale_existing:
            print(f"would remove: {relative_to_root(path, root)}")
        if not modifications and not stale_existing:
            print("No changes required.")
        return 0

    for path in stale_existing:
        relative_to_root(path, root)
        path.unlink()
    for path, data in outputs.items():
        if changed(path, data):
            atomic_write(path, data)

    print(f"Generated {len(outputs) - 2} managed resource/tag files for {len(load_manifest(manifest))} block families.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
