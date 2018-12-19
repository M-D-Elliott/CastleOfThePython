import random


class Coords:

    @staticmethod
    def center(l, h):
        """This accepts a length and height and finds the center of the
           2D object in a coordinate plane."""
        x = round((l / 2))
        y = round((h / 2))
        return tuple((x, y))

    @staticmethod
    def random(l, h, offset_l=0, offset_h=0):
        """This accepts a length and height and returns a random coordinate
           within on a 2D coordinate plane."""
        x = random.randint(0 + offset_l, l - offset_l)
        y = random.randint(0 + offset_h, h - offset_h)
        return tuple((x, y))
