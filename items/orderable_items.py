from core.item import Item

class Croissant(Item):
    def __init__(self, filled=False):
        super().__init__(f"{'filled' if filled else 'plain'}_croissant")
        self.filled     = filled
        self.description= f"{'filled' if filled else 'plain'} croissant"
        self.section    = "bakery"      # ← allow dropping only in bakery
        self.set_is_generator(True)

    def get_description(self):
        return self.description

    def reset_to_default_state(self):
        self.set_is_generator(False)


class Bread(Item):
    def __init__(self, toasted=False):
        super().__init__(f"{'toasted' if toasted else 'untoasted'}_bread")
        self.toasted    = toasted
        self.description= f"{'toasted' if toasted else 'untoasted'} bread"
        self.section    = "bakery"
        self.set_is_generator(True)

    def get_description(self):
        return self.description

    def reset_to_default_state(self):
        self.set_is_generator(False)


class Egg(Item):
    def __init__(self, style="scrambled"):
        super().__init__(f"{style}_egg")
        self.style      = style
        self.description= f"{style} egg"
        self.section    = "kitchen"     # ← allow dropping only in kitchen
        self.set_is_generator(True)

    def get_description(self):
        return self.description

    def reset_to_default_state(self):
        self.set_is_generator(False)


class Bacon(Item):
    def __init__(self, cooking_style="soft"):
        super().__init__(f"{cooking_style}_bacon")
        self.cooking_style = cooking_style
        self.description   = f"{cooking_style} bacon"
        self.section       = "kitchen"
        self.set_is_generator(True)

    def get_description(self):
        return self.description

    def reset_to_default_state(self):
        self.set_is_generator(False)


class Coffee(Item):
    def __init__(self, coffee_type="espresso"):
        super().__init__(f"{coffee_type}_drink")
        self.coffee_type = coffee_type
        self.description = coffee_type
        self.section     = "coffeebar"  # ← allow dropping only in coffee bar

    def get_description(self):
        return self.description
