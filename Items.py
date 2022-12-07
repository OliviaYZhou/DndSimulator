class Item:
    """

    """
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

class Food(Item):
    def __init__(self, name, description, value):
        super().__init__(name, description, value)

class Consumable(Item):
    def __init__(self, name, description, value):
        super().__init__(name, description, value)

class Equipment(Item):
    def __init__(self, description, value, modifier, equipment_type):
        super().__init__(description, value, modifier)
        self.equipment_type = equipment_type
