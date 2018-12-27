import pygame

from globals import root


class Object(pygame.sprite.Sprite):
    """Produce an object that can be added to the world for collisions or
       another attribute list, such as fog, to avoid collision."""
    def __init__(self, img_name):
        self.name = img_name
        pygame.sprite.Sprite.__init__(self)
        if not hasattr(self, 'img_path'):
            self.img_path = root + '/world/%s.png' % img_name
            self.image = pygame.image.load(self.img_path).convert_alpha()
        # if not self.img_path == root + '/world/False.png':
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]


class Fog(Object):
    """This is a unique object that is added to a sprite layer placed above the
       game layer. As the player's light radius collides with one of these objects
       it is deleted. i.e. t he fog clears."""
    def __init__(self, x, y, img_name):
        self.name = 'Fog'
        self.x = x
        self.y = y
        super().__init__(img_name)
