
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.Instrument;
import net.minecraft.block.BlockSetType;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.ButtonBlock;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.Direction;
import net.minecraft.util.math.BlockPos;

public class Dark_RedButtonBlock extends ButtonBlock {
	public Dark_RedButtonBlock() {
		super(BuildersPaletteBlockProperties.of().burnable().instrument(Instrument.BASS).sounds(BlockSoundGroup.WOOD).strength(2f, 3f), BlockSetType.OAK, 30, true);
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
	public int getFlammability(BlockState state, BlockView world, BlockPos pos, Direction face) {
		return 5;
	}
}
