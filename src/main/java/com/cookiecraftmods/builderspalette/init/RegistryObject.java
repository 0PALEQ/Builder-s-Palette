package com.cookiecraftmods.builderspalette.init;

import com.cookiecraftmods.builderspalette.BuildersPaletteMod;
import net.minecraft.registry.Registry;
import net.minecraft.registry.RegistryKey;
import net.minecraft.registry.RegistryKeys;
import net.minecraft.block.AbstractBlock;
import net.minecraft.item.Item;
import net.minecraft.util.Identifier;

import java.util.function.Supplier;

public final class RegistryObject<T> {
	private static final ThreadLocal<Identifier> ACTIVE_ID = new ThreadLocal<>();
	private final Identifier id;
	private final T value;

	private RegistryObject(Identifier id, T value) {
		this.id = id;
		this.value = value;
	}

	public static <T> RegistryObject<T> register(Registry<? super T> registry, String name, Supplier<? extends T> supplier) {
		Identifier id = Identifier.of(BuildersPaletteMod.MODID, name);
		if (ACTIVE_ID.get() != null) {
			throw new IllegalStateException("Nested registry construction is not supported");
		}
		T value;
		ACTIVE_ID.set(id);
		try {
			value = supplier.get();
		} finally {
			ACTIVE_ID.remove();
		}
		Registry.register(registry, id, value);
		return new RegistryObject<>(id, value);
	}

	public static AbstractBlock.Settings blockSettings(AbstractBlock.Settings settings) {
		return settings.registryKey(RegistryKey.of(RegistryKeys.BLOCK, activeId()));
	}

	public static Item.Settings itemSettings(Item.Settings settings) {
		return settings.registryKey(RegistryKey.of(RegistryKeys.ITEM, activeId()));
	}

	public static Item.Settings blockItemSettings(Item.Settings settings) {
		return itemSettings(settings).useBlockPrefixedTranslationKey();
	}

	private static Identifier activeId() {
		Identifier id = ACTIVE_ID.get();
		if (id == null) {
			throw new IllegalStateException("Settings must be created inside RegistryObject.register");
		}
		return id;
	}

	public T get() {
		return value;
	}

	public Identifier getId() {
		return id;
	}
}
