
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.core.BlockPos;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.state.BlockState;

public class PackedMudWallBlock extends WallBlock {
	public PackedMudWallBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.PACKED_MUD).strength(1f, 10f).dynamicShape().forceSolidOn());
	}
	public int getOpacity(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 0;
	}
}
