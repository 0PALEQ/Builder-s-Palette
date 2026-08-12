
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;

public class OrangeSmoothTerracottaSlabBlock extends SlabBlock {
	public OrangeSmoothTerracottaSlabBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(NoteBlockInstrument.BASEDRUM).sound(SoundType.STONE).strength(1f, 10f));
	}
}
