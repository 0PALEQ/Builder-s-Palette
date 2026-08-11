package com.cookiecraftmods.builderspalette.init;

import com.cookiecraftmods.builderspalette.BuildersPaletteMod;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

import java.util.function.Supplier;

public final class RegistryObject<T> {
	private final Identifier id;
	private final T value;

	private RegistryObject(Identifier id, T value) {
		this.id = id;
		this.value = value;
	}

	public static <T> RegistryObject<T> register(Registry<? super T> registry, String name, Supplier<? extends T> supplier) {
		Identifier id = new Identifier(BuildersPaletteMod.MODID, name);
		T value = supplier.get();
		Registry.register(registry, id, value);
		return new RegistryObject<>(id, value);
	}

	public T get() {
		return value;
	}

	public Identifier getId() {
		return id;
	}
}
