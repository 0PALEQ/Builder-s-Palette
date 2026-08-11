
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.fluid.FluidState;
import net.minecraft.block.enums.Instrument;
import net.minecraft.block.BlockState;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.PaneBlock;
import net.minecraft.world.BlockView;
import net.minecraft.world.BlockRenderView;
import net.minecraft.util.math.BlockPos;

public class FramedGlassBlock extends PaneBlock {
	public FramedGlassBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(Instrument.BASEDRUM).sounds(BlockSoundGroup.GLASS).strength(1f, 10f).nonOpaque().solidBlock((bs, br, bp) -> false));
	}
	public boolean shouldDisplayFluidOverlay(BlockState state, BlockRenderView world, BlockPos pos, FluidState fluidstate) {
		return true;
	}
	public int getOpacity(BlockState state, BlockView worldIn, BlockPos pos) {
		return 0;
	}
}
