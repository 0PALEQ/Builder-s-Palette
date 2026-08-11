package com.cookiecraftmods.builderspalette;

import com.cookiecraftmods.builderspalette.init.BuildersPaletteModBlocks;
import com.cookiecraftmods.builderspalette.init.BuildersPaletteModItems;
import com.cookiecraftmods.builderspalette.init.BuildersPaletteModTabs;
import net.fabricmc.api.ModInitializer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class BuildersPaletteMod implements ModInitializer {
	public static final Logger LOGGER = LogManager.getLogger(BuildersPaletteMod.class);
	public static final String MODID = "builders_palette";
	public void onInitialize() {
		BuildersPaletteModBlocks.register();
		BuildersPaletteModItems.register();
		BuildersPaletteModTabs.register();
	}
}
