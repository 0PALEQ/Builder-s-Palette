
package com.cookiecraftmods.builderspalette.item;

import com.cookiecraftmods.builderspalette.init.RegistryObject;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;

public class BlackBrickItem extends Item {
	public BlackBrickItem() {
		super(RegistryObject.itemSettings(new Item.Properties()).stacksTo(64).rarity(Rarity.COMMON));
	}
}
