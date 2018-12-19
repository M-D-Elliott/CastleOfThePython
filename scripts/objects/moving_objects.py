import pygame
import os

from scripts.objects.objects import Object


class MovingObject(Object):
    """This is the second tier in the object tree, the parent of all objects
       capable of movement. Initializes speeds in movx and movy and
       directionality."""
    def __init__(self, img_name, x, y):
        self.x = x
        self.y = y
        super().__init__(img_name)
        self.movy = 0
        self.movx = 0
        self.contact = False
        self.collision = False
        self.direction = "up"

    def collide(self, movx, movy, world):
        """This method defines the basic result of collision between a moving
           object and any other collideable object."""
        self.contact = False
        for o in world:
            if self.rect.colliderect(o) and o != self:
                if movx > 0:
                    self.rect.right = o.rect.left
                if movx < 0:
                    self.rect.left = o.rect.right
                if movy > 0:
                    self.rect.bottom = o.rect.top
                if movy < 0:
                    self.rect.top = o.rect.bottom


class Block(MovingObject):
    """This is a moving object that can be pushed by a character. Two
       blocks cannot be pushed at once."""
    def __init__(self, x, y):
        img_name = 'Block'
        super().__init__(img_name, x, y)
        self.name = 'Block'
        self.owner = False
