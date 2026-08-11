
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.block.enums.NoteBlockInstrument;
import net.minecraft.block.AbstractBlock;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.block.SlabBlock;

public class OrangeSmoothTerracottaSlabBlock extends SlabBlock {
	public OrangeSmoothTerracottaSlabBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(NoteBlockInstrument.BASEDRUM).sounds(BlockSoundGroup.STONE).strength(1f, 10f));
	}
}
