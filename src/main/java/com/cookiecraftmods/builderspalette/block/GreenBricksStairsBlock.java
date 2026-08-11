
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.Blocks;

public class GreenBricksStairsBlock extends StairBlock {
	public GreenBricksStairsBlock() {
		super(Blocks.AIR.defaultBlockState(), BuildersPaletteBlockProperties.of().sound(SoundType.STONE).strength(1f, 10f));
	}
	public float getExplosionResistance() {
		return 10f;
	}
	public boolean hasRandomTicks(BlockState state) {
		return false;
	}
}
