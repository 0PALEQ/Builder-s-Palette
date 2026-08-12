package com.cookiecraftmods.builderspalette.init;

import com.cookiecraftmods.builderspalette.BuildersPaletteMod;
import java.util.function.Supplier;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.state.BlockBehaviour;

public final class RegistryObject<T> {
	private static final ThreadLocal<Identifier> ACTIVE_ID = new ThreadLocal<>();
	private final Identifier id;
	private final T value;

	private RegistryObject(Identifier id, T value) {
		this.id = id;
		this.value = value;
	}

	public static <T> RegistryObject<T> register(Registry<? super T> registry, String name, Supplier<? extends T> supplier) {
		Identifier id = Identifier.fromNamespaceAndPath(BuildersPaletteMod.MODID, name);
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

	public T get() {
		return value;
	}

	public Identifier getId() {
		return id;
	}
}
