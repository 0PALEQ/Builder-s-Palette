
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;

public class PurpleSmoothTerracottaSlabBlock extends SlabBlock {
	public PurpleSmoothTerracottaSlabBlock() {
		super(BuildersPaletteBlockProperties.of().sound(SoundType.STONE).strength(1f, 10f));
	}
}
