
package com.cookiecraftmods.builderspalette.item;

import com.cookiecraftmods.builderspalette.init.RegistryObject;
import net.minecraft.util.Rarity;
import net.minecraft.item.Item;

public class BlackBrickItem extends Item {
	public BlackBrickItem() {
		super(RegistryObject.itemSettings(new Item.Settings()).maxCount(64).rarity(Rarity.COMMON));
	}
}
