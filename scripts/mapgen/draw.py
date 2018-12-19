import math


class Draw:
    """ Accepts parameters to draw
    geometric shapes in x and y coordinates

    return types for draw:
    'parsed', e.g. border, area = Draw.square(p,(h,l),t,'parsed')
    'outline', e.g  border = Draw.diamond(p,r,t,'outline')
    'block', e.g. circle = Draw.circle(p,r,t,'block')
    default return is simply the area within the shape."""

    @staticmethod
    def square(position, size, ret_type):
        """draws a square with size as a tuple of height and length, (h, l)
        position as a tuple of x and y coordinates, (x, y).
        the given position will lie at the center of the coordinate set."""
        lth, h = size
        h -= 1
        lth -= 1
        border = []
        area = []
        start_x, start_y = position
        start_y -= round(1 / 2 * h)
        start_x -= round(1 / 2 * lth)
        for y in range(h):
            border.append((start_x, start_y + y))
            border.append((start_x + lth, start_y + y))
        for x in range(lth):
            border.append((start_x + x, start_y))
            border.append((start_x + x, start_y + h))
        for y in range(h - 1):
            for x in range(lth - 1):
                area.append((start_x + x + 1, start_y + y + 1))
        border.append((start_x + lth, start_y + h))
        border = list(set(border))
        area = list(set(area))
        if ret_type == 'parsed':
            return border, area
        elif ret_type == 'outline':
            return border
        elif ret_type == 'block':
            return border + area
        else:
            return area

    @staticmethod
    def diamond(position, r, ret_type):
        """draws a diamond with radius r as an integer and
        position as a tuple of x and y coordinates.
        the given position will lie at the center of the coordinate set.
        :rtype: object"""
        border = []
        area = []
        start_x, start_y = position
        r -= 1
        for x in range(r):
            for y in range(x, r):
                area.append((start_x + x, start_y - y + r - 1))
                area.append((start_x + x, start_y + y - r + 1))
                area.append((start_x - x, start_y - y + r - 1))
                area.append((start_x - x, start_y + y - r + 1))
        r += 1
        for x in range(r):
            for y in range(x, r):
                border.append((start_x + x, start_y - y + r - 1))
                border.append((start_x + x, start_y + y - r + 1))
                border.append((start_x - x, start_y - y + r - 1))
                border.append((start_x - x, start_y + y - r + 1))

        border = list(set(border) - set(area))
        border = list(set(border))
        area = list(set(area))
        if ret_type == 'parsed':
            return border, area
        elif ret_type == 'outline':
            return border
        elif ret_type == 'block':
            return border + area
        else:
            return area

    @staticmethod
    def circle(position, r, ret_type):
        """draws a circle with radius r as an integer and
        position as a tuple of x and y coordinates.
        the given position will lie at the center of the coordinate set."""

        border = []
        area = []
        k, h = position
        X = int(r)
        for x in range(-X, X+1):
            Y = int((r*r-x*x)**0.5)
            for y in range(-Y, Y+1):
                area.append((x + k, y + h))
                x_sqrd = math.pow(x, 2)
                y_sqrd = math.pow(y, 2)
                if 0.9 * X < math.sqrt(x_sqrd + y_sqrd):
                    border.append((x + k, y + h))

        border = list(set(border))
        area = list(set(area) ^ set(border))
        if ret_type == 'parsed':
            return border, area
        elif ret_type == 'outline':
            return border
        elif ret_type == 'block':
            return border + area
        else:
            return area
