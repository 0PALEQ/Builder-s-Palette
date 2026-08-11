
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.NoteBlockInstrument;
import net.minecraft.block.BlockSetType;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.PressurePlateBlock;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.Direction;
import net.minecraft.util.math.BlockPos;

public class GreyPressurePlateBlock extends PressurePlateBlock {
	public GreyPressurePlateBlock() {
		super(BlockSetType.OAK, BuildersPaletteBlockProperties.of().burnable().instrument(NoteBlockInstrument.BASS).sounds(BlockSoundGroup.WOOD).strength(2f, 3f).solid());
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
	public int getFlammability(BlockState state, BlockView world, BlockPos pos, Direction face) {
		return 5;
	}
}
