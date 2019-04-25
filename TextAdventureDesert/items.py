﻿# Base class for all items
class Item:
    # __init__ is the contructor method
    def __init__(self, name, description, value):
        self.name = name   # attribute of the Item class and any subclasses
        self.description = description # attribute of the Item class and any subclasses
        self.value = value  # attribute of the Item class and any subclasses
    
    # __str__ method is used to print the object
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description, self.value)

# Extend the Items class
# Gold class will be a child or subclass of the superclass Item


class Gold(Item):
    # __init__ is the contructor method
    def __init__(self, amt): 
        self.amt = amt  # attribute of the Gold class
        super().__init__(name="Gold",
                         description="A round coin with {} stamped on the front.".format(str(self.amt)),
                         value=self.amt)


class Potions(Item):
    def __init__(self, name, description, value, amt, health):
        self.amt = amt # how many of the potions you have
        self.health = health # how much hp it heals

        super().__init__(name, description, value)


class APotion(Potions):
    def __init__(self):
        super().__init__(name="A",
                         description="'A' is a potion that restore 25 health points. It is stink!",
                         value=5,
                         amt=1,
                         health=25)

    def __str__(self):
        return "{}\n=====\n{} \nValue: {}\nAmount: {}".format(self.name, self.description, self.value, self.amt)


class Rope(Item):
    # __init__ is the contructor method
    def __init__(self, amt):
        self.amt = amt  # attribute of the HealthPotion class
        super().__init__(name="Rope",
                         description="A rope".format(str(self.amt)),
                         value=self.amt)


class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super().__init__(name, description, value)
 
    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(self.name, self.description, self.value, self.damage)


class Rock(Weapon):
    def __init__(self):
        super().__init__(name="Rock",
                         description="A fist-sized rock, suitable for bludgeoning.",
                         value=0,
                         damage=5)


class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Dagger",
                         description="A small dagger with some rust. Somewhat more dangerous than a rock.",
                         value=10,
                         damage=10)


class BoxingGlove(Weapon):
    def __init__(self):
        super().__init__(name="Boxing Glove",
                         description="A pair of red boxing glove.",
                         value=8,
                         damage=10)
