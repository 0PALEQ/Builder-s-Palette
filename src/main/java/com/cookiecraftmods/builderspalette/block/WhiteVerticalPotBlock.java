
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.NoteBlockInstrument;
import net.minecraft.state.property.DirectionProperty;
import net.minecraft.state.StateManager;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.util.BlockRotation;
import net.minecraft.util.BlockMirror;
import net.minecraft.block.HorizontalFacingBlock;
import net.minecraft.block.Block;
import net.minecraft.world.BlockView;
import net.minecraft.item.ItemPlacementContext;
import net.minecraft.util.math.Direction;
import net.minecraft.util.math.BlockPos;

public class WhiteVerticalPotBlock extends Block {
	public static final DirectionProperty FACING = HorizontalFacingBlock.FACING;

	public WhiteVerticalPotBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(NoteBlockInstrument.BASEDRUM).sounds(BlockSoundGroup.GRASS).strength(1f, 10f));
		this.setDefaultState(this.getDefaultState().with(FACING, Direction.NORTH));
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 15;
	}
	protected void appendProperties(StateManager.Builder<Block, BlockState> builder) {
		super.appendProperties(builder);
		builder.add(FACING);
	}
	public BlockState getPlacementState(ItemPlacementContext context) {
		return super.getPlacementState(context).with(FACING, context.getHorizontalPlayerFacing().getOpposite());
	}

	public BlockState rotate(BlockState state, BlockRotation rot) {
		return state.with(FACING, rot.rotate(state.get(FACING)));
	}

	public BlockState mirror(BlockState state, BlockMirror mirrorIn) {
		return state.rotate(mirrorIn.getRotation(state.get(FACING)));
	}
}
