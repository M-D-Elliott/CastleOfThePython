import random
from operator import itemgetter
import math

from scripts.mapgen.draw import Draw
from scripts.mapgen.coords import Coords
from scripts.mapgen.ascii import ascii
from root import root


class Map(dict):
    """This class instantiates a dictionary that fills itself with a grid of
       specified height and length. The keys are tuples of each x, y coordinate
       on the grid. The values of those keys are initializes as an empty
       'CastleWall' sprite."""
    def __init__(self, name, l, h):
        super().__init__()
        self.name = self['name'] = name
        for y in range(h):
            for x in range(l):
                self.update({(x, y): 'CastleWall'})
        self.update({'name': name})
        self.update({'height': h - 1, 'length': l - 1, 'area': h * l})
        self.update({'center': Coords.center(l, h)})

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    # def __unicode__(self):
    #     return unicode(repr(self.__dict__))

    def add_room(self, inp_position, shape, size):
        """This method adds a room of specified shape, random or specified
        size, and random or specified location to the dungeon. It also checks
        if the space where the room is located is open. If the space is not
        available it destroys the prepared room. The 'border' of the room is
        given the 'Wall' img while the area is tagged as 'Empty Floor', which
        gets interpreted as the background layer."""
        grid_h = self['height']
        grid_l = self['length']
        border = []
        area = []
        space_open = True
        doors = 0
        position = (5, 5)
        min_size = 8

        if inp_position == 'random':
            position = Coords.random(self['length'], self['height'], min_size, min_size)
        else:
            position = inp_position

        if size == 'random':
            max_h = round(grid_h / 4)
            max_lth = round(grid_l / 4)
            x, y = position
            if x + max_lth >= self['length']:
                max_lth = self['length'] - x
            elif x - max_lth <= 0:
                max_lth = x
            if y + max_h >= self['height']:
                max_h = self['height'] - y
            elif y - max_h <= 0:
                max_h = y
            lth = min_size + random.randint(0, (max_lth - min_size))
            h = min_size + random.randint(0, (max_h - min_size))
            if shape == 'circle' or shape == 'diamond':
                size = lth if lth <= h else h
            else:
                size = (lth, h)

        if shape == 'square':
            border, area = Draw.square(position, size, 'parsed')
            doors = random.randint(4, 8)
        elif shape == 'circle':
            border, area = Draw.circle(position, size, 'parsed')
            doors = random.randint(4, 8)
        elif shape == 'diamond':
            border, area = Draw.diamond(position, size, 'parsed')
            doors = random.randint(4, 8)
        for coordinate in border + area:
            if self[coordinate] != 'CastleWall':
                space_open = False

        door_chance = 1
        lth, h = size if shape == 'square' else (size, size)
        door_roll = round((lth * 2 + h * 2) / 4)
        if space_open:
            for coordinate in area:
                self[coordinate] = 'EmptyFloor'
            for coordinate in border:
                self[coordinate] = 'Wall'
                x, y = coordinate
                door_calc = random.randint(door_chance, door_roll) if door_chance < door_roll else door_roll
                if door_calc == door_roll and doors > 0:
                    door_chance = 1
                    if shape == 'square':
                        max_x = max(border, key=itemgetter(0))[0]
                        min_x = min(border, key=itemgetter(0))[0]
                        max_y = max(border, key=itemgetter(1))[1]
                        min_y = min(border, key=itemgetter(1))[1]
                        if (
                            coordinate != (max_x, min_y) and
                            coordinate != (max_x, max_y) and
                            coordinate != (min_x, min_y) and
                            coordinate != (min_x, max_y)
                           ):
                            doors -= 1
                            self[coordinate] = 'Door'
                    else:
                        doors -= 1
                        self[coordinate] = 'Door'
                else:
                    door_chance += 1
        del border
        del area

    def add_hallways(self):
        """
        This function loops across each door in the floor grid, or map,
        and attempts to find the "best door" or shortest distance door without
        obstruction to pair it with and build a hallway to.
        """
        # first this function collects all the doors in this grid into a list:
        all_doors = [k for k, v in self.items() if v == 'Door']
        for door in all_doors:
            # next it sets the x and y coordinates to the current door tuple:
            x, y = door

            # and establishes variables to be used:
            scan_size = 30
            scan_x = range(0, 0)
            scan_y = range(0, 0)
            x_door = False
            y_door = False
            x_inc = 0
            y_inc = 0

            # here we check the position of the door relative to empty grid space,
            # which is known as 'CastleWall'. This allows determination of the door's
            # directionality as x - 1 or x + 1, y - 1, or y + 1.
            # this portion ensures that the scanned range, scan_x and scan_y
            # does not exceed the bounds of the total grid.
            if self[(x - 1, y)] == 'CastleWall':
                x_door = True
                x_if = x - scan_size * 2 if x >= scan_size * 2 else 0
                scan_x = range(x_if, x - 1)
                y_r_min = y - scan_size if y >= scan_size else 0
                y_r_max = y + scan_size if y + scan_size <= self['height'] else self['height']
                scan_y = range(y_r_min, y_r_max)
            elif self[(x + 1, y)] == 'CastleWall':
                x_door = True
                x_if = x + scan_size * 2 if x + scan_size * 2 <= self['length'] else self['length']
                scan_x = range(x + 1, x_if)
                y_r_min = y - scan_size if y >= scan_size else 0
                y_r_max = y + scan_size if y + scan_size <= self['height'] else self['height']
                scan_y = range(y_r_min, y_r_max)
            elif self[(x, y - 1)] == 'CastleWall':
                y_door = True
                y_if = y - scan_size * 2 if y >= scan_size * 2 else 0
                scan_y = range(y_if, y - 1)
                x_r_min = x - scan_size if x >= scan_size else 0
                x_r_max = x + scan_size if x + scan_size <= self['height'] else self['height']
                scan_x = range(x_r_min, x_r_max)
            elif self[(x, y + 1)] == 'CastleWall':
                y_door = True
                y_if = y + scan_size * 2 if y + scan_size * 2 <= self['height'] else self['height']
                scan_y = range(y + 1, y_if)
                x_r_min = x - scan_size if x >= scan_size else 0
                x_r_max = x + scan_size if x + scan_size <= self['length'] else self['length']
                scan_x = range(x_r_min, x_r_max)
            else:
                # if the door has no directionality toward empty grid space
                # we can also check if it can be made into a "nook" door between adjacent rooms.
                # regardless of if this is possible this else then continues the loop
                # to the next door on the all_doors list.
                if (
                    self[(x - 1, y)] == 'EmptyFloor'
                    and self[(x + 2, y)] == 'EmptyFloor'
                ):
                    self[(x + 1, y)] = 'EmptyFloor'
                    self[(x, y)] = 'EmptyFloor'
                elif (
                    self[(x + 1, y)] == 'EmptyFloor'
                    and self[(x - 2, y)] == 'EmptyFloor'
                ):
                    self[(x - 1, y)] = 'EmptyFloor'
                    self[(x, y)] = 'EmptyFloor'
                elif (
                    self[(x, y - 1)] == 'EmptyFloor'
                    and self[(x, y + 2)] == 'EmptyFloor'
                ):
                    self[(x, y + 1)] = 'EmptyFloor'
                    self[(x, y)] = 'EmptyFloor'
                elif (
                    self[(x, y + 1)] == 'EmptyFloor'
                    and self[(x, y - 2)] == 'EmptyFloor'
                ):
                    self[(x, y - 1)] = 'EmptyFloor'
                    self[(x, y)] = 'EmptyFloor'
                continue

            # if the current door has directionality toward empty space or 'CastleWall'
            # then the range toward that empty space is scanned. An adj value is added so
            # that the minimum clearance size is greater than 0 and the for loops below occur.
            # This is needed for perfectly horizontal or vertical door-to-door pairs.
            # Once the range is established in a way that is adaptable to all above
            # directionality the spaces in the x and y clearance are checked to be empty
            # grid space or 'CastleWall' Every workable door is added to an option list.

            low_value = 1000
            min_distance = 4
            best_door = []
            for X in scan_x:
                for Y in scan_y:
                    distance = int(math.sqrt(math.pow((X - x), 2) + math.pow((Y - y), 2)))
                    if self[(X, Y)] == 'EmptyFloor' and min_distance < distance < low_value:
                        good_door = True
                        diff_x = abs(X - x)
                        diff_y = abs(Y - y)
                        X_door = bool(self[(X - 2, Y)] == 'CastleWall' or self[(X + 2, Y)] == 'CastleWall')
                        Y_door = bool(self[(X, Y - 2)] == 'CastleWall' or self[(X, Y + 2)] == 'CastleWall')
                        diag_door = bool(random.randint(0, 1))
                        diag_door = False
                        clearance_x = range(0, 0)
                        clearance_y = range(0, 0)
                        x_proportion = (diff_x/diff_y) if diff_y else 0
                        y_proportion = (diff_y/diff_x) if diff_x else 0

                        if diff_y == 0:
                            hall_type = 'direct_x'
                            clearance_x = range(x + 1, X - 2) if x < X else range(X + 2, x - 1)
                            clearance_y = range(y - 1, y + 1)
                        elif diff_x == 0:
                            hall_type = 'direct_y'
                            clearance_x = range(x - 1, x + 1)
                            clearance_y = range(y + 1, Y - 2) if y < Y else range(Y + 2, y - 1)
                        elif x_door and Y_door and not diag_door:
                            hall_type = 'corner_xtoy'
                            clearance_x = range(x + 1, X) if x < X else range(X, x - 1)
                            clearance_y = range(y, Y - 2) if y < Y else range(Y + 2, y)
                        elif y_door and X_door and not diag_door:
                            hall_type = 'corner_ytox'
                            clearance_y = range(y + 1, Y) if y < Y else range(Y, y - 1)
                            clearance_x = range(x, X - 2) if x < X else range(X + 2, x)
                        else:
                            x_prop = round(diff_x / diff_y)
                            y_prop = round(diff_y / diff_x)
                            hall_type = 'diag_y' if y_prop > x_prop else 'diag_x'
                            clearance_x = range(x, X) if x < X else range(X, x)
                            clearance_y = range(y, Y) if y < Y else range(Y, y)

                        for space_x in clearance_x:
                            for space_y in clearance_y:
                                if self[(space_x, space_y)] != 'CastleWall':
                                    good_door = False
                                    break
                            if not good_door:
                                break
                        if good_door:
                            low_value = distance
                            best_door = [(X, Y), hall_type]

            if len(best_door) == 0:
                continue
            # since the terminal door was found, the best door, we now assign to X and Y:
            X, Y = best_door[0]
            hall_type = best_door[1]
            diff_x = abs(X - x)
            diff_y = abs(Y - y)
            x_proportion = 0
            y_proportion = 0
            x_inc = 1 if x < X else -1
            y_inc = 1 if y < Y else -1
            # print(hall_type, x, X, y, Y)

            # now we increment the x and/or y value, starting from the
            # initial door, toward the terminal X and/or Y.
            while (
                (hall_type == 'direct_x' and diff_x > 2) or
                (hall_type == 'direct_y' and diff_y > 2) or
                (hall_type == 'corner_xtoy' and diff_y > 2) or
                (hall_type == 'corner_ytox' and diff_x > 2) or
                (hall_type == 'diag_y' and diff_x > 2) or
                (hall_type == 'diag_x' and diff_y > 2)
            ):
                diff_x = abs(X - x)
                diff_y = abs(Y - y)
                if diff_y == 0:
                    x += x_inc
                    self[(x, y + 1)] = 'Wall'
                    self[(x, y)] = 'EmptyFloor'
                    self[(x, y - 1)] = 'Wall'
                elif diff_x == 0:
                    y += y_inc
                    self[(x + 1, y)] = 'Wall'
                    self[(x, y)] = 'EmptyFloor'
                    self[(x - 1, y)] = 'Wall'
                elif hall_type == 'corner_xtoy':
                    x += x_inc
                    self[(x, y + 1)] = 'Wall'
                    self[(x, y)] = 'EmptyFloor'
                    self[(x, y - 1)] = 'Wall'
                    if diff_x == 1:
                        self[(x + x_inc, y)] = 'Wall'
                        self[(x + x_inc, y - y_inc)] = 'Wall'
                elif hall_type == 'corner_ytox':
                    y += y_inc
                    self[(x + 1, y)] = 'Wall'
                    self[(x, y)] = 'EmptyFloor'
                    self[(x - 1, y)] = 'Wall'
                    if diff_y == 1:
                        self[(x, y + y_inc)] = 'Wall'
                        self[(x - x_inc, y + y_inc)] = 'Wall'
                elif hall_type == 'diag':
                    x = X
                    y = Y
                else:
                    break

    def place_player(self):
        """This method places the player on the map with the ascii character
           '1'"""
        coordinate = self['center']
        self[coordinate] = 'Player1'

    def add_stairs(self, number, direction):
        """This method adds stairs to the dungeon floor. It also uses the
           empty floors method to make sure the stair is welcome!"""
        coordinates = []
        if direction.lower() == 'both':
            coordinates += (self.empty_floors(number * 2))
            for i, coordinate in enumerate(coordinates):
                if i <= number:
                    self[coordinate] = 'StairsUp'
                else:
                    self[coordinate] = 'StairsDown'
        else:
            coordinates += (self.empty_floors(number))
            for coordinate in coordinates:
                self[coordinate] = direction

    def add_blocks(self, coordinates):
        """This method adds a Block to the dungeon floor using the '?' ascii
           character. It accepts a list of coordinates to add."""
        for coordinate in coordinates:
            self[coordinate] = 'Block'

    def add_spawners(self, density):
        """This method adds monster spawners to the dungeon floor with the
           ascii character 'M'. It uses the empty floors method to ensure a
           space is available."""
        area = self['area']
        total_spawners = round((area / 1000) * density)
        for coordinate in self.empty_floors(total_spawners):
            self[coordinate] = 'Spawner'

    def empty_floors(self, number):
        """Takes a specified number and generates a list of coordinates for
           the currently empty floors in the dungeon. Every round of the while
           loop it gets a random coordinate key and checks if its value in the
           dungeon map is an Empty floor. Then it appends the coordinate and
           removes all duplicates from itself. If it cannot find the specified
           number in number * 10 trials it gives up and returns whatever
           coordinates it did find."""
        coordinates = []
        trials = 0
        while number > len(coordinates):
            coordinate = Coords.random(self['length'], self['height'])
            trials += 1
            if self[coordinate] == 'EmptyFloor':
                coordinates.append(coordinate)
                coordinates = list(set(coordinates))
            elif trials > number * 10:
                break
        return coordinates

    def finalize(self):
        """This turns the map dictionary into a .txt file composed of the ascii
           characters defined in ascii's, the dictionary, keys."""
        all_doors = [k for k, v in self.items() if v == 'Door']
        for door in all_doors:
            X, Y = door
            if(
                self[(X + 1, Y)] == 'CastleWall' or
                self[(X - 1, Y)] == 'CastleWall' or
                self[(X, Y + 1)] == 'CastleWall' or
                self[(X, Y - 1)] == 'CastleWall'
            ):
                self[(X, Y)] = 'Wall'
        length = self['length']
        height = self['height']
        MAP = ''
        for y in range(height):
            for x in range(length):
                MAP += ascii[self[(x, y)]]
                if x == length - 1:
                    MAP += '\n'
        filename = root + "/level/%s.txt" % self.name
        with open(filename, "w") as f:
            f.write(MAP)
        del self
