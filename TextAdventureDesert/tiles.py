import items, enemies, actions, world


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()
 
    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves
 
    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
 
        return moves


class StartingRoom(MapTile):
    # override the intro_text method in the superclass
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You remember nothing! Suddenly, you noticed there is a letter of 'N' on you right hand palm.
        You turned back, and you saw four stones next to one path.
        You can make out four paths, each equally as dark and foreboding.
        """
 
    def modify_player(self, player):
        # Room has no action on player
        pass


class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)
 
    def add_loot(self, player):
        player.inventory.append(self.item)
 
    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy), actions.Punch(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class HealthRoom(MapTile):  # Super to PotionRoom, ... maybe fountain room
    def __init__(self, x, y, health, beenThere=False):
        self.health = health
        self.beenThere = False
        super().__init__(x, y)

    def add_hp(self, player):
        if not self.beenThere:
            self.beenThere = True
            # Add room's health to player health.
            player.hp += self.health
            # hp can't be higher than max hp.
            if player.hp > player.maxHp:
                player.hp = player.maxHp
            print("HP is {}\n".format(player.hp))
            input("Press any key to continue...")

    def modify_player(self, player):
        self.add_hp(player)


class ERoom(MapTile):
    def __init__(self, x, y, enemy, item):
        self.enemy = enemy
        self.item = item
        super().__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))
            the_player.inventory.append(self.item)

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Kick(enemy=self.enemy), actions.Jump(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
 
    def modify_player(self, player):
        # Room has no action on player
        pass


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())
 
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """


class BrownBearRoom(ERoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.BrownBear(), items.Diary(1))

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant brown Bear comes after you!
            """
        else:
            return """
            The corpse of a dead Brown bear disappeared!
            """


class PolarBearRoom(ERoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.PolarBear(), items.Card(1))

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A polar Bear lays in front of you!
            """
        else:
            return """
            Small scarabs is eating the corpse.
            """


class GiantScarabRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant Scarab jumps down and stand in front of you!
            """
        else:
            return """
            The corpse of a dead Scarab rots on the ground.
            """


class GiantScorpionRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Scorpion())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant purple Scorpion surrounded by enormous scorpions!
            """
        else:
            return """
            The corpse of a dead Scarab rots on the ground.
            """


class FogRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Scorpion())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            You Slowly open the door, and what you see is a woman!
            "Kris" 
            The woman disappear in the fog, you try to stop her, but she is dissolved!
            "Who is Kris?"
            """
        else:
            return """
            You died! The last thing you remember is the space is filled with fog.
            """


class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())
 
    def intro_text(self):
        return """
        Your notice something shiny in the corner.
        It's a dagger! You pick it up.
        """


class FindGloveRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.BoxingGlove())

    def intro_text(self):
        return """
        Your notice something shiny in a pile of bloods on the Table.
        It's a pair of red boxing gloves! You pick it up and try it on.
        """


class RingRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())

    def intro_text(self):
        return """
        Once you entered the room, you hear something drop on the ground.
        You looked down, it is a silver ring slowly scrolled toward you.
        You picked it up, and you saw your name 'NK' next to 'EK' inside of the ring.
        A picture of a slender woman lay in a pile of bloods with a empty hole in her chest.
        "Eleanor Kaur!" 
        "DO I know this woman? is she my friend or MY WIFE!"
        You tried very hard to see that woman's face, but you noticed something strange 
        "WHERE IS HER HEART!!!"
        """


class AmberRoom(HealthRoom):
    def __init__(self, x, y):
        super().__init__(x, y, 50, beenThere=False)

    def intro_text(self, player):
        print("\nYou see a huge tree that surrounded by enormous graves.\n")

        if (self.health + player.hp) > player.maxHp:
            if (player.hp) >= player.maxHp:
                return """
                HP already full!
                """
            return """
                You gained {} HP!
                """.format(player.maxHp - (player.hp))

        return """
            You gained 25 HP!
                """


class CrystalRoom(HealthRoom):
    def __init__(self, x, y):
        super().__init__(x, y, 50, beenThere=False)  # 50 hp fountain

    def intro_text(self, player):
        if self.beenThere:
            return "\nA Green Book flying around.\
                    \nThe book sat on my Head!!!.\n"

        else:
            print("The book flied away.")

            if (self.health + player.hp) > player.maxHp:
                if (player.hp) >= player.maxHp:
                    return """
                    HP already full!
                    """
                return """
                    You gained {} HP!
                    """.format(player.maxHp - (player.hp))

            return """
                You gained 50 HP!
                """


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        player.victory = True
