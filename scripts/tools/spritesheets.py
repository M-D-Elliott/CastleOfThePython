"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame

class SpriteSheet(object):
    def get_image(posx, posy, width, height, sprite_sheet):
        """Extracts image from sprite sheet"""
        image = pygame.Surface([width, height])
        image.blit(sprite_sheet, (0, 0), (posx, posy, width, height))
        image.set_colorkey(0, 0)

        return image