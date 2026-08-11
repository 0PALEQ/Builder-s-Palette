# Block family generator

`add_blocks.py` adds ordinary solid block families without creating a Java
class for every block shape. It generates registrations, textures, blockstates,
models, loot tables, language entries, mining tags, and shape tags.

## Safe workflow

1. Copy textures into a folder near the manifest. Texture paths are resolved
   relative to the manifest file.
2. Add a family to `block_families.json`. See `block_families.example.json`.
3. Preview and validate all changes:

   ```powershell
   python tools/add_blocks.py --dry-run
   ```

4. Generate the files and compile the mod:

   ```powershell
   python tools/add_blocks.py
   .\gradlew.bat build
   ```

5. CI or a local validation can check for stale generated files:

   ```powershell
   python tools/add_blocks.py --check
   ```

The state in `block_generator_state.json` identifies only files and JSON values
owned by this generator. Removing a family from the manifest and rerunning the
script removes those managed outputs, but it will not overwrite or delete an
unmanaged existing resource.

## Parameters

- `id`: lowercase registry ID such as `blue_marble`.
- `display_name`: English block name.
- `texture`: one PNG used on every face.
- `textures`: instead of `texture`, an object containing `side`, `top`, and
  `bottom` PNG paths.
- `variants`: any of `block`, `stairs`, `slab`, and `wall`; `block` is required.
- `sound`: a supported `BlockSoundGroup` constant such as `STONE` or `WOOD`.
- `hardness` and `resistance`: non-negative block strength values.
- `requires_tool`: whether the block requires the correct tool for drops.
- `tool`: `pickaxe`, `axe`, `shovel`, `hoe`, or `none`.
- `render_type`: currently `solid`. Cutout/translucent blocks need additional
  client-side render-layer registration and are intentionally rejected.

Recipes and behavior-bearing blocks are intentionally outside the initial safe
scope. They require explicit inputs or handwritten behavior rather than values
the generator could safely guess.
