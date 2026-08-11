
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.AbstractBlock;
import net.minecraft.block.WallBlock;
import net.minecraft.sound.BlockSoundGroup;

public class LightGrayBricksWallBlock extends WallBlock {
	public LightGrayBricksWallBlock() {
		super(BuildersPaletteBlockProperties.of().sounds(BlockSoundGroup.STONE).strength(1f, 10f).solid());
	}
}
