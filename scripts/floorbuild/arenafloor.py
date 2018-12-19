from scripts.mapgen.map import Map
from scripts.mapgen.draw import Draw

test = Map('arena', 40, 40)
floor_center = test['center']
test.add_room(floor_center, 'square', (30, 30))
test.place_player()
coordinates: list = Draw.diamond(floor_center, 5, 'outline')
test.add_blocks(coordinates)
# test.addStairs(5, 'both')
# Map.add_room(test, floor_center, 'square', (10, 14))
# coordinates = Draw.square(floor_center, (5, 5), 'outline')
# coordinates = Draw.circle(floor_center, 9, 'outline')
test.add_spawners(1)
# for coord in coordinates:

# del coordinates
test.finalize()
del test