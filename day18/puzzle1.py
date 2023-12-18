from collections import deque
# import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

dig_plan: list[list[str]] = [line.rstrip().split() for line in open(input_filename)]

digger_path: list[tuple] = []

# lookup table for deltas to move in the specified direction
MOVES = {
    'U': (-1, 0),
    'D': (+1, 0),
    'L': (0, -1),
    'R': (0, +1),
}

# trace out the digger path
current: tuple[int, int] = (0, 0)
for instruction in dig_plan:
    direction, length, color = instruction
    for step in range(int(length)):
        y, x = current
        dy, dx = MOVES[direction]
        current = (y + dy, x + dx)
        digger_path.append(current)

# pprint.pprint(digger_path)

# the digger path coordinates are relative, not absolute, so we need to offset them into a grid of positive numbers
all_ys: list[int] = [coord[0] for coord in digger_path]
min_y: int = min(all_ys)
max_y: int = max(all_ys)

all_xs: list[int] = [coord[1] for coord in digger_path]
min_x: int = min(all_xs)
max_x: int = max(all_xs)

# print(min_y, max_y)
# print(min_x, max_x)

# lay out an absolute grid
dig_map: list[list[str]] = [['.' for x in range(min_x, max_x + 2, 1)] for y in range(min_y, max_y + 1, 1)]

# trace out the digger path in the grid
for point in digger_path:
    y, x = point
    dig_map[y - min_y][x - min_x] = '#'

# the output is too wide for my terminal - use a file instead
with open('map_test.txt', 'w') as output:
    for row in dig_map:
        output.write(''.join(row) + '\n')
    output.write('\n')

max_height: int = len(dig_map)
max_width: int = len(dig_map[0])

# a simple fill algorithm should work - let's assume path is clockwise, so 1 ⬇ and 1 ➡ from start should be good
# relative start was (0, 0), so offsets to absolute start is (-min_y, -min_x)
fill_from: deque = deque([(-min_y + 1, -min_x + 1)])
while fill_from:
    y, x = fill_from.popleft()
    # print(f'Checking around ({y}, {x}):')
    for y1 in range(max(0, y - 1), min(max_height, y + 2), 1):
        for x1 in range(max(0, x - 1), min(max_width, x + 2), 1):
            # print(f'  ({y1}, {x1}) = {dig_map[y1][x1]}')
            if dig_map[y1][x1] == '.':
                dig_map[y1][x1] = '#'
                fill_from.append((y1, x1))

# the output is too wide for my terminal - use a file instead
with open('map_test.txt', 'a') as output:
    for row in dig_map:
        output.write(''.join(row) + '\n')

# brute force: count out the spots
print(sum([row.count('#') for row in dig_map]))
