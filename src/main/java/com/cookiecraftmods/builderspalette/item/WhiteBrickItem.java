
package com.cookiecraftmods.builderspalette.item;

import com.cookiecraftmods.builderspalette.init.RegistryObject;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.Item;

public class WhiteBrickItem extends Item {
	public WhiteBrickItem() {
		super(RegistryObject.itemSettings(new Item.Properties()).stacksTo(64).rarity(Rarity.COMMON));
	}
}
