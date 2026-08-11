
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.Instrument;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.StairsBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.Blocks;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.BlockPos;

public class BrownBricksStairsBlock extends StairsBlock {
	public BrownBricksStairsBlock() {
		super(Blocks.AIR.getDefaultState(), BuildersPaletteBlockProperties.of().instrument(Instrument.BASEDRUM).sounds(BlockSoundGroup.STONE).strength(1f, 10f));
	}
	public float getExplosionResistance() {
		return 10f;
	}
	public boolean hasRandomTicks(BlockState state) {
		return false;
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
}
