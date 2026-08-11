
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.LeavesBlock;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.Direction;
import net.minecraft.util.math.BlockPos;

public class Dark_RedLeavesBlock extends LeavesBlock {
	public Dark_RedLeavesBlock() {
		super(BuildersPaletteBlockProperties.of().burnable().sounds(BlockSoundGroup.GRASS).strength(0.2f).nonOpaque());
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 1;
	}
	public int getFlammability(BlockState state, BlockView world, BlockPos pos, Direction face) {
		return 30;
	}
}
