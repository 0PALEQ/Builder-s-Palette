
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.NoteBlockInstrument;
import net.minecraft.block.BlockSetType;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.ButtonBlock;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.Direction;
import net.minecraft.util.math.BlockPos;

public class GreyButtonBlock extends ButtonBlock {
	public GreyButtonBlock() {
		super(BlockSetType.OAK, 30, BuildersPaletteBlockProperties.of().burnable().instrument(NoteBlockInstrument.BASS).sounds(BlockSoundGroup.WOOD).strength(2f, 3f));
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
	public int getFlammability(BlockState state, BlockView world, BlockPos pos, Direction face) {
		return 5;
	}
}
