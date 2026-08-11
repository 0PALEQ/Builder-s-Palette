package com.cookiecraftmods.builderspalette.init;

import com.cookiecraftmods.builderspalette.BuildersPaletteMod;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.resources.ResourceLocation;

import java.util.function.Supplier;

/**
 * Small compatibility wrapper that keeps the generated catalog source stable
 * while delegating registration to Forge's deferred registries.
 */
public final class RegistryObject<T> implements Supplier<T> {
    private final Supplier<? extends T> delegate;
    private final ResourceLocation id;

    private RegistryObject(Supplier<? extends T> delegate, ResourceLocation id) {
        this.delegate = delegate;
        this.id = id;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    public static <T> RegistryObject<T> register(Registry<? super T> registry, String name,
            Supplier<? extends T> supplier) {
        Supplier<? extends T> value;
        if (registry == BuiltInRegistries.BLOCK) {
            value = BuildersPaletteMod.BLOCKS.register(name, (Supplier) supplier);
        } else if (registry == BuiltInRegistries.ITEM) {
            value = BuildersPaletteMod.ITEMS.register(name, (Supplier) supplier);
        } else if (registry == BuiltInRegistries.CREATIVE_MODE_TAB) {
            value = BuildersPaletteMod.CREATIVE_TABS.register(name, (Supplier) supplier);
        } else {
            throw new IllegalArgumentException("Unsupported registry for builders_palette:" + registry.key().location());
        }
        return new RegistryObject<>(value, ResourceLocation.fromNamespaceAndPath(BuildersPaletteMod.MODID, name));
    }

    @Override
    public T get() {
        return delegate.get();
    }

    public ResourceLocation getId() {
        return id;
    }
}
