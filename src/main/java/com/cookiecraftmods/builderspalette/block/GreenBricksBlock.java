
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.core.BlockPos;

public class GreenBricksBlock extends Block {
	public GreenBricksBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.STONE).strength(1f, 10f));
	}
	public int getLightBlock(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 15;
	}
}
