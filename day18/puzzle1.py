from collections import deque
import pprint
import re

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

dig_plan = [line.rstrip().split() for line in open(input_filename)]

digger_path = []

current = (0, 0)
for instruction in dig_plan:
    direction, length, color = instruction
    for step in range(int(length)):
        y, x = current
        match direction:
            case 'U':
                y -= 1
            case 'D':
                y += 1
            case 'L':
                x += 1
            case 'R':
                x -= 1
        current = (y, x)
        digger_path.append(current)

# pprint.pprint(digger_path)

all_ys = [coord[0] for coord in digger_path]
min_y = min(all_ys)
max_y = max(all_ys)

all_xs = [coord[1] for coord in digger_path]
min_x = min(all_xs)
max_x = max(all_xs)

print(min_y, max_y)
print(min_x, max_x)

dig_map = [['.' for x in range(min_x, max_x + 2, 1)] for y in range(min_y, max_y + 1, 1)]

for point in digger_path:
    y, x = point
    dig_map[y - min_y][x - min_x] = '#'

with open('map_test.txt', 'w') as output:
    for row in dig_map:
        output.write(''.join(row) + '\n')
    output.write('\n')

# a simple fill algorithm should work - let's assume path is clockwise, so 1 D and 1 R from start should be good
max_height = len(dig_map)
max_width = len(dig_map[0])

# because of how I did the offsets, mine is mirrored, so down one and in one is really down out and out one
fill_from = deque([(-min_y + 1, -min_x - 1)])
while fill_from:
    y, x = fill_from.popleft()
    # print(f'Checking around ({y}, {x}):')
    for y1 in range(max(0, y - 1), min(max_height, y + 2), 1):
        for x1 in range(max(0, x - 1), min(max_width, x + 2), 1):
            # print(f'  ({y1}, {x1}) = {dig_map[y1][x1]}')
            if dig_map[y1][x1] == '.':
                dig_map[y1][x1] = '#'
                fill_from.append((y1, x1))

with open('map_test.txt', 'a') as output:
    for row in dig_map:
        output.write(''.join(row) + '\n')

count = sum([row.count('#') for row in dig_map])
print(count)
