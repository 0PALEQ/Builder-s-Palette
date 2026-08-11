package com.cookiecraftmods.builderspalette.init;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;

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
			RegistryObject.register(BuiltInRegistries.ITEM, block.getId().getPath(),
					() -> new BlockItem(block.get(), new Item.Properties()));
		}
	}

	public static void addToTab(CreativeModeTab.Output entries) {
		for (RegistryObject<Block> block : BLOCKS) {
			entries.accept(block.get().asItem());
		}
	}

	private static void registerFamily(String name, float hardness, float resistance,
			SoundType sound, boolean requiresTool, boolean stairs, boolean slab, boolean wall) {
		RegistryObject<Block> base = register(name,
				() -> new Block(settings(hardness, resistance, sound, requiresTool)));

		if (stairs) {
			register(name + "_stairs", () -> new StairBlock(base.get().defaultBlockState(),
					BlockBehaviour.Properties.copy(base.get())));
		}
		if (slab) {
			register(name + "_slab", () -> new SlabBlock(BlockBehaviour.Properties.copy(base.get())));
		}
		if (wall) {
			register(name + "_wall", () -> new WallBlock(BlockBehaviour.Properties.copy(base.get())));
		}
	}

	private static BlockBehaviour.Properties settings(float hardness, float resistance,
			SoundType sound, boolean requiresTool) {
		BlockBehaviour.Properties settings = BlockBehaviour.Properties.of()
				.sound(sound)
				.strength(hardness, resistance);
		return requiresTool ? settings.requiresCorrectToolForDrops() : settings;
	}

	private static RegistryObject<Block> register(String name, java.util.function.Supplier<? extends Block> supplier) {
		RegistryObject<Block> block = RegistryObject.register(BuiltInRegistries.BLOCK, name, supplier);
		BLOCKS.add(block);
		return block;
	}
}
