from scripts.mapgen.map import Map
from scripts.mapgen.draw import Draw
from scripts.mapgen.floor_generator import floor_generator


def random_diamond_floor():
    floor = Map('randdiamondfloor', 100, 60)
    floor_center = floor['center']
    floor.add_room(floor_center, 'square', (15, 20))
    coordinates = Draw.diamond(floor_center, 5, 'outline')
    floor.add_blocks(coordinates)
    del coordinates
    return floor_generator('randdiamondfloor', (100, 100), floor, 20, 0, 0)

