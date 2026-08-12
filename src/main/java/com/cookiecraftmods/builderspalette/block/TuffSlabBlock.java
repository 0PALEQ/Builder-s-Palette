
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockState;

public class TuffSlabBlock extends SlabBlock {
	public TuffSlabBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.TUFF).strength(1f, 10f).dynamicShape());
	}
	public int getOpacity(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 0;
	}
}
