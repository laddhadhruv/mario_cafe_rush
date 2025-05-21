from core.item import Item

class Croissant(Item):
    def __init__(self, filled=False):
        super().__init__(f"{'filled' if filled else 'plain'}_croissant") # Unique ID
        self.filled = filled
        self.description = f"{'filled' if filled else 'plain'} croissant"

    def get_description(self):
        return self.description

class Bread(Item):
    def __init__(self, toasted=False):
        super().__init__(f"{'toasted' if toasted else 'untoasted'}_bread") # Unique ID
        self.toasted = toasted
        self.description = f"{'toasted' if toasted else 'untoasted'} bread"

    def get_description(self):
        return self.description

class Egg(Item):
    def __init__(self, style="scrambled"):
        super().__init__(f"{style}_egg") # Unique ID
        self.style = style # scrambled, boiled, omelette
        self.description = f"{style} egg"

    def get_description(self):
        return self.description

class Bacon(Item):
    def __init__(self, cooking_style="soft"):
        super().__init__(f"{cooking_style}_bacon") # Unique ID
        self.cooking_style = cooking_style # soft, crispy
        self.description = f"{cooking_style} bacon"

    def get_description(self):
        return self.description

class Coffee(Item):
    def __init__(self, coffee_type="espresso"):
        # Ensure coffee_type is part of the ID for uniqueness if multiple Coffee items are instantiated
        super().__init__(f"{coffee_type}_drink") # Potentially conflicting with Espresso item ID 'espresso'
        self.coffee_type = coffee_type # espresso, americano, cortado, cappuccino, latte
        self.description = coffee_type

    def get_description(self):
        return self.description 