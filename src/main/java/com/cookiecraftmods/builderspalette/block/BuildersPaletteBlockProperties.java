package com.cookiecraftmods.builderspalette.block;

import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

public final class BuildersPaletteBlockProperties {
	private BuildersPaletteBlockProperties() {
	}

	public static BlockBehaviour.Properties of() {
		return BlockBehaviour.Properties.of().mapColor(colorFor(callingBlockClassName()));
	}

	private static String callingBlockClassName() {
		StackTraceElement[] stackTrace = Thread.currentThread().getStackTrace();
		for (StackTraceElement element : stackTrace) {
			String className = element.getClassName();
			if (className.startsWith("com.cookiecraftmods.builderspalette.block.")
					&& !className.equals(BuildersPaletteBlockProperties.class.getName())) {
				int lastDot = className.lastIndexOf('.');
				return lastDot >= 0 ? className.substring(lastDot + 1) : className;
			}
		}
		return "";
	}

	private static MapColor colorFor(String className) {
		String normalizedName = className.replace("_", "").toLowerCase();

		if (normalizedName.contains("framedglass")) {
			return MapColor.COLOR_LIGHT_GRAY;
		}
		if (normalizedName.contains("asphalt") || normalizedName.contains("black")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_BLACK, MapColor.COLOR_BLACK);
		}
		if (normalizedName.contains("white") || normalizedName.contains("calcite")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_WHITE, MapColor.SNOW);
		}
		if (normalizedName.contains("lightgray") || normalizedName.contains("lightgrey")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_LIGHT_GRAY, MapColor.COLOR_LIGHT_GRAY);
		}
		if (normalizedName.contains("darkgray") || normalizedName.contains("darkgrey") || normalizedName.contains("gray") || normalizedName.contains("grey")
				|| normalizedName.contains("tuff")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_GRAY, MapColor.COLOR_GRAY);
		}
		if (normalizedName.contains("lightblue")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_LIGHT_BLUE, MapColor.COLOR_LIGHT_BLUE);
		}
		if (normalizedName.contains("deepblue") || normalizedName.contains("blue")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_BLUE, MapColor.COLOR_BLUE);
		}
		if (normalizedName.contains("green")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_GREEN, MapColor.COLOR_GREEN);
		}
		if (normalizedName.contains("yellow")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_YELLOW, MapColor.COLOR_YELLOW);
		}
		if (normalizedName.contains("orange")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_ORANGE, MapColor.COLOR_ORANGE);
		}
		if (normalizedName.contains("pink") || normalizedName.contains("peach")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_PINK, MapColor.COLOR_PINK);
		}
		if (normalizedName.contains("purple")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_PURPLE, MapColor.COLOR_PURPLE);
		}
		if (normalizedName.contains("brown") || normalizedName.contains("packedmud") || normalizedName.contains("mud") || normalizedName.contains("wenge")
				|| normalizedName.contains("coffewood")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_BROWN, MapColor.COLOR_BROWN);
		}
		if (normalizedName.contains("darkred") || normalizedName.contains("red") || normalizedName.contains("scarlett") || normalizedName.contains("bricks")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_RED, MapColor.COLOR_RED);
		}
		if (normalizedName.contains("lightoak")) {
			return MapColor.WOOD;
		}
		if (normalizedName.contains("endstone")) {
			return MapColor.SAND;
		}
		if (normalizedName.contains("terracotta")) {
			return MapColor.TERRACOTTA_ORANGE;
		}
		if (normalizedName.contains("leaves")) {
			return MapColor.PLANT;
		}
		return MapColor.STONE;
	}

	private static MapColor terracottaOrColor(String normalizedName, MapColor terracottaColor, MapColor fallbackColor) {
		return normalizedName.contains("terracotta") ? terracottaColor : fallbackColor;
	}
}
