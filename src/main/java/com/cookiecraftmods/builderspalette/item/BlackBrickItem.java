
package com.cookiecraftmods.builderspalette.item;

import net.minecraft.util.Rarity;
import net.minecraft.item.Item;

public class BlackBrickItem extends Item {
	public BlackBrickItem() {
		super(new Item.Settings().maxCount(64).rarity(Rarity.COMMON));
	}
}
