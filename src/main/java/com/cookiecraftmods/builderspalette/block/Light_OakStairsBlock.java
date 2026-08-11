
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.Instrument;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.StairsBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.Blocks;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.Direction;
import net.minecraft.util.math.BlockPos;

public class Light_OakStairsBlock extends StairsBlock {
	public Light_OakStairsBlock() {
		super(Blocks.AIR.getDefaultState(), BuildersPaletteBlockProperties.of().burnable().instrument(Instrument.BASS).sounds(BlockSoundGroup.WOOD).strength(3f, 2f));
	}
	public float getExplosionResistance() {
		return 2f;
	}
	public boolean hasRandomTicks(BlockState state) {
		return false;
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
	public int getFlammability(BlockState state, BlockView world, BlockPos pos, Direction face) {
		return 5;
	}
}
