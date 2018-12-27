import pygame
import random
import math

from scripts.objects.objects import Object
from scripts.objects.moving_objects import MovingObject
from scripts.objects.weapons import Projectile
from scripts.objects.weapons import Melee
from globals import root


class Character(MovingObject):
    """Initializes a character which is the parent to all player and monster
       classes. All children of this class can move in interact with each other
       and objects in the world."""
    def __init__(self, img_name, x, y):
        super().__init__(img_name, x, y)
        self.jump = False
        self.frame = 0
        self.owner = img_name
        self.proj_count = self.proj_count if self.proj_count else 0
        self.in_door = False
        self.door = None

    def collide(self, movx, movy, world):
        """This overrides the basic collide interaction established in
           MovingObject. This does the same thing but also checks for blocks
           and calls for the block push method."""
        self.contact = False
        for o in world:
            if self.rect.colliderect(o):
                if o.name == 'DoorOpen':
                    if self.x == o.x and self.y == o.y:
                        self.in_door = True
                        self.door = o
                        self.door.obstruct(True)
                elif o != self:
                    if movx > 0:
                        self.rect.right = o.rect.left
                    if movy > 0:
                        self.rect.bottom = o.rect.top
                    if movx < 0:
                        self.rect.left = o.rect.right
                    if movy < 0:
                        self.rect.top = o.rect.bottom
                    if o.__class__.__name__ == 'Block':
                        self.move_block(o, movx, movy, world)
                    self.collision = True
                elif self.door is not None:
                    if self.x != self.door.x or self.y != self.door.y:
                        self.door.obstruct(False)
                        self.door = None
                        self.in_door = False

    @staticmethod
    def move_block(o, movx, movy, world):
        """This method allows all characters to push blocks in the world."""
        o.rect.right += movx
        o.collide(movx, 0, world)
        o.rect.top += movy
        o.collide(0, movy, world)
        o.contact = False

    def attack_with_weapon(self, weapon,
                           all_sprite, active_weapons, one_square):
        """This method allows defines the projectile shooting ability of
           all character children. With a count of 0 above, this function is
           effectively disabled."""
        active_weapon = None
        if weapon[0] == 'Melee':
            active_weapon = Melee(self, weapon[1], one_square)
        elif weapon[0] == 'Projectile':
            active_weapon = Projectile(self, weapon[1], one_square)
        self.proj_count -= 1
        active_weapons.append(active_weapon)
        all_sprite.add(active_weapon)


class Player(Character):
    """Class for player 1. Instantiates left-hand character with left-hand
       key controls."""
    def __init__(self, img_name, x, y, one_square, light_r):
        self.img_path = root + '/actions/%s-10.png' % img_name
        self.image = pygame.image.load(self.img_path).convert_alpha()
        self.direction = "up"
        self.hit_points = 50
        self.vision = light_r * one_square
        self.dirn_x = 0
        self.dirn_y = -1
        self.proj_count = 1
        self.weapons = [['Projectile', 'Arrow'], ['Melee', 'Sword']]
        self.w_equipped = self.weapons[0]
        super().__init__(img_name, x, y)

    def update(self,
               up, down, left, right, attack, pivot, strafe, w_toggle,
               world, all_sprite, fog_sprites, active_weapons,
               one_square, screen):
        """Takes WASD control to move player 1 u/d/r/l and attack. Also takes
           the world list, the all_sprite list, the fog_sprites list, the
           projectiles list, and the square size."""

        self.movx = 0
        self.movy = 0

        if up:
            self.movy = -one_square
        if down:
            self.movy = one_square
        if left:
            self.movx = -one_square
        if right:
            self.movx = one_square
        if w_toggle:
            current_index = self.weapons.index(self.w_equipped)
            next_index = 1 + current_index
            if next_index == len(self.weapons):
                current_index = 0
            else:
                current_index = next_index
            self.w_equipped = self.weapons[current_index]
        elif attack and self.proj_count > 0:
            self.attack_with_weapon(self.w_equipped,
                                    all_sprite, active_weapons, one_square)

        if not pivot:
            self.rect.right += self.movx
            self.collide(self.movx, 0, world)
            self.rect.top += self.movy
            self.collide(0, self.movy, world)

        if not strafe and (self.movx or self.movy):
            self.dirn_x = 0 if self.movx == 0 else int(self.movx / abs(self.movx))
            self.dirn_y = 0 if self.movy == 0 else int(self.movy / abs(self.movy))
        direction = str(int(self.dirn_x)) + str(int(self.dirn_y))
        self.image = pygame.image.load(root + "/actions/Player1%s.png" % direction)
        self.contact = False

        self.x, self.y = self.rect.topleft
        line = None
        for f in fog_sprites:
            vision = True
            distance = int(math.sqrt(math.pow((f.x - self.x), 2) + math.pow((f.y - self.y), 2)))
            if distance <= self.vision:
                # line = pygame.draw.line(screen, (255, 255, 255), (f.x, f.y), (self.x, self.y), one_square)
                # for o in world:
                #     if line.colliderect(o) and (o.name == 'Wall' or o.name == 'Door'):
                #         vision = False
                #         break
                # del line
                # if vision:
                fog_sprites.remove(f)
                f.kill()
                del f
        player_moves = (self.movy or self.movx) and not pivot
        player_acts = player_moves or attack
        return player_acts


class Spawner(Object):
    def __init__(self, x, y, img_name, one_square, rate=2):
        self.x = x
        self.y = y
        super().__init__(img_name)
        self.spawn_locations = []
        self.rate = rate
        self.tick = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                self.spawn_locations.append((self.x + one_square * x,
                                             self.y + one_square * y))
        self.owner = False

    def spawn(self, world, all_sprite, monster_list, one_square, monster_types):
        if self.tick == 4:
            self.tick = 0
            x, y = random.choice(self.spawn_locations)
            monster_choice = monster_types[random.randint(0, len(monster_types) - 1)]
            monster = Monster(monster_choice, x, y, one_square)
            world.append(monster)
            all_sprite.add(monster)
            monster_list.append(monster)
        self.tick += 1


class Monster(Character):
    """Instantiates a monster with a name passed in. The name attaches to a
       file in the monsters folder as well as that monster in the SQL
       database."""
    def __init__(self, monster, x, y, one_square):
        self.name = self.owner = monster[0]
        self.img_path = root + '/monsters/%s.png' % self.name
        self.image = pygame.image.load(self.img_path).convert_alpha()
        self.type = monster[1]
        self.spells = monster[2]
        self.hit_points = random.randint(monster[3], monster[4])
        self.attack = monster[5]
        self.speed = monster[6]
        self.defense = monster[7]
        self.algorithm = monster[8]
        self.vision = monster[9] * one_square
        self.power = monster[10]
        self.tick = 0
        self.dirn_x = 1
        self.dirn_y = 1
        self.proj_count = 1
        super().__init__(self.name, x, y)

    def update(self, world, all_sprite, monster_list, player, active_weapons,
               one_square):
        """The monster only moves when it's personal tick value falls
           behind that of the global tick (generated by the player). If the
           player enters a monster's 'vision radius' the monster will
           intelligently move toward the player and attack. These actions will
           be randomly chosen from a list of possible actions."""

        if self.hit_points < 1:
            world.remove(self)
            monster_list.remove(self)
            all_sprite.remove(self)
            self.kill()
        else:
            if self.tick == 4:
                self.tick = 0
                if self.algorithm == 0:
                    self.algorithm_0(player, world, all_sprite, active_weapons, one_square)
            self.tick += 1

    def algorithm_0(self, player, world, all_sprite, active_weapons, one_square):
        self.movx = 0
        self.movy = 0
        x = self.x
        y = self.y
        X = player.x
        Y = player.y
        diff_x = x - X
        diff_y = y - Y
        distance = int(math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2)))
        sees_player = distance <= self.vision

        if sees_player:
            diff_x = abs(diff_x)
            diff_y = abs(diff_y)
            sign_x = 0 if diff_x == 0 else (X - x) / diff_x
            sign_y = 0 if diff_y == 0 else (Y - y) / diff_y
            if (
                (diff_x == diff_y and sign_x == self.dirn_x and sign_y == self.dirn_y) or
                (not diff_x and sign_y == self.dirn_y and self.dirn_x == 0) or
                (not diff_y and sign_x == self.dirn_x and self.dirn_y == 0)
            ):
                self.attack_with_weapon(['Projectile', 'Arrow'], all_sprite, active_weapons,
                                        one_square)
            else:
                self.movx = one_square * sign_x
                self.movy = one_square * sign_y
        else:
            self.movx = one_square * random.randint(-1, 1)
            self.movy = one_square * random.randint(-1, 1)

        self.dirn_x = 0 if not self.movx else self.movx / abs(self.movx)
        self.dirn_y = 0 if not self.movy else self.movy / abs(self.movy)

        self.rect.right += self.movx
        self.collide(self.movx, 0, world)
        self.rect.top += self.movy
        self.collide(0, self.movy, world)

        self.x, self.y = self.rect.topleft
        self.contact = False
