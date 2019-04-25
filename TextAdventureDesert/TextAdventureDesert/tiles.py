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
        You can't remember anything no matter how hard you try.
        You heard someone singing or something is making the noise!
        Suddenly, there is a water drop on the tip of your nose. 
        You thought of "am I under the ocean?, but wait, what does ocean mean?" 
        In less than five minutes, three walls of the caves starting pushing forward. You have to make your decision, quick!
        You can make out four paths, each equally as dark and foreboding.
        """
 
    def modify_player(self, player):
        # Room has no action on player
        pass


class HealthRoom(MapTile):
    def __init__(self, x, y, health, beenThere = False):
        self.health = health
        self.beenThere = False
        super().__init__(x, y)

    def add_hp(self, player):
        if not self.beenThere:
            self.beenThere = True
            #Add room's health to player health.
            player.hp += self.health
            #hp can't be higher than max hp.
            if player.hp > player.maxHp:
                player.hp = player.maxHp
            print("HP is {}\n".format(player.hp))
            input("Press any key to continue...")

    def modify_player(self, player):
        self.add_hp(player)


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


class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
 
    def modify_player(self, player):
        #Room has no action on player
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


class BrownBearRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.BrownBear())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant brown Bear comes after you!
            """
        else:
            return """
            The corpse of a dead Brown bear disappeared!
            """


class PolarBearRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.PolarBear())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A polar Bear lays in front of you!
            """
        else:
            return """
            Small scarabs is eating the corpse. You saw something on the wall, it said, "NO ONE CAN ESCAPE!" Suddenly, you hear something.
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
            You find a black man watch and it stops at 12:00AM. Then you pick it up.
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


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        player.victory = True
