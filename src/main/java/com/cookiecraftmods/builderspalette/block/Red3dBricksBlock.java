
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.util.shape.VoxelShape;
import net.minecraft.util.shape.VoxelShapes;
import net.minecraft.block.ShapeContext;
import net.minecraft.block.enums.Instrument;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.Block;
import net.minecraft.world.BlockView;
import net.minecraft.util.math.BlockPos;

public class Red3dBricksBlock extends Block {
	public Red3dBricksBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(Instrument.BASEDRUM).sounds(BlockSoundGroup.STONE).strength(1f, 10f).nonOpaque().solidBlock((bs, br, bp) -> false));
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
}
