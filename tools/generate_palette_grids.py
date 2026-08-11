#!/usr/bin/env python3
"""Render reusable gallery grids from Builders Palette block textures."""

from __future__ import annotations

import argparse
import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from generate_pastel_concrete import COLORS


ROOT = Path(__file__).resolve().parents[1]
TEXTURES = ROOT / "src/main/resources/assets/builders_palette/textures/block"
OUTPUT = ROOT / "gallery/pastel_concrete"
WOOD_OUTPUT = ROOT / "gallery/wood"
LOGO = ROOT / "src/main/resources/logo.png"

BACKGROUND = (20, 23, 30)
PANEL = (31, 36, 46)
PANEL_ALT = (36, 42, 54)
BORDER = (73, 82, 101)
TEXT = (241, 243, 247)
MUTED = (168, 177, 194)
ACCENT = (213, 165, 101)

FAMILIES = (
    ("smooth_concrete", "Smooth"),
    ("concrete_bricks", "Bricks"),
    ("packed_concrete_bricks", "Packed Bricks"),
    ("concrete_pillar", "Pillar"),
)
SHAPES = (("block", "Block"), ("stairs", "Stairs"), ("slab", "Slab"), ("wall", "Wall"))

WOODS = (
    ("light_oak", "Light Oak", "ikea_wood"),
    ("dark_red", "Dark Red", "table-top"),
    ("grey", "Grey", "grey_planks"),
    ("white", "White", "white_planks"),
    ("wenge", "Wenge", "wenge_planks"),
    ("maple", "Maple", "maple_planks"),
    ("cedar", "Cedar", "cedar_planks"),
    ("walnut", "Walnut", "walnut_planks"),
    ("olive", "Olive", "olive_planks"),
    ("purpleheart", "Purpleheart", "purpleheart_planks"),
)
WOOD_OVERVIEW_ROWS = (
    ("planks", "Planks"),
    ("log", "Log"),
    ("wood", "Wood"),
    ("leaves", "Leaves"),
    ("fence", "Fences"),
)
WOOD_BLOCKS = (
    ("planks", "Planks", "block"),
    ("log", "Log", "block"),
    ("wood", "Wood", "block"),
    ("leaves", "Leaves", "block"),
    ("stairs", "Stairs", "stairs"),
    ("slab", "Slab", "slab"),
    ("fence", "Fence", "fence"),
    ("fence_gate", "Fence Gate", "fence_gate"),
    ("pressure_plate", "Pressure Plate", "pressure_plate"),
    ("button", "Button", "button"),
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ("seguisb.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")
    for name in names:
        path = Path("C:/Windows/Fonts") / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], value: str, face, fill=TEXT) -> None:
    box = draw.textbbox((0, 0), value, font=face)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), value, font=face, fill=fill)


def shade(color: tuple[int, int, int, int], factor: float) -> tuple[int, int, int, int]:
    return tuple(max(0, min(255, round(channel * factor))) for channel in color[:3]) + (color[3],)


def occupancy(shape: str) -> set[tuple[int, int, int]]:
    result: set[tuple[int, int, int]] = set()
    if shape == "block":
        return {(x, y, z) for x in range(16) for y in range(16) for z in range(16)}
    if shape == "slab":
        return {(x, y, z) for x in range(16) for y in range(8) for z in range(16)}
    if shape == "stairs":
        for x in range(16):
            for z in range(16):
                height = 16 if z >= 8 else 8
                result.update((x, y, z) for y in range(height))
        return result
    if shape == "wall":
        # Inventory-style wall: a full-height post and two lower arms.
        result.update((x, y, z) for x in range(5, 11) for y in range(16) for z in range(5, 11))
        result.update((x, y, z) for x in range(16) for y in range(12) for z in range(6, 10))
        return result
    if shape == "fence":
        result.update((x, y, z) for x in range(6, 10) for y in range(16) for z in range(6, 10))
        result.update((x, y, z) for x in range(16) for y in range(5, 8) for z in range(7, 9))
        result.update((x, y, z) for x in range(16) for y in range(11, 14) for z in range(7, 9))
        return result
    if shape == "fence_gate":
        result.update((x, y, z) for x in range(1, 4) for y in range(16) for z in range(6, 10))
        result.update((x, y, z) for x in range(12, 15) for y in range(16) for z in range(6, 10))
        result.update((x, y, z) for x in range(4, 12) for y in range(5, 8) for z in range(7, 9))
        result.update((x, y, z) for x in range(4, 12) for y in range(11, 14) for z in range(7, 9))
        return result
    if shape == "pressure_plate":
        return {(x, y, z) for x in range(2, 14) for y in range(2) for z in range(2, 14)}
    if shape == "button":
        return {(x, y, z) for x in range(5, 11) for y in range(3) for z in range(5, 11)}
    if shape == "wall_slats":
        return {(x, y, z) for x in range(16) for y in range(16) for z in range(5, 11)}
    raise ValueError(f"Unknown shape: {shape}")


def texture_for(color_id: str, family: str) -> tuple[Image.Image, Image.Image]:
    base = f"pastel_{color_id}_{family}"
    if family == "concrete_pillar":
        side = Image.open(TEXTURES / f"{base}_side.png").convert("RGBA")
        top = Image.open(TEXTURES / f"{base}_top.png").convert("RGBA")
    else:
        side = Image.open(TEXTURES / f"{base}.png").convert("RGBA")
        top = side.copy()
    return side, top


def render_textured_icon(side: Image.Image, top: Image.Image, shape: str, size: int = 160) -> Image.Image:
    filled = occupancy(shape)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    diagonal = 4
    # Standard 2:1 isometric projection; framing below keeps the full icon visible.
    rise = 2
    # Slightly taller than mathematical isometric projection so Minecraft
    # blocks retain their visual height at gallery scale.
    vertical = 5
    center_x = size // 2
    base_y = size // 2

    def project(x: int, y: int, z: int) -> tuple[float, float]:
        return center_x + (x - z) * diagonal, base_y + (x + z) * rise - y * vertical

    faces = []
    for x, y, z in filled:
        if (x, y + 1, z) not in filled:
            faces.append((x + y + z + 0.35, "top", x, y, z))
        if (x + 1, y, z) not in filled:
            faces.append((x + y + z + 0.2, "x", x, y, z))
        if (x, y, z + 1) not in filled:
            faces.append((x + y + z + 0.1, "z", x, y, z))
    faces.sort(key=lambda item: item[0])

    for _, face, x, y, z in faces:
        if face == "top":
            points = (project(x, y + 1, z), project(x + 1, y + 1, z), project(x + 1, y + 1, z + 1), project(x, y + 1, z + 1))
            color = shade(top.getpixel((x, 15 - z)), 1.08)
        elif face == "x":
            points = (project(x + 1, y, z), project(x + 1, y + 1, z), project(x + 1, y + 1, z + 1), project(x + 1, y, z + 1))
            color = shade(side.getpixel((z, 15 - y)), 0.82)
        else:
            points = (project(x, y, z + 1), project(x + 1, y, z + 1), project(x + 1, y + 1, z + 1), project(x, y + 1, z + 1))
            color = shade(side.getpixel((15 - x, 15 - y)), 0.68)
        draw.polygon(points, fill=color)

    # A soft shadow keeps pale icons readable without blurring their pixel edges.
    alpha = canvas.getchannel("A")
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(5)))
    shadow = ImageEnhance.Brightness(shadow).enhance(0)
    composed = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    composed.alpha_composite(shadow, (4, 7))
    composed.alpha_composite(canvas)
    return composed


def render_icon(color_id: str, family: str, shape: str, size: int = 160) -> Image.Image:
    side, top = texture_for(color_id, family)
    return render_textured_icon(side, top, shape, size)


def wood_textures(wood_id: str, plank_texture: str, block: str) -> tuple[Image.Image, Image.Image]:
    if block == "log":
        side_name, top_name = f"{wood_id}_log_side", f"{wood_id}_log_top"
    elif block == "wood":
        side_name = top_name = f"{wood_id}_log_side"
    elif block == "leaves":
        side_name = top_name = f"{wood_id}_leaves"
    elif block == "log_wall_slats":
        side_name, top_name = f"{wood_id}_log_wall_slats_back", f"{wood_id}_log_side"
    else:
        side_name = top_name = plank_texture
    return (
        Image.open(TEXTURES / f"{side_name}.png").convert("RGBA"),
        Image.open(TEXTURES / f"{top_name}.png").convert("RGBA"),
    )


def render_wood_icon(wood_id: str, plank_texture: str, block: str, shape: str, size: int = 160) -> Image.Image:
    side, top = wood_textures(wood_id, plank_texture, block)
    return render_textured_icon(side, top, shape, size)


def background(size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", size, BACKGROUND)
    pixels = image.load()
    for y in range(size[1]):
        factor = y / max(1, size[1] - 1)
        color = tuple(round(BACKGROUND[i] * (1 - factor) + (11, 13, 18)[i] * factor) for i in range(3))
        for x in range(size[0]):
            pixels[x, y] = color
    return image


def add_header(image: Image.Image, title: str, subtitle: str, title_size: int = 42) -> None:
    draw = ImageDraw.Draw(image)
    logo = Image.open(LOGO).convert("RGB").resize((72, 72), Image.Resampling.LANCZOS)
    image.paste(logo, (34, 24))
    draw.text((126, 27), title, font=font(title_size, True), fill=TEXT)
    draw.text((128, 76), subtitle, font=font(18), fill=MUTED)
    draw.line((34, 112, image.width - 34, 112), fill=ACCENT, width=2)


def overview() -> Image.Image:
    image = background((1920, 1080))
    add_header(image, "Pastel Concrete Collection", "10 colors • Smooth • Bricks • Packed Bricks • Pillars")
    draw = ImageDraw.Draw(image)
    left = 178
    top = 168
    column = 168
    row = 202

    for index, (color_id, display, _, _) in enumerate(COLORS):
        centered(draw, (left + index * column + column // 2, top - 28), display, font(18, True))
    for index, (_, label) in enumerate(FAMILIES):
        draw.text((38, top + index * row + 69), label, font=font(21, True), fill=MUTED)

    for row_index, (family, _) in enumerate(FAMILIES):
        for column_index, (color_id, _, _, _) in enumerate(COLORS):
            x = left + column_index * column
            y = top + row_index * row
            draw.rounded_rectangle((x + 8, y + 6, x + column - 8, y + row - 10), radius=16, fill=PANEL_ALT if (row_index + column_index) % 2 else PANEL, outline=BORDER, width=1)
            icon = render_icon(color_id, family, "block", 160)
            image.paste(icon, (x + 4, y + 20), icon)

    centered(draw, (960, 1038), "Builders Palette • Minecraft 1.20.1", font(17), MUTED)
    return image


def color_grid(color_id: str, display: str) -> Image.Image:
    image = background((1280, 1280))
    add_header(image, f"Pastel {display} Concrete", "Complete building palette • 16 blocks", 40)
    draw = ImageDraw.Draw(image)
    left = 186
    top = 194
    cell = 250

    for index, (_, label) in enumerate(SHAPES):
        centered(draw, (left + index * cell + cell // 2, top - 32), label, font(22, True))
    for index, (_, label) in enumerate(FAMILIES):
        draw.text((32, top + index * cell + 104), label, font=font(21, True), fill=MUTED)

    for row_index, (family, _) in enumerate(FAMILIES):
        for column_index, (shape, _) in enumerate(SHAPES):
            x = left + column_index * cell
            y = top + row_index * cell
            draw.rounded_rectangle((x + 9, y + 9, x + cell - 9, y + cell - 9), radius=18, fill=PANEL_ALT if (row_index + column_index) % 2 else PANEL, outline=BORDER, width=2)
            icon = render_icon(color_id, family, shape, 160).resize((208, 208), Image.Resampling.NEAREST)
            image.paste(icon, (x + 21, y + 21), icon)

    centered(draw, (640, 1250), "Builders Palette", font(17), MUTED)
    return image


def wood_overview() -> Image.Image:
    image = background((1920, 1080))
    add_header(image, "Wood Collection", "10 species • Planks • Logs • Wood • Leaves • Fences")
    draw = ImageDraw.Draw(image)
    left = 178
    top = 152
    column = 168
    row = 172

    for index, (_, display, _) in enumerate(WOODS):
        centered(draw, (left + index * column + column // 2, top - 22), display, font(17, True))
    for index, (_, label) in enumerate(WOOD_OVERVIEW_ROWS):
        draw.text((38, top + index * row + 63), label, font=font(20, True), fill=MUTED)

    for row_index, (block, _) in enumerate(WOOD_OVERVIEW_ROWS):
        for column_index, (wood_id, _, plank_texture) in enumerate(WOODS):
            x = left + column_index * column
            y = top + row_index * row
            draw.rounded_rectangle(
                (x + 8, y + 6, x + column - 8, y + row - 10),
                radius=16,
                fill=PANEL_ALT if (row_index + column_index) % 2 else PANEL,
                outline=BORDER,
                width=1,
            )
            shape = "fence" if block == "fence" else "block"
            icon = render_wood_icon(wood_id, plank_texture, block, shape, 148)
            image.paste(icon, (x + 10, y + 13), icon)

    centered(draw, (960, 1048), "Builders Palette • Minecraft 1.20.1", font(17), MUTED)
    return image


def wood_grid(wood_id: str, display: str, plank_texture: str) -> Image.Image:
    image = background((1280, 1120))
    add_header(image, f"{display} Wood", "Complete building palette • 10 blocks", 40)
    draw = ImageDraw.Draw(image)
    left = 50
    top = 150
    cell_width = 295
    cell_height = 300

    for index, (block, label, shape) in enumerate(WOOD_BLOCKS):
        row_index, column_index = divmod(index, 4)
        x = left + column_index * cell_width
        y = top + row_index * cell_height
        draw.rounded_rectangle(
            (x + 9, y + 9, x + cell_width - 9, y + cell_height - 9),
            radius=18,
            fill=PANEL_ALT if (row_index + column_index) % 2 else PANEL,
            outline=BORDER,
            width=2,
        )
        centered(draw, (x + cell_width // 2, y + 34), label, font(20, True))
        icon = render_wood_icon(wood_id, plank_texture, block, shape, 160).resize((220, 220), Image.Resampling.NEAREST)
        image.paste(icon, (x + 38, y + 57), icon)

    centered(draw, (640, 1084), "Builders Palette", font(17), MUTED)
    return image


def png_bytes(image: Image.Image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when gallery images are stale")
    args = parser.parse_args()
    outputs = {OUTPUT / "pastel_concrete_overview.png": png_bytes(overview())}
    for color_id, display, _, _ in COLORS:
        outputs[OUTPUT / f"pastel_{color_id}_concrete_grid.png"] = png_bytes(color_grid(color_id, display))
    outputs[WOOD_OUTPUT / "wood_overview.png"] = png_bytes(wood_overview())
    for wood_id, display, plank_texture in WOODS:
        outputs[WOOD_OUTPUT / f"{wood_id}_wood_grid.png"] = png_bytes(wood_grid(wood_id, display, plank_texture))

    changed = [path for path, data in outputs.items() if not path.exists() or path.read_bytes() != data]
    if args.check:
        if changed:
            print(f"{len(changed)} palette grids are stale")
            return 1
        print(f"All {len(outputs)} palette grids are up to date")
        return 0
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(path.relative_to(ROOT))
    print(f"Generated {len(outputs)} gallery images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
