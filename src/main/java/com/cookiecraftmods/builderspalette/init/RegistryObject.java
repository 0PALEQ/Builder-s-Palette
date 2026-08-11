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
    private final net.minecraftforge.registries.RegistryObject<? extends T> delegate;

    private RegistryObject(net.minecraftforge.registries.RegistryObject<? extends T> delegate) {
        this.delegate = delegate;
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    public static <T> RegistryObject<T> register(Registry<? super T> registry, String name,
            Supplier<? extends T> supplier) {
        net.minecraftforge.registries.RegistryObject<? extends T> value;
        if (registry == BuiltInRegistries.BLOCK) {
            value = (net.minecraftforge.registries.RegistryObject) BuildersPaletteMod.BLOCKS.register(name, (Supplier) supplier);
        } else if (registry == BuiltInRegistries.ITEM) {
            value = (net.minecraftforge.registries.RegistryObject) BuildersPaletteMod.ITEMS.register(name, (Supplier) supplier);
        } else if (registry == BuiltInRegistries.CREATIVE_MODE_TAB) {
            value = (net.minecraftforge.registries.RegistryObject) BuildersPaletteMod.CREATIVE_TABS.register(name, (Supplier) supplier);
        } else {
            throw new IllegalArgumentException("Unsupported registry for builders_palette:" + registry.key().location());
        }
        return new RegistryObject<>(value);
    }

    @Override
    public T get() {
        return delegate.get();
    }

    public ResourceLocation getId() {
        return delegate.getId();
    }
}
