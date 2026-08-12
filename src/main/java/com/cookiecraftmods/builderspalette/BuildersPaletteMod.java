package com.cookiecraftmods.builderspalette;

import com.cookiecraftmods.builderspalette.init.BuildersPaletteModBlocks;
import com.cookiecraftmods.builderspalette.init.BuildersPaletteModItems;
import com.cookiecraftmods.builderspalette.init.BuildersPaletteModTabs;
import com.mojang.logging.LogUtils;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.registries.DeferredRegister;
import org.slf4j.Logger;

@Mod(BuildersPaletteMod.MODID)
public final class BuildersPaletteMod {
    public static final String MODID = "builders_palette";
    public static final Logger LOGGER = LogUtils.getLogger();

    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(Registries.BLOCK, MODID);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(Registries.ITEM, MODID);
    public static final DeferredRegister<CreativeModeTab> CREATIVE_TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    public BuildersPaletteMod(IEventBus modBus) {
        BuildersPaletteModBlocks.register();
        BuildersPaletteModItems.register();
        BuildersPaletteModTabs.register();

        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        CREATIVE_TABS.register(modBus);
    }
}
