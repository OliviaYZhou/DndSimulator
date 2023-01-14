class Item:
    """
    Things to put in the bag. Not necessarily useful.
    """
    def __init__(self, name, description, value):
        """

        :param name: Item name
        :param description: item description
        :param value: Market value of item. Sale price will vary based on charisma.
        """
        self.name = name
        self.description = description
        self.value = value

class Consumable(Item):
    def __init__(self, name, description, value, effect):
        """
        :param effect: list tuple [(effected stat, effect size, over turns)] eg [[hp, 2, 5], [mp, -5, 1]]
        """
        super().__init__(name, description, value)
        self.effect = effect

class Food(Consumable):
    def __init__(self, name, description, value, effect, hunger):
        """
        :param hunger: amount of hunger recovered
        """
        super().__init__(name, description, value, effect)
        self.hunger = hunger

class Equipment(Item):
    def __init__(self, name, description, value, equipment_type, modifier):
        """
        :param equipment_type: Type of equipment. from [helmet, armor, shoes, weapon, top, bot, accessories]
        :param modifier: stats modified. {def: 20, magic_def: 30, hp:20, mp:-5, charisma: 99}
        """
        super().__init__(name, description, value)
        self.equipment_type = equipment_type
        self.modifier = modifier
