
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.StairsBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.Blocks;

public class GreenBricksStairsBlock extends StairsBlock {
	public GreenBricksStairsBlock() {
		super(Blocks.AIR.getDefaultState(), BuildersPaletteBlockProperties.of().sounds(BlockSoundGroup.STONE).strength(1f, 10f));
	}
	public float getExplosionResistance() {
		return 10f;
	}
	public boolean hasRandomTicks(BlockState state) {
		return false;
	}
}
