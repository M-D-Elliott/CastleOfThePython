from scripts.mapgen.map import Map
from scripts.mapgen.draw import Draw


def floor_generator(name, size, preset_floor, rnd_squares, rnd_circles, rnd_diamonds):
    lth, h = size
    floor = None
    if preset_floor == 'random':
        floor = Map(name, lth, h)
    else:
        floor = preset_floor
    for _ in range(rnd_squares):
        floor.add_room('random', 'square', 'random')
    for _ in range(rnd_circles):
        floor.add_room('random', 'circle', 'random')
    for _ in range(rnd_diamonds):
        floor.add_room('random', 'diamond', 'random')
    floor.add_spawners(1)
    floor.add_hallways()
    # floor.add_hallways()
    floor.place_player()
    floor.finalize()
    return name
