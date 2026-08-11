package com.cookiecraftmods.builderspalette.init;

import net.minecraft.block.AbstractBlock;
import net.minecraft.block.Block;
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

/**
 * Compact registrations owned by tools/add_blocks.py.
 *
 * <p>The generator replaces only the statements between the GENERATED markers.
 * The shared registration logic deliberately lives here so generated blocks do
 * not need one Java class per shape.</p>
 */
public final class GeneratedBlockFamilies {
	private static final List<RegistryObject<Block>> BLOCKS = new ArrayList<>();
	private static boolean blocksRegistered;
	private static boolean itemsRegistered;

	private GeneratedBlockFamilies() {
	}

	public static void registerBlocks() {
		if (blocksRegistered) {
			return;
		}
		blocksRegistered = true;

		// GENERATED BLOCK FAMILIES START
		// GENERATED BLOCK FAMILIES END
	}

	public static void registerItems() {
		if (itemsRegistered) {
			return;
		}
		if (!blocksRegistered) {
			throw new IllegalStateException("Generated blocks must be registered before their items");
		}
		itemsRegistered = true;

		for (RegistryObject<Block> block : BLOCKS) {
			RegistryObject.register(Registries.ITEM, block.getId().getPath(),
					() -> new BlockItem(block.get(), new Item.Settings()));
		}
	}

	public static void addToTab(ItemGroup.Entries entries) {
		for (RegistryObject<Block> block : BLOCKS) {
			entries.add(block.get().asItem());
		}
	}

	private static void registerFamily(String name, float hardness, float resistance,
			BlockSoundGroup sound, boolean requiresTool, boolean stairs, boolean slab, boolean wall) {
		RegistryObject<Block> base = register(name,
				() -> new Block(settings(hardness, resistance, sound, requiresTool)));

		if (stairs) {
			register(name + "_stairs", () -> new StairsBlock(base.get().getDefaultState(),
					AbstractBlock.Settings.copy(base.get())));
		}
		if (slab) {
			register(name + "_slab", () -> new SlabBlock(AbstractBlock.Settings.copy(base.get())));
		}
		if (wall) {
			register(name + "_wall", () -> new WallBlock(AbstractBlock.Settings.copy(base.get())));
		}
	}

	private static AbstractBlock.Settings settings(float hardness, float resistance,
			BlockSoundGroup sound, boolean requiresTool) {
		AbstractBlock.Settings settings = AbstractBlock.Settings.create()
				.sounds(sound)
				.strength(hardness, resistance);
		return requiresTool ? settings.requiresTool() : settings;
	}

	private static RegistryObject<Block> register(String name, java.util.function.Supplier<? extends Block> supplier) {
		RegistryObject<Block> block = RegistryObject.register(Registries.BLOCK, name, supplier);
		BLOCKS.add(block);
		return block;
	}
}
