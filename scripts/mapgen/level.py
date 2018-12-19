import pygame

from scripts.mapgen.ascii import ascii
from scripts.objects.obstacles import Obstacle
from scripts.objects.obstacles import Door
from scripts.objects.objects import Fog
from scripts.objects.characters import Spawner
from scripts.objects.moving_objects import Block
from scripts.objects.characters import Player
from root import root


class Level(object):
    """Instantiate a level object that can be written on to."""
    def __init__(self, open_level):
        text_map = root + "/level/" + open_level + ".txt"
        self.level1 = []
        self.world = []
        self.player1 = None
        self.monster_list = []
        self.spawner_list = []
        self.power_min = 0
        self.power_max = 5
        self.projectiles = []
        self.one_square = 25
        self.max_monsters = 0
        self.all_sprite = pygame.sprite.Group()
        self.fog_sprites = pygame.sprite.Group()
        self.level = open(text_map, "r")

    def create_level(self, x, y, one_square):
        """Read an ascii map generated by the Map class and create that
           level. The level's details will be stored in the instance of this
           class."""
        for l in self.level:
            self.level1.append(l)

        for row in self.level1:
            for col in row:
                if col == ascii['Player1']:
                    self.player1 = Player('Player1', x, y, one_square, light_r=5)
                else:
                    fog = Fog(x, y, 'NoGo')
                    self.fog_sprites.add(fog)
                if col == ascii['Block']:
                    block = Block(x, y)
                    self.world.append(block)
                    self.all_sprite.add(block)
                elif col == ascii['Door']:
                    door = Door(x, y)
                    self.world.append(door)
                    self.all_sprite.add(door)
                elif col == ascii['Wall']:
                    wall = Obstacle(x, y, 'Wall')
                    self.world.append(wall)
                    self.all_sprite.add(wall)
                elif col == ascii['CastleWall']:
                    wall = Obstacle(x, y, 'CastleWall')
                    self.world.append(wall)
                    self.all_sprite.add(wall)
                elif col == ascii['Spawner']:
                    spawner = Spawner(x, y, 'Spawner', one_square, rate=2)
                    self.spawner_list.append(spawner)
                    self.all_sprite.add(spawner)
                    self.max_monsters += 3
                x += one_square
            y += one_square
            x = 0
        self.all_sprite.add(self.player1)
        self.world.append(self.player1)

    def get_size(self):
        """Gets the size of the level."""
        lines = self.level1
        line = max(lines, key=len)
        self.width = (len(line))*25
        self.height = (len(lines))*25
        return self.width, self.height
