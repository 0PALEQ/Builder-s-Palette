
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.SlabBlock;

public class GreenBricksSlabBlock extends SlabBlock {
	public GreenBricksSlabBlock() {
		super(BuildersPaletteBlockProperties.of().sounds(BlockSoundGroup.STONE).strength(1f, 10f));
	}
}
