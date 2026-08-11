
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.WallBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.BlockPos;

public class PackedMudWallBlock extends WallBlock {
	public PackedMudWallBlock() {
		super(BuildersPaletteBlockProperties.of().sounds(BlockSoundGroup.PACKED_MUD).strength(1f, 10f).dynamicBounds().solid());
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
}
