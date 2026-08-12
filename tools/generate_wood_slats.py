#!/usr/bin/env python3
"""Generate log-textured wall slats for every custom wood family.

The raised slats use each family's plank texture. A dark, wood-tinted backing
texture is derived from the same source so every variant keeps the existing
coffee slat design while remaining recognizable as its wood family.
"""

from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
from typing import Callable

try:
    from PIL import Image, ImageEnhance
except ImportError as exc:  # pragma: no cover - developer environment guard
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc


ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / "src/main/java/com/cookiecraftmods/builderspalette/init"
RESOURCES = ROOT / "src/main/resources"
ASSETS = RESOURCES / "assets/builders_palette"
DATA = RESOURCES / "data"

WOODS = (
    ("light_oak", "Light Oak"),
    ("dark_red", "Dark Red"),
    ("grey", "Grey"),
    ("white", "White"),
    ("wenge", "Wenge"),
    ("maple", "Maple"),
    ("cedar", "Cedar"),
    ("walnut", "Walnut"),
    ("olive", "Olive"),
    ("purpleheart", "Purpleheart"),
)

BEGIN = "// BEGIN GENERATED WOOD WALL SLATS"
END = "// END GENERATED WOOD WALL SLATS"


def json_text(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def slat_id(wood_id: str) -> str:
    return f"{wood_id}_wood_wall_slats"


def variants():
    for wood_id, display_name in WOODS:
        yield (
            f"{wood_id}_log_wall_slats",
            f"{display_name} Log Wall Slats",
            f"{wood_id}_log_side",
            f"{wood_id}_log",
        )


def constant(block_id: str) -> str:
    return block_id.upper()


def blockstate(block_id: str) -> dict:
    model = f"builders_palette:block/{block_id}"
    return {
        "variants": {
            "facing=north": {"model": model},
            "facing=east": {"model": model, "y": 90},
            "facing=south": {"model": model, "y": 180},
            "facing=west": {"model": model, "y": 270},
        }
    }


def block_model(block_id: str, texture: str) -> dict:
    backing = f"builders_palette:block/{block_id}_back"
    return {
        "parent": "builders_palette:custom/wood_wall_slats",
        "textures": {
            "all": backing,
            "particle": backing,
            "0": backing,
            "1": f"builders_palette:block/{texture}",
        },
        "render_type": "solid",
    }


def item_model(block_id: str) -> dict:
    return {
        "parent": f"builders_palette:block/{block_id}",
        "display": {
            "gui": {
                "rotation": [20, 200, 0],
                "translation": [0, 0, 0],
                "scale": [0.75, 0.75, 0.75],
            },
            "thirdperson_righthand": {
                "rotation": [10, -45, 170],
                "translation": [0, 1.5, -2.75],
                "scale": [0.375, 0.375, 0.375],
            },
            "thirdperson_lefthand": {
                "rotation": [10, 45, -170],
                "translation": [0, 1.5, -2.75],
                "scale": [0.375, 0.375, 0.375],
            },
        },
    }


def loot_table(block_id: str) -> dict:
    return {
        "type": "minecraft:block",
        "random_sequence": f"builders_palette:blocks/{block_id}",
        "pools": [
            {
                "rolls": 1,
                "bonus_rolls": 0,
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": f"builders_palette:{block_id}",
                    }
                ],
                "conditions": [{"condition": "minecraft:survives_explosion"}],
            }
        ],
    }


def recipe(block_id: str, ingredient: str) -> dict:
    return {
        "type": "minecraft:crafting_shaped",
        "category": "building",
        "pattern": ["###", "###"],
        "key": {"#": f"builders_palette:{ingredient}"},
        "result": {"id": f"builders_palette:{block_id}", "count": 6},
        "show_notification": True,
    }


def dark_backing(source: Path) -> bytes:
    with Image.open(source) as image:
        rgba = image.convert("RGBA")
        rgb = rgba.convert("RGB")
        rgb = ImageEnhance.Color(rgb).enhance(0.55)
        rgb = ImageEnhance.Brightness(rgb).enhance(0.18)
        red, green, blue = rgb.split()
        alpha = rgba.getchannel("A")
        result = Image.merge("RGBA", (red, green, blue, alpha))
        output = io.BytesIO()
        result.save(output, format="PNG", optimize=True)
        return output.getvalue()


def fixed_slats_model() -> dict:
    """Convert the existing 32px slat geometry to correct 16px texture UVs."""
    source = ASSETS / "models/custom/lamel.json"
    model = json.loads(source.read_text(encoding="utf-8"))
    model["credit"] = "Builders Palette 16px wall slats, based on the original Blockbench model"
    model["texture_size"] = [16, 16]
    stripe_elements = [
        element
        for element in model["elements"]
        if any(face.get("texture") == "#1" for face in element.get("faces", {}).values())
    ]
    for index, element in enumerate(stripe_elements):
        u = index * 2
        for face_name, face in element["faces"].items():
            if face.get("texture") != "#1":
                continue
            if face_name in ("up", "down"):
                face["uv"] = [u, 0, u + 1, 1]
            else:
                face["uv"] = [u, 0, u + 1, 16]
    return model


def generated_section(content: str, anchor: str, lines: list[str]) -> str:
    indent = anchor[: len(anchor) - len(anchor.lstrip())]
    body = "\n".join(f"{indent}{line}" for line in [BEGIN, *lines, END])
    if BEGIN in content and END in content:
        marker = content.index(BEGIN)
        start = content.rfind("\n", 0, marker) + 1
        finish = content.index(END, start) + len(END)
        return content[:start] + body + content[finish:]
    if anchor not in content:
        raise RuntimeError(f"Could not find generation anchor: {anchor}")
    return content.replace(anchor, f"{anchor}\n{body}", 1)


def update_json(path: Path, update: Callable[[dict], None]) -> str:
    value = json.loads(path.read_text(encoding="utf-8"))
    update(value)
    return json_text(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated outputs are stale")
    parser.add_argument("--dry-run", action="store_true", help="list changes without writing them")
    args = parser.parse_args()

    text_outputs: dict[Path, str] = {}
    binary_outputs: dict[Path, bytes] = {}
    generated_variants = tuple(variants())
    obsolete_outputs: list[Path] = []
    for wood_id, _ in WOODS:
        old_id = slat_id(wood_id)
        obsolete_outputs.extend(
            (
                ASSETS / f"blockstates/{old_id}.json",
                ASSETS / f"models/block/{old_id}.json",
                ASSETS / f"models/item/{old_id}.json",
                ASSETS / f"items/{old_id}.json",
                ASSETS / f"textures/block/{old_id}_back.png",
                DATA / f"builders_palette/loot_table/blocks/{old_id}.json",
                DATA / f"builders_palette/recipe/{old_id}.json",
            )
        )
    text_outputs[ASSETS / "models/custom/wood_wall_slats.json"] = json_text(fixed_slats_model())

    for block_id, display_name, texture, ingredient in generated_variants:
        text_outputs[ASSETS / f"blockstates/{block_id}.json"] = json_text(blockstate(block_id))
        text_outputs[ASSETS / f"models/block/{block_id}.json"] = json_text(block_model(block_id, texture))
        text_outputs[ASSETS / f"models/item/{block_id}.json"] = json_text(item_model(block_id))
        text_outputs[ASSETS / f"items/{block_id}.json"] = json_text(
            {"model": {"type": "minecraft:model", "model": f"builders_palette:item/{block_id}"}}
        )
        text_outputs[DATA / f"builders_palette/loot_table/blocks/{block_id}.json"] = json_text(loot_table(block_id))
        text_outputs[DATA / f"builders_palette/recipe/{block_id}.json"] = json_text(recipe(block_id, ingredient))
        source = ASSETS / f"textures/block/{texture}.png"
        if not source.is_file():
            raise FileNotFoundError(f"Missing plank texture for {display_name}: {source}")
        binary_outputs[ASSETS / f"textures/block/{block_id}_back.png"] = dark_backing(source)

    blocks_path = JAVA / "BuildersPaletteModBlocks.java"
    blocks = blocks_path.read_text(encoding="utf-8")
    import_line = "import com.cookiecraftmods.builderspalette.block.WoodWallSlatsBlock;"
    if import_line not in blocks:
        anchor = "import com.cookiecraftmods.builderspalette.block.CoffeWoodWallSlatsBlock;"
        blocks = blocks.replace(anchor, f"{anchor}\n{import_line}", 1)
    block_anchor = (
        '\tpublic static final RegistryObject<Block> COFFE_WOOD_WALL_SLATS = '
        'register("coffe_wood_wall_slats", () -> new CoffeWoodWallSlatsBlock());'
    )
    block_lines = [
        f'public static final RegistryObject<Block> {constant(block_id)} = register("{block_id}", WoodWallSlatsBlock::new);'
        for block_id, _, _, _ in generated_variants
    ]
    text_outputs[blocks_path] = generated_section(blocks, block_anchor, block_lines)

    items_path = JAVA / "BuildersPaletteModItems.java"
    items = items_path.read_text(encoding="utf-8")
    item_anchor = (
        "\tpublic static final RegistryObject<Item> COFFE_WOOD_WALL_SLATS = "
        "block(BuildersPaletteModBlocks.COFFE_WOOD_WALL_SLATS);"
    )
    item_lines = [
        f"public static final RegistryObject<Item> {constant(block_id)} = block(BuildersPaletteModBlocks.{constant(block_id)});"
        for block_id, _, _, _ in generated_variants
    ]
    text_outputs[items_path] = generated_section(items, item_anchor, item_lines)

    tabs_path = JAVA / "BuildersPaletteModTabs.java"
    tabs = tabs_path.read_text(encoding="utf-8")
    tab_anchor = "\t\t\t\ttabData.accept(BuildersPaletteModBlocks.COFFE_WOOD_WALL_SLATS.get().asItem());"
    tab_lines = [
        f"tabData.accept(BuildersPaletteModBlocks.{constant(block_id)}.get().asItem());"
        for block_id, _, _, _ in generated_variants
    ]
    text_outputs[tabs_path] = generated_section(tabs, tab_anchor, tab_lines)

    for language in ("en_us", "pl_pl"):
        lang_path = ASSETS / f"lang/{language}.json"

        def add_names(value: dict) -> None:
            for wood_id, _ in WOODS:
                value.pop(f"block.builders_palette.{slat_id(wood_id)}", None)
            for block_id, display_name, _, _ in generated_variants:
                value[f"block.builders_palette.{block_id}"] = display_name

        text_outputs[lang_path] = update_json(lang_path, add_names)

    axe_path = DATA / "minecraft/tags/block/mineable/axe.json"

    def add_axe_values(value: dict) -> None:
        values = value.setdefault("values", [])
        coffee = "builders_palette:coffe_wood_wall_slats"
        if coffee not in values:
            values.append(coffee)
        obsolete = {f"builders_palette:{slat_id(wood_id)}" for wood_id, _ in WOODS}
        values[:] = [entry for entry in values if entry not in obsolete]
        for block_id, _, _, _ in generated_variants:
            entry = f"builders_palette:{block_id}"
            if entry not in values:
                values.append(entry)

    text_outputs[axe_path] = update_json(axe_path, add_axe_values)

    changed: list[Path] = []
    for path, content in text_outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            changed.append(path)
            if not args.check and not args.dry_run:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
    for path, content in binary_outputs.items():
        current = path.read_bytes() if path.exists() else None
        if current != content:
            changed.append(path)
            if not args.check and not args.dry_run:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
    for path in obsolete_outputs:
        if path.exists():
            changed.append(path)
            if not args.check and not args.dry_run:
                path.unlink()

    for path in changed:
        print(path.relative_to(ROOT))
    if args.check and changed:
        print(f"{len(changed)} generated wood-slat outputs are stale")
        return 1
    verb = "Would update" if args.dry_run else "Updated"
    print(f"{verb} {len(changed)} files for {len(generated_variants)} wood slat variants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
