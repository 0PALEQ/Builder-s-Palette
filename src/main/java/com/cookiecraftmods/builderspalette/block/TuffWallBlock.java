
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.core.BlockPos;

public class TuffWallBlock extends WallBlock {
	public TuffWallBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.TUFF).strength(1f, 10f).dynamicShape().forceSolidOn());
	}
	public int getLightBlock(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 0;
	}
}
