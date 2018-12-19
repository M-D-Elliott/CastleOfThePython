import pygame
from pygame.locals import *
from pygame.locals import Rect
import sys
from time import time
import random

from scripts.mapgen.level import Level
from scripts.databases.MonsterDBInitializer import MonsterDB
from scripts.floorbuild.randfloor import random_diamond_floor
# from scripts.windows.text_window import TextWindow
from scripts.windows.draw_text import draw_text
from root import root

screen_x = 800
screen_y = 600
SCREEN_SIZE = (screen_x, screen_y)  # resolution of the game
one_square = 25
x_center = screen_x / 2
y_center = screen_y / 2

global FPS
# global clock
global time_spent


def rel_rect(actor, campy):
    return pygame.Rect(actor.rect.x-campy.rect.x, actor.rect.y-campy.rect.y,
                       actor.rect.w, actor.rect.h)


class Camera(object):
    """This class dynamically keeps the screen on the player. The player is
       is given minor freedom of movement apart from the camera, however."""
    def __init__(self, screen_arg, player_arg, level_width, level_height):
        self.player = player_arg
        self.rect = screen_arg.get_rect()
        self.rect.center = self.player.topright
        self.world_rect = Rect(0, 0, level_width, level_height)
        # self.fog_rect = Rect(0, 0, level_width, level_height)

    def update(self):
        if self.player.centerx > self.rect.centerx + 150:
            self.rect.centerx += 25
        if self.player.centerx < self.rect.centerx - 150:
            self.rect.centerx -= 25
        if self.player.centery > self.rect.centery + 150:
            self.rect.centery += 25
        if self.player.centery < self.rect.centery - 150:
            self.rect.centery -= 25
        self.rect.clamp_ip(self.world_rect)
        # self.rect.clamp_ip(self.fog_rect)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, rel_rect(s, self))


def tps(orologio, fps):
    """This method defines the global tick speed for the game."""
    temp = orologio.tick(fps)
    temp_ps = temp / 1000.
    return temp_ps


def move_delay(start_t):
    """This method creates a delay before auto_repeat begins.."""
    if (time() - start_t) >= input_delay:
        bool_switch: bool = True
    else:
        bool_switch: bool = False
    return bool_switch


# start pygame.
pygame.init()
"""Below the basic factors of the pygame screen and camera are established.
   Also the level class from the objects script is called and filled with the
   txt file generated by the mapgen script."""

#  the pygame screen is established and filled with a rect. then the BG is loaded.
screen = pygame.display.set_mode(SCREEN_SIZE, 32)
screen_rect = screen.get_rect()
background = pygame.image.load(root + "/world/Background.png").convert_alpha()
background_rect = background.get_rect()

#  a clock is initialized to track FPS,
#  and the area of the BG is taken to create a pygame surface.
clock = pygame.time.Clock()
a_size = (screen_rect.w, screen_rect.h)
bg = pygame.Surface(a_size)

#  Directions, attack, and pivot are actions
#  the player can take singly or in combination.
input_delay = .22


def game():
    #  a level is interpreted from a .txt file using the Level class.
    #  this class converts a grid of characters into a playable gamespace.
    file_name = random_diamond_floor()
    level = Level(file_name)
    level.create_level(0, 0, one_square)

    #  object and fog containers are pulled into this scope;
    #  this is useful for collision and "vision":
    world = level.world
    all_sprite = level.all_sprite
    fog_sprites = level.fog_sprites
    active_weapons = []

    #  player is collected into a variable in this scope from level.
    player = level.player1
    pygame.mouse.set_visible(0)

    #  camera is now centered around extracted player.
    camera = Camera(screen, player.rect, level.get_size()[0], level.get_size()[1])

    #  Now the monster and spawner lists are pulled to this scope,
    #  including the max_monsters for the level.
    #  Also a boolean for whether the player successfully
    #  performs a 'move', e.g. attack or left. This is used
    #  to increment up a monster's internal tick so they can act.
    monster_list = level.monster_list
    spawner_list = level.spawner_list
    max_monsters = level.max_monsters
    max_monsters = 20

    #  Checks the power min and power max for the stage and queries for monsters within it.
    p_min = level.power_min
    p_max = level.power_max
    p_min = 0
    p_max = 50
    monster_data = MonsterDB.select().where(MonsterDB.power <= p_max).where(MonsterDB.power >= p_min)
    monster_types = []
    #  Attaches monster data to a list of types
    #  that can spawn on this level:
    for monster in monster_data:
        monster_types.append([monster.name, monster.type, monster.spells, monster.min_hp,
                              monster.max_hp, monster.attack, monster.speed, monster.defense,
                              monster.algorithm, monster.light_r, monster.power])
    del monster_data

    #  the state of auto_repeat is True after input_delay has passed on player input.
    auto_repeat = False
    up = down = left = right = attack = False
    pivot = strafe = w_toggle = enter = False

    start = 0
    reset = False
    #  move is applied so that one input passes.
    # and the game is started paused.
    move = paused = True

    #  An alternating control frame is applied
    control_frame = 1

    while True:
        """This is the main game loop. It checks for keydown events that match
           particular keys. It also checks for keyup events to cancel input and
           auto_repeat and single movement commands to initial values. In each
           cycle of the loop all objects are redrawn onto the camera surface.
           Projectiles have their position updated every cycle, but the player's
           position is updated only every other cycle. When the player moves, all
           other characters are given one movement and updated as well."""
        for event in pygame.event.get():
            if ((event.type == QUIT or event.type == KEYDOWN) and
                    event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                # if not start:
                start = time()
                move = True
                if event.key == K_RETURN or event.key == K_p:
                    paused = not paused
                if event.key == K_w:
                    up = True
                if event.key == K_a:
                    left = True
                if event.key == K_s:
                    down = True
                if event.key == K_d:
                    right = True
                if event.key == K_e:
                    attack = True
                if event.key == K_n and paused:
                    game()
                # if event.key == K_r:
                #     w_toggle = True
                if event.key == K_f:
                    strafe = not strafe
                if event.key == K_RCTRL:
                    pivot = True
                    strafe = False
                    start = input_delay
            if event.type == KEYUP:
                if event.key == K_w:
                    up = False
                if event.key == K_a:
                    left = False
                if event.key == K_s:
                    down = False
                if event.key == K_d:
                    right = False
                if event.key == K_e:
                    attack = False
                if event.key == K_r:
                    w_toggle = False
                if event.key == K_RCTRL:
                    pivot = False
                if not up and not left and not down and not right and not attack:
                    auto_repeat = False
                    # start = 0

        FPS = round(2 + len(monster_list) / 12) * 30
        time_spent = tps(clock, FPS)
        # parallax background option:
        # a_size = ((screen_rect.w // background_rect.w + 1) * background_rect.w,
        #          (screen_rect.h // background_rect.h + 1) * background_rect.h)
        for x in range(0, a_size[0], background_rect.w):
            for y in range(0, a_size[1], background_rect.h):
                screen.blit(background, (x, y))
        camera.draw_sprites(screen, all_sprite)
        camera.draw_sprites(screen, fog_sprites)

        if paused:
            rect_x = 400
            rect_y = 120
            rect = (x_center - rect_x / 2, y_center - rect_y / 2, rect_x, rect_y)
            remainder = draw_text(screen, "tutorial", [0, 0, 0], rect, "aerial", bkg=[255, 255, 255])
            if remainder:
                print(remainder)
        else:
            auto_repeat = move_delay(start)
            control_frame *= -1
            player_acts = False
            if control_frame > 0 and (move or auto_repeat):
                player_acts = player.update(
                                             up, down, left, right, attack, pivot, strafe, w_toggle,
                                             world, all_sprite, fog_sprites,
                                             active_weapons, one_square, screen
                                )
                move = False

            if player_acts:
                for monster in monster_list:
                    monster.update(world, all_sprite, monster_list,
                                   player, active_weapons, one_square)
                if len(monster_list) < max_monsters:
                    chosen_spawner = random.choice(spawner_list)
                    chosen_spawner.spawn(world, all_sprite, monster_list,
                                         one_square, monster_types)

            for weapon in active_weapons:
                weapon.update(world, all_sprite, active_weapons)

        camera.update()
        pygame.display.flip()


game()