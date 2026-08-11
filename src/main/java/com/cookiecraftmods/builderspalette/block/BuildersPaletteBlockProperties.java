package com.cookiecraftmods.builderspalette.block;

import com.cookiecraftmods.builderspalette.init.RegistryObject;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.MapColor;

public final class BuildersPaletteBlockProperties {
	private BuildersPaletteBlockProperties() {
	}

	public static AbstractBlock.Settings of() {
		return RegistryObject.blockSettings(AbstractBlock.Settings.create())
				.mapColor(colorFor(callingBlockClassName()));
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
			return MapColor.LIGHT_GRAY;
		}
		if (normalizedName.contains("asphalt") || normalizedName.contains("black")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_BLACK, MapColor.BLACK);
		}
		if (normalizedName.contains("white") || normalizedName.contains("calcite")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_WHITE, MapColor.WHITE);
		}
		if (normalizedName.contains("lightgray") || normalizedName.contains("lightgrey")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_LIGHT_GRAY, MapColor.LIGHT_GRAY);
		}
		if (normalizedName.contains("darkgray") || normalizedName.contains("darkgrey") || normalizedName.contains("gray") || normalizedName.contains("grey")
				|| normalizedName.contains("tuff")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_GRAY, MapColor.GRAY);
		}
		if (normalizedName.contains("lightblue")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_LIGHT_BLUE, MapColor.LIGHT_BLUE);
		}
		if (normalizedName.contains("deepblue") || normalizedName.contains("blue")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_BLUE, MapColor.BLUE);
		}
		if (normalizedName.contains("green")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_GREEN, MapColor.GREEN);
		}
		if (normalizedName.contains("yellow")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_YELLOW, MapColor.YELLOW);
		}
		if (normalizedName.contains("orange")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_ORANGE, MapColor.ORANGE);
		}
		if (normalizedName.contains("pink") || normalizedName.contains("peach")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_PINK, MapColor.PINK);
		}
		if (normalizedName.contains("purple")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_PURPLE, MapColor.PURPLE);
		}
		if (normalizedName.contains("brown") || normalizedName.contains("packedmud") || normalizedName.contains("mud") || normalizedName.contains("wenge")
				|| normalizedName.contains("coffewood")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_BROWN, MapColor.BROWN);
		}
		if (normalizedName.contains("darkred") || normalizedName.contains("red") || normalizedName.contains("scarlett") || normalizedName.contains("bricks")) {
			return terracottaOrColor(normalizedName, MapColor.TERRACOTTA_RED, MapColor.RED);
		}
		if (normalizedName.contains("lightoak")) {
			return MapColor.OAK_TAN;
		}
		if (normalizedName.contains("endstone")) {
			return MapColor.PALE_YELLOW;
		}
		if (normalizedName.contains("terracotta")) {
			return MapColor.TERRACOTTA_ORANGE;
		}
		if (normalizedName.contains("leaves")) {
			return MapColor.DARK_GREEN;
		}
		return MapColor.STONE_GRAY;
	}

	private static MapColor terracottaOrColor(String normalizedName, MapColor terracottaColor, MapColor fallbackColor) {
		return normalizedName.contains("terracotta") ? terracottaColor : fallbackColor;
	}
}
