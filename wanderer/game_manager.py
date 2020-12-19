from random import randrange
from area2 import Area
from hero import Hero
from skeleton import Skeleton
from boss import Boss

class Game:

    def __init__(self):
        self.hero = Hero()

    def create_characters(self):
        characters = []
        characters.append(self.hero)
        monsters = self.create_monsters()
        for i in range(0, len(monsters)):
            characters.append(monsters[i])
        return characters

    def create_monsters(self):
        monsters = []
        boss = Boss()
        monsters.append(boss)
        skeletons = []
        skeleton_number = randrange(2, 5)
        for i in range(skeleton_number):
            skeletons.append(Skeleton('Skeleton ' + str(i + 1)))
        skeletons[0].has_key == True
        for i in range(0, len(skeletons)):
            monsters.append(skeletons[i])
        return monsters

    def get_stats(self, characters):
        for character in characters:
            print(character.introduce())

    def get_tile_stats(self, tile):
        print(tile.walkable)
        print(tile.has_hero)
        print(tile.has_monster)

    def set_free_tiles(self, area):
        area.free_tiles = []
        for tile in area.tiles.values():
            #self.get_tile_stats(tile)
            if tile.walkable == True and tile.has_hero == False and tile.has_monster == False:
                area.free_tiles.append((tile, tile.x, tile.y))

    def spawn_characters(self, area, canvas, hero, monsters):
        area.character_images = {}
        self.spawn_hero(area, canvas, hero)
        self.spawn_monsters(area, canvas, monsters)

    def spawn_hero(self, area, canvas, hero):
        self.set_free_tiles(area)
        hero.image_path = hero.image_down
        area.draw_character(canvas, hero)
        tile = area.tiles[0]
        tile.has_hero = True

    def spawn_monsters(self, area, canvas, monsters):
        for monster in monsters:
            self.set_free_tiles(area)
            tile = area.free_tiles[randrange(len(area.free_tiles))]
            monster.y = tile[1]
            monster.x = tile[2]
            area.draw_character(canvas, monster)
            tile[0].has_monster = True

    def set_hero_position(self, area, canvas, hero, direction):
        hero.turn(direction)
        area.draw_character(canvas, hero)
        destination_x, destination_y = self.calculate_destination(hero, direction)
        is_wall = self.check_walls(area, destination_x, destination_y)
        if is_wall == True:
            print('Ouch! Watch where you are going!')
            return
        if (destination_x >= 0 and destination_x < area.area_size
            and destination_y >= 0 and destination_y < area.area_size):
            #for tile in area.tiles:
                #tile.has_hero = False
                #if tile.x == destination_x and tile.y == destination_y:
                    #tile.has_hero = True
            hero.x, hero.y = destination_x, destination_y
            area.draw_character(canvas, hero)
        else:
            print('The edge has been reached!')
            return

    def set_monster_position(self, area, canvas, monster, direction):
        destination_x, destination_y = self.calculate_destination(monster, direction)
        is_wall = self.check_walls(area, destination_x, destination_y)
        if is_wall == True:
            dir = 'down' #change so it works
            self.set_monster_position(area, canvas, monster, dir)
        if (destination_x >= 0 and destination_x < area.area_size
            and destination_y >= 0 and destination_y < area.area_size):
            #for tile in area.tiles:
                #tile.has_monster = False
                #if tile.x == destination_x and tile.y == destination_y:
                    #tile.has_monster = True
            monster.x, monster.y = destination_x, destination_y
        else:
            dir = 'down' #change so it works
            self.set_monster_position(area, canvas, monster, dir)

    def calculate_destination(self, character, direction):
        if direction == 'up':
            x = character.x
            y = character.y - 72
        elif direction == 'down':
            x = character.x
            y = character.y + 72
        elif direction == 'right':
            y = character.y
            x = character.x + 72
        elif direction == 'left':
            y = character.y
            x = character.x -72
        else:
            y = character.y
            x = character.x
        return (x, y)

    def check_walls(self, area, destination_x, destination_y):
        if (((destination_y * area.number_of_tiles) / area.tile_size) +
            (destination_x / area.tile_size) in area.walls):
            return True
        else:
            return False

    def check_other_characters(self, character, characters):
        for char in characters:
            pass
        #check for other characters
        #character.step(direction)
        #if hero x monster -> fight

    def check_fight(self, attacker, defender):
        if attacker.on_tile == defender.on_tile:
            self.fight(attacker, defender)

    def fight(self, attacker, defender):
        while attacker.current_health > 0 and defender.current_health > 0:
            attacker.hit(defender)
            defender.check_death()
            #prevent defender to hit after it died
            defender.hit(attacker)
            attacker.check_death()
        if attacker.current_health <= 0:
            self.kill(attacker)
        else:
            self.kill(defender)

    def kill(self, character):
        del character

    def check_next_area(self, area, canvas, characters):
        if characters[1].__class__() == "Boss":
            return
        for skeleton in characters[2:]:
            if skeleton.has_key == True:
                return
        self.next_area(area, canvas, characters)

    def next_area(self, area, canvas, characters):
        hero = self.hero
        monsters = characters[1:]
        self.clear_area(monsters)
        area.number += 1
        self.create_characters()
        new_monsters = characters[1:]
        self.spawn_characters(area, canvas, hero, new_monsters)

    def clear_area(self, monsters):
        for monster in monsters:
            del monster
