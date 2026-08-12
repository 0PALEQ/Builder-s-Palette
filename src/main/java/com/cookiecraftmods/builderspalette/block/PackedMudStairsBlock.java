
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.state.BlockState;

public class PackedMudStairsBlock extends StairBlock {
	public PackedMudStairsBlock() {
		super(Blocks.AIR.defaultBlockState(), BuildersPaletteBlockProperties.of().sound(SoundType.PACKED_MUD).strength(1f, 10f).dynamicShape());
	}
	public float getExplosionResistance() {
		return 10f;
	}
	public boolean isRandomlyTicking(BlockState state) {
		return false;
	}
	public int getOpacity(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 0;
	}
}
