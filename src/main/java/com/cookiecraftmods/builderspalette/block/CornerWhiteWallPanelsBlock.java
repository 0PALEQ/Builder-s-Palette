
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.util.shape.VoxelShape;
import net.minecraft.util.shape.VoxelShapes;
import net.minecraft.block.ShapeContext;
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

public class CornerWhiteWallPanelsBlock extends Block {
	public static final DirectionProperty FACING = HorizontalFacingBlock.FACING;

	public CornerWhiteWallPanelsBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(NoteBlockInstrument.BASEDRUM).sounds(BlockSoundGroup.METAL).strength(1f, 10f).nonOpaque().solidBlock((bs, br, bp) -> false));
		this.setDefaultState(this.getDefaultState().with(FACING, Direction.NORTH));
	}
	public boolean hasSidedTransparency(BlockState state) {
		return true;
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
	public VoxelShape getCameraCollisionShape(BlockState state, BlockView world, BlockPos pos, ShapeContext context) {
		return VoxelShapes.empty();
	}
	public VoxelShape getOutlineShape(BlockState state, BlockView world, BlockPos pos, ShapeContext context) {
		return switch (state.get(FACING)) {
			default -> VoxelShapes.union(createCuboidShape(0, 0, -2, 16, 16, 2), createCuboidShape(-2, 0, -16, 2, 16, 0));
			case NORTH -> VoxelShapes.union(createCuboidShape(0, 0, 14, 16, 16, 18), createCuboidShape(14, 0, 16, 18, 16, 32));
			case EAST -> VoxelShapes.union(createCuboidShape(-2, 0, 0, 2, 16, 16), createCuboidShape(-16, 0, 14, 0, 16, 18));
			case WEST -> VoxelShapes.union(createCuboidShape(14, 0, 0, 18, 16, 16), createCuboidShape(16, 0, -2, 32, 16, 2));
		};
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
