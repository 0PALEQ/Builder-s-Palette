
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.core.BlockPos;

public class CalciteStairsBlock extends StairBlock {
	public CalciteStairsBlock() {
		super(Blocks.AIR.defaultBlockState(), BuildersPaletteBlockProperties.of().sound(SoundType.CALCITE).strength(1f, 10f).dynamicShape());
	}
	public float getExplosionResistance() {
		return 10f;
	}
	public boolean hasRandomTicks(BlockState state) {
		return false;
	}
	public int getLightBlock(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 0;
	}
}
