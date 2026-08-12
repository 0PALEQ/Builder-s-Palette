
package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.IronBarsBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;

public class FramedGlassBlock extends IronBarsBlock {
	public FramedGlassBlock() {
		super(BuildersPaletteBlockProperties.of().instrument(NoteBlockInstrument.BASEDRUM).sound(SoundType.GLASS).strength(1f, 10f).noOcclusion().isRedstoneConductor((bs, br, bp) -> false));
	}
}
