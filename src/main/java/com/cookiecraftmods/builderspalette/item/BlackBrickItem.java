
package com.cookiecraftmods.builderspalette.item;

import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.Item;

public class BlackBrickItem extends Item {
	public BlackBrickItem() {
		super(new Item.Properties().stacksTo(64).rarity(Rarity.COMMON));
	}
}
