class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage
 
    def is_alive(self):
        return self.hp > 0


class GiantSpider(Enemy):
    def __init__(self):
        super().__init__(name="Giant Spider", hp=10, damage=2)


class Ogre(Enemy):
    def __init__(self):
        super().__init__(name="Ogre", hp=30, damage=15)


class Camel(Enemy):
    def __init__(self):
        super().__init__(name="Dog", hp=20, damage=10)


class Scarab(Enemy):
    def __init__(self):
        super().__init__(name="Scarab", hp=15, damage=15)


class PolarBear(Enemy):
    def __init__(self):
        super().__init__(name="Polar Bear", hp=100, damage=40)


class BrownBear(Enemy):
    def __init__(self):
        super().__init__(name="Brown bear", hp=80, damage=20)


class Scorpion(Enemy):
    def __init__(self):
        super().__init__(name="Brown bear", hp=50, damage=14)


class GiantCat(Enemy):
    def __init__(self):
        super().__init__(name="Giant Cat", hp=10, damage=20)


class Fog(Enemy):
    def __init__(self):
        super().__init__(name="Fog", hp=10, damage=100)
