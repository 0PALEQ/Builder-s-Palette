#!/usr/bin/env python3
"""Generate the ten-color pastel concrete collection and all block shapes."""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT / "src/main/resources"
ASSETS = RESOURCES / "assets/builders_palette"
DATA = RESOURCES / "data"
JAVA = ROOT / "src/main/java/com/cookiecraftmods/builderspalette/init/GeneratedPastelConcrete.java"
STATE = ROOT / "tools/pastel_concrete_generator_state.json"
NAMESPACE = "builders_palette"

# The target RGB value is the average body color; template shading is retained.
COLORS = (
    ("rose", "Rose", "#DDA6B7", "pink_dye"),
    ("coral", "Coral", "#E3A093", "red_dye"),
    ("peach", "Peach", "#E8B58F", "orange_dye"),
    ("butter", "Butter", "#E5D99B", "yellow_dye"),
    ("sage", "Sage", "#B5C49A", "green_dye"),
    ("mint", "Mint", "#9FD0B5", "lime_dye"),
    ("aqua", "Aqua", "#9DCECB", "cyan_dye"),
    ("sky", "Sky", "#A6C9E3", "light_blue_dye"),
    ("periwinkle", "Periwinkle", "#A9B5DE", "blue_dye"),
    ("lavender", "Lavender", "#C4AAD9", "purple_dye"),
)

TEMPLATES = {
    "smooth": "whiteconcrete.png",
    "bricks": "white_terracotta_bricks.png",
    "packed": "packed_white_terracotta_bricks.png",
    "pillar_side": "white_terracotta_pillar_side.png",
    "pillar_top": "white_terracotta_pillar_top.png",
}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def rgb(hex_color: str) -> tuple[int, int, int]:
    value = hex_color.removeprefix("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def recolor(template_name: str, target: tuple[int, int, int]) -> bytes:
    path = ASSETS / "textures/block" / template_name
    with Image.open(path) as source:
        image = source.convert("RGBA")
        pixels = [image.getpixel((x, y)) for y in range(image.height) for x in range(image.width)]
        luminances = [(54 * r + 183 * g + 19 * b) / 256 for r, g, b, a in pixels if a]
        average = sum(luminances) / len(luminances)
        output = []
        for red, green, blue, alpha in pixels:
            luminance = (54 * red + 183 * green + 19 * blue) / 256
            delta = (luminance - average) * 0.9
            output.append(tuple(max(0, min(255, round(channel + delta))) for channel in target) + (alpha,))
        image.putdata(output)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()


def block_ids(base_id: str) -> tuple[str, str, str, str]:
    return base_id, f"{base_id}_stairs", f"{base_id}_slab", f"{base_id}_wall"


def replace_strings(value: object, old: str, new: str) -> object:
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [replace_strings(item, old, new) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item, old, new) for key, item in value.items()}
    return value


def shape_blockstate(shape: str, base_id: str) -> object:
    template = ASSETS / f"blockstates/blue_bricks_{shape}.json"
    value = json.loads(template.read_text(encoding="utf-8"))
    return replace_strings(value, f"{NAMESPACE}:block/blue_bricks", f"{NAMESPACE}:block/{base_id}")


def model(parent: str, textures: dict[str, str]) -> dict:
    return {"parent": parent, "textures": textures, "render_type": "solid"}


def self_drop(block_id: str) -> dict:
    return {
        "type": "minecraft:block",
        "random_sequence": f"{NAMESPACE}:blocks/{block_id}",
        "pools": [
            {
                "rolls": 1,
                "bonus_rolls": 0,
                "conditions": [{"condition": "minecraft:survives_explosion"}],
                "entries": [{"type": "minecraft:item", "name": f"{NAMESPACE}:{block_id}"}],
            }
        ],
    }


def item_definition(block_id: str) -> dict:
    return {"model": {"type": "minecraft:model", "model": f"{NAMESPACE}:item/{block_id}"}}


def shaped(pattern: list[str], key: dict, result: str, count: int) -> dict:
    return {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "pattern": pattern,
        "key": key,
        "result": {"item": result, "count": count},
        "show_notification": True,
    }


def add_family_resources(outputs: dict[Path, bytes], base_id: str, pillar: bool) -> None:
    blockstates = ASSETS / "blockstates"
    block_models = ASSETS / "models/block"
    item_models = ASSETS / "models/item"
    item_defs = ASSETS / "items"
    loot = DATA / f"{NAMESPACE}/loot_tables/blocks"

    if pillar:
        side = f"{NAMESPACE}:block/{base_id}_side"
        top = f"{NAMESPACE}:block/{base_id}_top"
        outputs[blockstates / f"{base_id}.json"] = json_bytes({
            "variants": {
                "axis=x": {"model": f"{NAMESPACE}:block/{base_id}", "x": 90, "y": 90},
                "axis=y": {"model": f"{NAMESPACE}:block/{base_id}"},
                "axis=z": {"model": f"{NAMESPACE}:block/{base_id}", "x": 90},
            }
        })
        outputs[block_models / f"{base_id}.json"] = json_bytes(
            model("minecraft:block/cube_column", {"end": top, "side": side, "particle": side})
        )
        shape_textures = {"particle": side, "bottom": top, "top": top, "side": side}
        wall_texture = side
    else:
        texture = f"{NAMESPACE}:block/{base_id}"
        outputs[blockstates / f"{base_id}.json"] = json_bytes(
            {"variants": {"": {"model": f"{NAMESPACE}:block/{base_id}"}}}
        )
        outputs[block_models / f"{base_id}.json"] = json_bytes(
            model("minecraft:block/cube_all", {"all": texture, "particle": texture})
        )
        shape_textures = {"particle": texture, "bottom": texture, "top": texture, "side": texture}
        wall_texture = texture

    outputs[item_models / f"{base_id}.json"] = json_bytes({"parent": f"{NAMESPACE}:block/{base_id}"})
    outputs[item_defs / f"{base_id}.json"] = json_bytes(item_definition(base_id))
    outputs[loot / f"{base_id}.json"] = json_bytes(self_drop(base_id))

    stairs = f"{base_id}_stairs"
    outputs[blockstates / f"{stairs}.json"] = json_bytes(shape_blockstate("stairs", base_id))
    for suffix, parent in (("", "minecraft:block/stairs"), ("_inner", "minecraft:block/inner_stairs"), ("_outer", "minecraft:block/outer_stairs")):
        outputs[block_models / f"{stairs}{suffix}.json"] = json_bytes(model(parent, shape_textures))
    outputs[item_models / f"{stairs}.json"] = json_bytes({"parent": f"{NAMESPACE}:block/{stairs}"})
    outputs[item_defs / f"{stairs}.json"] = json_bytes(item_definition(stairs))
    outputs[loot / f"{stairs}.json"] = json_bytes(self_drop(stairs))

    slab = f"{base_id}_slab"
    outputs[blockstates / f"{slab}.json"] = json_bytes(shape_blockstate("slab", base_id))
    for suffix, parent in (("", "minecraft:block/slab"), ("_top", "minecraft:block/slab_top"), ("_full", "minecraft:block/cube_bottom_top")):
        outputs[block_models / f"{slab}{suffix}.json"] = json_bytes(model(parent, shape_textures))
    outputs[item_models / f"{slab}.json"] = json_bytes({"parent": f"{NAMESPACE}:block/{slab}"})
    outputs[item_defs / f"{slab}.json"] = json_bytes(item_definition(slab))
    outputs[loot / f"{slab}.json"] = json_bytes(self_drop(slab))

    wall = f"{base_id}_wall"
    outputs[blockstates / f"{wall}.json"] = json_bytes(shape_blockstate("wall", base_id))
    wall_textures = {"wall": wall_texture, "particle": wall_texture}
    for suffix, parent in (("", "minecraft:block/template_wall_side"), ("_post", "minecraft:block/template_wall_post"), ("_side_tall", "minecraft:block/template_wall_side_tall"), ("_inventory", "minecraft:block/wall_inventory")):
        outputs[block_models / f"{wall}{suffix}.json"] = json_bytes(model(parent, wall_textures))
    outputs[item_models / f"{wall}.json"] = json_bytes({"parent": f"{NAMESPACE}:block/{wall}_inventory"})
    outputs[item_defs / f"{wall}.json"] = json_bytes(item_definition(wall))
    outputs[loot / f"{wall}.json"] = json_bytes(self_drop(wall))


def add_shape_recipes(outputs: dict[Path, bytes], base_id: str) -> None:
    recipes = DATA / f"{NAMESPACE}/recipes"
    ingredient = {"item": f"{NAMESPACE}:{base_id}"}
    outputs[recipes / f"{base_id}_stairs.json"] = json_bytes(
        shaped(["#  ", "## ", "###"], {"#": ingredient}, f"{NAMESPACE}:{base_id}_stairs", 4)
    )
    outputs[recipes / f"{base_id}_slab.json"] = json_bytes(
        shaped(["###"], {"#": ingredient}, f"{NAMESPACE}:{base_id}_slab", 6)
    )
    outputs[recipes / f"{base_id}_wall.json"] = json_bytes(
        shaped(["###", "###"], {"#": ingredient}, f"{NAMESPACE}:{base_id}_wall", 6)
    )


def generated_java(families: list[tuple[str, bool]]) -> bytes:
    statements = "\n".join(
        f'\t\tregisterFamily("{base_id}", {str(pillar).lower()});' for base_id, pillar in families
    )
    source = f'''package com.cookiecraftmods.builderspalette.init;

import net.minecraft.block.AbstractBlock;
import net.minecraft.block.Block;
import net.minecraft.block.PillarBlock;
import net.minecraft.block.SlabBlock;
import net.minecraft.block.StairsBlock;
import net.minecraft.block.WallBlock;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.registry.Registries;
import net.minecraft.sound.BlockSoundGroup;

import java.util.ArrayList;
import java.util.List;

/** Generated by tools/generate_pastel_concrete.py. */
public final class GeneratedPastelConcrete {{
\tprivate static final List<RegistryObject<Block>> BLOCKS = new ArrayList<>();
\tprivate static boolean blocksRegistered;
\tprivate static boolean itemsRegistered;

\tprivate GeneratedPastelConcrete() {{
\t}}

\tpublic static void registerBlocks() {{
\t\tif (blocksRegistered) return;
\t\tblocksRegistered = true;
{statements}
\t}}

\tpublic static void registerItems() {{
\t\tif (itemsRegistered) return;
\t\tif (!blocksRegistered) throw new IllegalStateException("Pastel concrete blocks must be registered before their items");
\t\titemsRegistered = true;
\t\tfor (RegistryObject<Block> block : BLOCKS) {{
\t\t\tRegistryObject.register(Registries.ITEM, block.getId().getPath(),
\t\t\t\t\t() -> new BlockItem(block.get(), new Item.Settings()));
\t\t}}
\t}}

\tpublic static void addToTab(ItemGroup.Entries entries) {{
\t\tfor (RegistryObject<Block> block : BLOCKS) entries.add(block.get().asItem());
\t}}

\tprivate static void registerFamily(String name, boolean pillar) {{
\t\tRegistryObject<Block> base = pillar
\t\t\t\t? register(name, () -> new PillarBlock(settings()))
\t\t\t\t: register(name, () -> new Block(settings()));
\t\tregister(name + "_stairs", () -> new StairsBlock(base.get().getDefaultState(), AbstractBlock.Settings.copy(base.get())));
\t\tregister(name + "_slab", () -> new SlabBlock(AbstractBlock.Settings.copy(base.get())));
\t\tregister(name + "_wall", () -> new WallBlock(AbstractBlock.Settings.copy(base.get())));
\t}}

\tprivate static AbstractBlock.Settings settings() {{
\t\treturn AbstractBlock.Settings.create().sounds(BlockSoundGroup.STONE).strength(1.8f, 6.0f).requiresTool();
\t}}

\tprivate static RegistryObject<Block> register(String name, java.util.function.Supplier<? extends Block> supplier) {{
\t\tRegistryObject<Block> block = RegistryObject.register(Registries.BLOCK, name, supplier);
\t\tBLOCKS.add(block);
\t\treturn block;
\t}}
}}
'''
    return source.encode("utf-8")


def update_shared_json(outputs: dict[Path, bytes], state: dict, lang_entries: dict[str, str], tags: dict[Path, list[str]]) -> None:
    old_keys = set(state.get("lang_keys", []))
    for language in ("en_us", "pl_pl"):
        path = ASSETS / f"lang/{language}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in old_keys:
            data.pop(key, None)
        for key, value in lang_entries.items():
            if key in data and key not in old_keys:
                raise RuntimeError(f"Refusing to overwrite unmanaged language key: {key}")
            data[key] = value
        outputs[path] = json_bytes(data)

    old_tags = state.get("tag_values", {})
    all_paths = set(tags) | {ROOT / path for path in old_tags}
    for path in all_paths:
        data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"replace": False, "values": []}
        old_values = set(old_tags.get(path.relative_to(ROOT).as_posix(), []))
        values = [value for value in data["values"] if value not in old_values]
        for value in tags.get(path, []):
            if value in values:
                raise RuntimeError(f"Refusing to duplicate unmanaged tag entry: {value}")
            values.append(value)
        data["values"] = values
        outputs[path] = json_bytes(data)


def build_plan() -> tuple[dict[Path, bytes], set[Path], dict]:
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    outputs: dict[Path, bytes] = {}
    owned: set[Path] = {JAVA}
    families: list[tuple[str, bool]] = []
    lang: dict[str, str] = {}
    tags: dict[Path, list[str]] = {}

    def tag(relative: str, block_id: str) -> None:
        tags.setdefault(ROOT / relative, []).append(f"{NAMESPACE}:{block_id}")

    for color_id, display, hex_color, dye in COLORS:
        target = rgb(hex_color)
        prefix = f"pastel_{color_id}"
        smooth = f"{prefix}_smooth_concrete"
        bricks = f"{prefix}_concrete_bricks"
        packed = f"{prefix}_packed_concrete_bricks"
        pillar = f"{prefix}_concrete_pillar"
        definitions = (
            (smooth, f"Pastel {display} Smooth Concrete", False),
            (bricks, f"Pastel {display} Concrete Bricks", False),
            (packed, f"Pastel {display} Packed Concrete Bricks", False),
            (pillar, f"Pastel {display} Concrete Pillar", True),
        )

        texture_outputs = {
            ASSETS / f"textures/block/{smooth}.png": recolor(TEMPLATES["smooth"], target),
            ASSETS / f"textures/block/{bricks}.png": recolor(TEMPLATES["bricks"], target),
            ASSETS / f"textures/block/{packed}.png": recolor(TEMPLATES["packed"], target),
            ASSETS / f"textures/block/{pillar}_side.png": recolor(TEMPLATES["pillar_side"], target),
            ASSETS / f"textures/block/{pillar}_top.png": recolor(TEMPLATES["pillar_top"], target),
        }
        outputs.update(texture_outputs)
        owned.update(texture_outputs)

        recipes = DATA / f"{NAMESPACE}/recipes"
        outputs[recipes / f"{smooth}.json"] = json_bytes(shaped(
            ["###", "#D#", "###"],
            {"#": {"item": "minecraft:white_concrete"}, "D": {"item": f"minecraft:{dye}"}},
            f"{NAMESPACE}:{smooth}", 8,
        ))
        outputs[recipes / f"{bricks}.json"] = json_bytes(shaped(
            ["##", "##"], {"#": {"item": f"{NAMESPACE}:{smooth}"}}, f"{NAMESPACE}:{bricks}", 4,
        ))
        outputs[recipes / f"{packed}.json"] = json_bytes(shaped(
            ["##", "##"], {"#": {"item": f"{NAMESPACE}:{bricks}"}}, f"{NAMESPACE}:{packed}", 4,
        ))
        outputs[recipes / f"{pillar}.json"] = json_bytes(shaped(
            ["#", "#"], {"#": {"item": f"{NAMESPACE}:{smooth}"}}, f"{NAMESPACE}:{pillar}", 2,
        ))
        owned.update((recipes / f"{base}.json" for base in (smooth, bricks, packed, pillar)))

        for base_id, display_name, is_pillar in definitions:
            families.append((base_id, is_pillar))
            before = set(outputs)
            add_family_resources(outputs, base_id, is_pillar)
            add_shape_recipes(outputs, base_id)
            owned.update(set(outputs) - before)
            for block_id, suffix in zip(block_ids(base_id), ("", " Stairs", " Slab", " Wall")):
                lang[f"block.{NAMESPACE}.{block_id}"] = display_name + suffix
                tag("src/main/resources/data/minecraft/tags/blocks/mineable/pickaxe.json", block_id)
            tag("src/main/resources/data/minecraft/tags/blocks/stairs.json", f"{base_id}_stairs")
            tag("src/main/resources/data/minecraft/tags/items/stairs.json", f"{base_id}_stairs")
            tag("src/main/resources/data/minecraft/tags/blocks/slabs.json", f"{base_id}_slab")
            tag("src/main/resources/data/minecraft/tags/items/slabs.json", f"{base_id}_slab")
            tag("src/main/resources/data/minecraft/tags/blocks/walls.json", f"{base_id}_wall")

    outputs[JAVA] = generated_java(families)
    update_shared_json(outputs, state, lang, tags)
    new_state = {
        "schema_version": 1,
        "owned_files": sorted(path.relative_to(ROOT).as_posix() for path in owned),
        "lang_keys": sorted(lang),
        "tag_values": {
            path.relative_to(ROOT).as_posix(): values for path, values in sorted(tags.items(), key=lambda item: str(item[0]))
        },
    }
    stale = {ROOT / path for path in state.get("owned_files", [])} - owned
    return outputs, stale, new_state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    outputs, stale, state = build_plan()
    changed = [path for path, data in outputs.items() if not path.exists() or path.read_bytes() != data]
    changed.extend(path for path in stale if path.exists())
    state_data = json_bytes(state)
    if not STATE.exists() or STATE.read_bytes() != state_data:
        changed.append(STATE)

    for path in sorted(set(changed), key=str):
        print(path.relative_to(ROOT))
    if args.check:
        if changed:
            print(f"{len(set(changed))} pastel concrete outputs are stale")
            return 1
        print("Pastel concrete outputs are up to date")
        return 0
    if args.dry_run:
        print(f"Would update {len(set(changed))} files")
        return 0

    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != data:
            path.write_bytes(data)
    for path in stale:
        if path.exists():
            path.unlink()
    STATE.write_bytes(state_data)
    print(f"Updated {len(set(changed))} files for {len(COLORS)} colors and {len(COLORS) * 16} blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
