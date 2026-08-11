
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.WallBlock;
import net.minecraft.world.level.block.SoundType;

public class LightBrownBricksWallBlock extends WallBlock {
	public LightBrownBricksWallBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.STONE).strength(1f, 10f).forceSolidOn());
	}
}
