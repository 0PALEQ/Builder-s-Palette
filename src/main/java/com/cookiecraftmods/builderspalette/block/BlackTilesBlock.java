
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockState;

public class BlackTilesBlock extends Block {
	public BlackTilesBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.STONE).strength(1f, 10f));
	}
	public int getOpacity(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 15;
	}
}
