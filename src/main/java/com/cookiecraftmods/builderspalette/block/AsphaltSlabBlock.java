
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.SlabBlock;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.BlockPos;

public class AsphaltSlabBlock extends SlabBlock {
	public AsphaltSlabBlock() {
		super(BuildersPaletteBlockProperties.of().sounds(BlockSoundGroup.STONE).strength(1f, 10f));
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
}
