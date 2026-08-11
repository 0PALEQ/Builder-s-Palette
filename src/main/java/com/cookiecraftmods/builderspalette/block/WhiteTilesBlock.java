
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.Block;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.BlockPos;

public class WhiteTilesBlock extends Block {
	public WhiteTilesBlock() {
		super(BuildersPaletteBlockProperties.of().sounds(BlockSoundGroup.STONE).strength(1f, 10f));
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 15;
	}
}
