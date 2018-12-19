import pygame
from root import root

from scripts.objects.objects import Object


class Obstacle(Object):
    """This class is specially tuned for objects intended to collide with the
       character class and all children."""
    def __init__(self, x, y, img_name):
        self.name = img_name
        self.x = x
        self. y = y
        super().__init__(img_name)
        self.owner = None


class Door(Obstacle):
    def __init__(self, x, y):
        img_name = 'Door'
        super().__init__(x, y, img_name)
        self.name = 'Door'
        self.obstructed = False

    def toggle(self):
        if self.name == 'Door':
            self.name = 'DoorOpen'
            self.image = pygame.image.load(root + "/world/DoorOpen.png")
        elif not self.obstructed:
            self.name = 'Door'
            self.image = pygame.image.load(root + "/world/Door.png")

    def obstruct(self, boolean):
        self.obstructed = boolean
