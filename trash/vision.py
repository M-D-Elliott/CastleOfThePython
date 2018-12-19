
class Vision(MovingObject):
    """
    creates dynamic vision radius composed of 8 rectangles
    """
    def __init__(self, x, y, one_square, position, size):
        self.name = 'Vision'
        img_path = False
        self.collision = False
        super().__init__(x, y, img_path)

        depth = one_square * size
        square = 0
        if position == 'top' or position == 'bottom':
            square = pygame.Surface((one_square, depth), pygame.SRCALPHA)
        elif position == 'left' or position == 'right':
            square = pygame.Surface((depth, one_square), pygame.SRCALPHA)
        else:
            square = pygame.Surface((depth, depth), pygame.SRCALPHA)
        square.fill((255, 25, 25, 0))
        self.rect = square.get_rect()
        self.image = square
        if position == 'top':
            self.rect.topleft = [x, y - (2 * one_square)]
        elif position == 'bottom':
            self.rect.topleft = [x, y + one_square]
        elif position == 'left':
            self.rect.topleft = [x - (2 * one_square), y]
        elif position == 'right':
            self.rect.topleft = [x + one_square, y]
        elif position == 'tl':
            self.rect.topleft = [x - one_square, y - one_square]
        elif position == 'tr':
            self.rect.topleft = [x + one_square, y - one_square]
        elif position == 'bl':
            self.rect.topleft = [x - one_square, y + one_square]
        elif position == 'br':
            self.rect.topleft = [x + one_square, y + one_square]

    def collide(self, world, fog_sprites, light_r):
        """Defines the fog destroying effect of the light radius. Allows the
           player to remove fog of war from places that have been visited."""
        self.collision = False
        # for o in world:
        #     if self.rect.colliderect(o) and o != self and o.name != 'DoorOpen':
        #         self.collision = True

        if not self.collision:
            for o in fog_sprites:
                if self.rect.colliderect(o):
                    fog_sprites.remove(o)
                    o.kill()
                    del o