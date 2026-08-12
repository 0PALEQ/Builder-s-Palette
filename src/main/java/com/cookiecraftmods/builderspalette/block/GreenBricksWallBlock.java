
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.WallBlock;

public class GreenBricksWallBlock extends WallBlock {
	public GreenBricksWallBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.STONE).strength(1f, 10f).forceSolidOn());
	}
}
