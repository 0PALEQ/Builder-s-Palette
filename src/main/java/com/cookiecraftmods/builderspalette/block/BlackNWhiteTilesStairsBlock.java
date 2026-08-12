
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.state.BlockState;

public class BlackNWhiteTilesStairsBlock extends StairBlock {
	public BlackNWhiteTilesStairsBlock() {
		super(Blocks.AIR.defaultBlockState(), BuildersPaletteBlockProperties.of().sound(SoundType.STONE).strength(1f, 10f));
	}
	public float getExplosionResistance() {
		return 10f;
	}
	public boolean isRandomlyTicking(BlockState state) {
		return false;
	}
}
