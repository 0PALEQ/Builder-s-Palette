package com.cookiecraftmods.builderspalette;

import com.cookiecraftmods.builderspalette.init.BuildersPaletteModBlocks;
import com.cookiecraftmods.builderspalette.init.BuildersPaletteModItems;
import com.cookiecraftmods.builderspalette.init.BuildersPaletteModTabs;
import com.mojang.logging.LogUtils;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.core.registries.Registries;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import org.slf4j.Logger;

@Mod(BuildersPaletteMod.MODID)
public final class BuildersPaletteMod {
    public static final String MODID = "builders_palette";
    public static final Logger LOGGER = LogUtils.getLogger();

    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, MODID);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, MODID);
    public static final DeferredRegister<CreativeModeTab> CREATIVE_TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MODID);

    public BuildersPaletteMod() {
        BuildersPaletteModBlocks.register();
        BuildersPaletteModItems.register();
        BuildersPaletteModTabs.register();

        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        CREATIVE_TABS.register(modBus);
    }
}
