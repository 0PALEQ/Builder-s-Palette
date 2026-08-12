package com.cookiecraftmods.builderspalette.init;

import com.cookiecraftmods.builderspalette.BuildersPaletteMod;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.state.BlockBehaviour;

import java.util.function.Supplier;

/**
 * Keeps the generated catalog source loader-neutral while delegating object
 * creation to NeoForge's deferred registries.
 */
public final class RegistryObject<T> implements Supplier<T> {
    private static final ThreadLocal<Identifier> ACTIVE_ID = new ThreadLocal<>();
    private final Supplier<? extends T> delegate;
    private final Identifier id;

    private RegistryObject(Supplier<? extends T> delegate, Identifier id) {
        this.delegate = delegate;
        this.id = id;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    public static <T> RegistryObject<T> register(Registry<? super T> registry, String name,
            Supplier<? extends T> supplier) {
        Identifier id = Identifier.fromNamespaceAndPath(BuildersPaletteMod.MODID, name);
        Supplier<? extends T> keyedSupplier = () -> {
            if (ACTIVE_ID.get() != null) {
                throw new IllegalStateException("Nested registry construction is not supported");
            }
            ACTIVE_ID.set(id);
            try {
                return supplier.get();
            } finally {
                ACTIVE_ID.remove();
            }
        };
        Supplier<? extends T> value;
        if (registry == BuiltInRegistries.BLOCK) {
            value = BuildersPaletteMod.BLOCKS.register(name, (Supplier) keyedSupplier);
        } else if (registry == BuiltInRegistries.ITEM) {
            value = BuildersPaletteMod.ITEMS.register(name, (Supplier) keyedSupplier);
        } else if (registry == BuiltInRegistries.CREATIVE_MODE_TAB) {
            value = BuildersPaletteMod.CREATIVE_TABS.register(name, (Supplier) keyedSupplier);
        } else {
            throw new IllegalArgumentException("Unsupported registry for builders_palette: " + registry.key().identifier());
        }
        return new RegistryObject<>(value, id);
    }

    public static BlockBehaviour.Properties blockSettings(BlockBehaviour.Properties settings) {
        return settings.setId(ResourceKey.create(Registries.BLOCK, activeId()));
    }

    public static Item.Properties itemSettings(Item.Properties settings) {
        return settings.setId(ResourceKey.create(Registries.ITEM, activeId()));
    }

    public static Item.Properties blockItemSettings(Item.Properties settings) {
        return itemSettings(settings).useBlockDescriptionPrefix();
    }

    private static Identifier activeId() {
        Identifier id = ACTIVE_ID.get();
        if (id == null) {
            throw new IllegalStateException("Settings must be created inside RegistryObject.register");
        }
        return id;
    }

    @Override
    public T get() {
        return delegate.get();
    }

    public Identifier getId() {
        return id;
    }
}
