
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

public class CornerWhiteWallPanelsBlock extends Block {
	public static final EnumProperty<Direction> FACING = HorizontalDirectionalBlock.FACING;

	public CornerWhiteWallPanelsBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(NoteBlockInstrument.BASEDRUM).sound(SoundType.METAL).strength(1f, 10f).noOcclusion().isRedstoneConductor((bs, br, bp) -> false));
		this.registerDefaultState(this.defaultBlockState().setValue(FACING, Direction.NORTH));
	}
	public boolean useShapeForLightOcclusion(BlockState state) {
		return true;
	}
	public int getOpacity(BlockState state, BlockGetter worldIn, BlockPos pos) {
		return 0;
	}
	public VoxelShape getVisualShape(BlockState state, BlockGetter world, BlockPos pos, CollisionContext context) {
		return Shapes.empty();
	}
	public VoxelShape getShape(BlockState state, BlockGetter world, BlockPos pos, CollisionContext context) {
		return switch (state.getValue(FACING)) {
			default -> Shapes.or(box(0, 0, -2, 16, 16, 2), box(-2, 0, -16, 2, 16, 0));
			case NORTH -> Shapes.or(box(0, 0, 14, 16, 16, 18), box(14, 0, 16, 18, 16, 32));
			case EAST -> Shapes.or(box(-2, 0, 0, 2, 16, 16), box(-16, 0, 14, 0, 16, 18));
			case WEST -> Shapes.or(box(14, 0, 0, 18, 16, 16), box(16, 0, -2, 32, 16, 2));
		};
	}
	protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
		super.createBlockStateDefinition(builder);
		builder.add(FACING);
	}
	public BlockState getStateForPlacement(BlockPlaceContext context) {
		return super.getStateForPlacement(context).setValue(FACING, context.getHorizontalDirection().getOpposite());
	}

	public BlockState rotate(BlockState state, Rotation rot) {
		return state.setValue(FACING, rot.rotate(state.getValue(FACING)));
	}

	public BlockState mirror(BlockState state, Mirror mirrorIn) {
		return rotate(state, mirrorIn.getRotation(state.getValue(FACING)));
	}
}
