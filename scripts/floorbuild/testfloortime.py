from scripts.mapgen.map import Map
from scripts.mapgen.draw import Draw
from scripts.mapgen.floor_generator import floor_generator
from time import time

generate = 10
start = time()

for i in range(generate):
    test = Map('test' + str(i + 1), 100, 60)
    floor_center = test['center']
    test.add_room(floor_center, 'square', (15, 20))
    coordinates = Draw.diamond(floor_center, 5, 'outline')
    test.add_blocks(coordinates)
    # test2 = test
    floor_generator('test', (100, 100), test, 20, 0, 0)
    del coordinates

end = time()
total_time = (end - start)
print(total_time)

