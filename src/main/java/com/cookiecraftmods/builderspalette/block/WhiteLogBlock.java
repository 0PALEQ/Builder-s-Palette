
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.NoteBlockInstrument;
import net.minecraft.state.property.EnumProperty;
import net.minecraft.state.property.Properties;
import net.minecraft.state.StateManager;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.util.BlockRotation;
import net.minecraft.block.Block;
import net.minecraft.world.BlockView;
import net.minecraft.item.ItemPlacementContext;
import net.minecraft.util.math.Direction;
import net.minecraft.util.math.BlockPos;

public class WhiteLogBlock extends Block {
	public static final EnumProperty<Direction.Axis> AXIS = Properties.AXIS;

	public WhiteLogBlock() {
		super(BuildersPaletteBlockProperties.of().burnable().instrument(NoteBlockInstrument.BASS).sounds(BlockSoundGroup.WOOD).strength(2f));
		this.setDefaultState(this.getDefaultState().with(AXIS, Direction.Axis.Y));
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 15;
	}
	protected void appendProperties(StateManager.Builder<Block, BlockState> builder) {
		super.appendProperties(builder);
		builder.add(AXIS);
	}
	public BlockState getPlacementState(ItemPlacementContext context) {
		return super.getPlacementState(context).with(AXIS, context.getSide().getAxis());
	}
	public BlockState rotate(BlockState state, BlockRotation rot) {
		if (rot == BlockRotation.CLOCKWISE_90 || rot == BlockRotation.COUNTERCLOCKWISE_90) {
			if (state.get(AXIS) == Direction.Axis.X) {
				return state.with(AXIS, Direction.Axis.Z);
			} else if (state.get(AXIS) == Direction.Axis.Z) {
				return state.with(AXIS, Direction.Axis.X);
			}
		}
		return state;
	}
	public int getFlammability(BlockState state, BlockView world, BlockPos pos, Direction face) {
		return 5;
	}
}
