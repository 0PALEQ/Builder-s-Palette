package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.HorizontalFacingBlock;
import net.minecraft.block.ShapeContext;
import net.minecraft.block.enums.Instrument;
import net.minecraft.item.ItemPlacementContext;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.state.StateManager;
import net.minecraft.state.property.DirectionProperty;
import net.minecraft.util.BlockMirror;
import net.minecraft.util.BlockRotation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Direction;
import net.minecraft.util.shape.VoxelShape;
import net.minecraft.util.shape.VoxelShapes;
import net.minecraft.world.BlockView;

/** Shared behavior and collision shape for the wall-mounted wood slat variants. */
public class WoodWallSlatsBlock extends Block {
	public static final DirectionProperty FACING = HorizontalFacingBlock.FACING;

	public WoodWallSlatsBlock() {
		super(BuildersPaletteBlockProperties.of()
			.instrument(Instrument.BASEDRUM)
			.sounds(BlockSoundGroup.WOOD)
			.strength(1f, 10f)
			.nonOpaque()
			.solidBlock((state, world, pos) -> false));
		setDefaultState(getDefaultState().with(FACING, Direction.NORTH));
	}

	@Override
	public boolean hasSidedTransparency(BlockState state) {
		return true;
	}

	@Override
	public int getOpacity(BlockState state, BlockView world, BlockPos pos) {
		return 0;
	}

	@Override
	public VoxelShape getCameraCollisionShape(BlockState state, BlockView world, BlockPos pos, ShapeContext context) {
		return VoxelShapes.empty();
	}

	@Override
	public VoxelShape getOutlineShape(BlockState state, BlockView world, BlockPos pos, ShapeContext context) {
		return switch (state.get(FACING)) {
			default -> createCuboidShape(0, 0, 0, 16, 16, 1.25);
			case NORTH -> createCuboidShape(0, 0, 14.75, 16, 16, 16);
			case EAST -> createCuboidShape(0, 0, 0, 1.25, 16, 16);
			case WEST -> createCuboidShape(14.75, 0, 0, 16, 16, 16);
		};
	}

	@Override
	protected void appendProperties(StateManager.Builder<Block, BlockState> builder) {
		super.appendProperties(builder);
		builder.add(FACING);
	}

	@Override
	public BlockState getPlacementState(ItemPlacementContext context) {
		return super.getPlacementState(context).with(FACING, context.getHorizontalPlayerFacing().getOpposite());
	}

	@Override
	public BlockState rotate(BlockState state, BlockRotation rotation) {
		return state.with(FACING, rotation.rotate(state.get(FACING)));
	}

	@Override
	public BlockState mirror(BlockState state, BlockMirror mirror) {
		return state.rotate(mirror.getRotation(state.get(FACING)));
	}
}
