
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.WallBlock;

public class LightGrayBricksWallBlock extends WallBlock {
	public LightGrayBricksWallBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.STONE).strength(1f, 10f).forceSolidOn());
	}
}
