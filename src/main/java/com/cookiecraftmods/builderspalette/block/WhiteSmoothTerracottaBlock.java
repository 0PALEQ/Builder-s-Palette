
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.Instrument;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.Block;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.BlockPos;

public class WhiteSmoothTerracottaBlock extends Block {
	public WhiteSmoothTerracottaBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(Instrument.BASEDRUM).sounds(BlockSoundGroup.STONE).strength(1f, 10f));
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 15;
	}
}
