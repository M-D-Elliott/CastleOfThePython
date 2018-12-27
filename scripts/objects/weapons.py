import pygame
import os
from PIL import Image

from scripts.objects.moving_objects import MovingObject
from scripts.tools.spritesheets import SpriteSheet
from globals import root


class Weapon(MovingObject):
    def __init__(self, owner, img_name):
        self.dirn_x = owner.dirn_x
        self.dirn_y = owner.dirn_y
        dirn_name = ''
        angle = 0
        if self.dirn_x != 0 and self.dirn_y != 0:
            dirn_name = 'Diag'
            if (self.dirn_x, self.dirn_y) == (1, 1):
                angle = 90
            elif (self.dirn_x, self.dirn_y) == (1, -1):
                angle = 180
            elif (self.dirn_x, self.dirn_y) == (-1, 1):
                angle = 0
            elif (self.dirn_x, self.dirn_y) == (-1, -1):
                angle = -90
        else:
            angle = 180 if self.dirn_y == -1 else 90 * self.dirn_x
        self.img_name = img_name + dirn_name
        self.img_path = root + '/weapons/%s.png' % self.img_name
        self.img_sheet = pygame.transform.rotate(pygame.image.load(self.img_path).convert_alpha(), angle)
        self.sheet_width = (Image.open(self.img_path)).width
        self.image = SpriteSheet.get_image(0, 0, self.sheet_width, 25, self.img_sheet)
        self.frames = []
        self.frame = 0
        x = owner.rect.centerx
        y = owner.rect.centery
        super().__init__(self.img_name, x, y)
        self.owner = owner

    def collide(self, world, all_sprite, active_weapons):
        """When a projectile collides with an object in the level.world
           list attribute it is destroyed and removed all lists. The owner of
           the projectile also has their count restored by 1."""
        self.contact = False
        for o in world:
            if self.rect.colliderect(o) and o.owner != self.owner.owner:
                if o.name == 'Door' or o.name == 'DoorOpen':
                    o.toggle()
                if hasattr(o, 'hit_points'):
                    o.hit_points -= 1
                return True


class Projectile(Weapon):
    """This is a weapon that is generated when a character uses a
    ranged attack. It flies the direction the character is facing. Speed and
    img files can be called to create numerous projectile types."""

    def __init__(self, owner, img_name, one_square):
        super().__init__(owner, img_name)
        self.rect.centerx = owner.rect.centerx
        self.rect.centery = owner.rect.centery
        self.movx = one_square * .8 * owner.dirn_x
        self.movy = one_square * .8 * owner.dirn_y

    def update(self, world, all_sprite, active_weapons):
        """This controls how a projectile changes over time, or when it is
           granted an update."""
        self.rect.right += self.movx
        self.rect.top += self.movy
        self.collide(world, all_sprite, active_weapons)

    def collide(self, world, all_sprite, active_weapons):
        """When a projectile collides with an object in the level.world
           list attribute it is destroyed and removed all lists. The owner of
           the projectile also has their count restored by 1."""

        if super().collide(world, all_sprite, active_weapons):
            self.owner.proj_count += 1
            active_weapons.remove(self)
            self.kill()


class Melee(Weapon):
    def __init__(self, owner, img_name, one_square):
        super().__init__(owner, img_name)
        self.last_frame = int(self.sheet_width / one_square)
        if self.dirn_x and self.dirn_y:
            self.rect.left = owner.rect.right
        else:
            if self.dirn_x == 1:
                self.rect.left = owner.rect.right
            elif self.dirn_x == -1:
                self.rect.right = owner.rect.left
            elif self.dirn_y == 1:
                self.rect.top = owner.rect.bottom
            elif self.dirn_y == -1:
                self.rect.bottom = owner.rect.top
        for l in range(self.last_frame):
            self.frames.append(SpriteSheet.get_image(25 * (l - 1), 0, self.sheet_width, 25, self.img_sheet))

    def update(self, world, all_sprite, active_weapons):
        if self.dirn_x and self.dirn_y:
            self.rect.left = self.owner.rect.right
        else:
            if self.dirn_x == 1:
                self.rect.left = self.owner.rect.right
            elif self.dirn_x == -1:
                self.rect.right = self.owner.rect.left
            elif self.dirn_y == 1:
                self.rect.top = self.owner.rect.bottom
            elif self.dirn_y == -1:
                self.rect.bottom = self.owner.rect.top
        self.frame += 1
        self.image = self.frames[self.frame]
        self.collide(world, all_sprite, active_weapons)
        if self.frame == self.last_frame - 1:
            self.owner.proj_count += 1
            active_weapons.remove(self)
            self.kill()


