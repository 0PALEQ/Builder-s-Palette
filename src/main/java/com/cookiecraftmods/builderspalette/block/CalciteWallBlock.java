
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.core.BlockPos;

public class CalciteWallBlock extends WallBlock {
	public CalciteWallBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.CALCITE).strength(1f, 10f).dynamicShape().forceSolidOn());
	}
	public int getLightBlock(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 0;
	}
}
