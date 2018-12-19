from scripts.mapgen.map import Map
from scripts.mapgen.draw import Draw
from scripts.mapgen.floor_generator import floorGenerator


# ---------Map Editor--------
map_name = 'test'
map_length = 80
map_height = 80
start_room_type = 'square'  # accepts 'square', 'circle', or 'diamond'
start_room_position = (20, 20)  # accepts x, y coordinates in parentheses, e.g. (20, 20)
blocks = False
rnd_square_rooms = 5
rnd_circle_rooms = 0
rnd_diamond_rooms = 0

your_rooms_here = [
    'square,11,11,10,10',
    'circle,30,10,9',
    'square,20,40,8,8'
]
# key to your_rooms_here list:
# x is x_position
# y is y_position
# r is radius
# h is height
# l is length
# 'square,x,y,h,l',
# 'circle,x,y,r'
# 'diamond,x,y,r'

# -------------Developer Portion------------

test = Map(map_name, map_length, map_height)
floor_center = test['center']
# test.add_room(floor_center, 'circle', 15)
test.add_room(floor_center, start_room_type, start_room_position)

if len(your_rooms_here) > 0:
    for room in your_rooms_here:
        value = room.split(',')
        if value[0] == 'square':
            test.add_room((int(value[1]), int(value[2])), 'square', (int(value[3]), int(value[4])))
        if value[0] == 'circle':
            test.add_room((int(value[1]), int(value[2])), 'circle', int(value[3]))
        if value[0] == 'diamond':
            test.add_room((int(value[1]), int(value[2])), 'diamond', int(value[3]))
else:
    print('No rooms listed')

if blocks:
    coordinates: list = Draw.diamond(floor_center, 5, 'outline')
    test.add_blocks(coordinates)
floorGenerator('test', (100, 100), test, rnd_square_rooms, rnd_circle_rooms, rnd_diamdon_rooms)