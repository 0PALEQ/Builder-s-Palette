
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.TintedParticleLeavesBlock;
import net.minecraft.world.level.block.state.BlockState;

public class Dark_RedLeavesBlock extends TintedParticleLeavesBlock {
	public Dark_RedLeavesBlock() {
		super(0.01f, BuildersPaletteBlockProperties.of().ignitedByLava().sound(SoundType.GRASS).strength(0.2f).noOcclusion());
	}
	public int getOpacity(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 1;
	}
	public int getFlammability(BlockState state, BlockGetter world, BlockPos pos, Direction face) {
		return 30;
	}
}
