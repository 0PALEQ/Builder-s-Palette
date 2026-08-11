
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.AbstractBlock;
import net.minecraft.block.WallBlock;
import net.minecraft.sound.BlockSoundGroup;

public class GreenBricksWallBlock extends WallBlock {
	public GreenBricksWallBlock() {
		super(BuildersPaletteBlockProperties.of().sounds(BlockSoundGroup.STONE).strength(1f, 10f).solid());
	}
}
