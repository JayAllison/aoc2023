import re
import itertools
# from pprint import pprint

# input_filename = 'sample_data'
# input_filename = 'sample2'
input_filename = 'input.txt'

# read in the input and find the bounds
schematic: list[str] = [line.rstrip() for line in open(input_filename)]
x_max = len(schematic[0])  # number of columns
y_max = len(schematic)  # number of rows

# the unique identifier of each part number is its starting position
# store every position containing a digit, mapping to the starting point of that full part number
part_number_positions: dict[tuple[int, int]: tuple[int, int]] = {}

# store every part number starting point mapped to the value of the part number
part_numbers: dict[tuple[int, int]: int] = {}

# Step 1: search schematic for all part numbers, one row at a time, and store off their locations and values
part_number_finder: re.Pattern = re.compile(r'[0-9]+')
for y in range(y_max):
    part_number_found: re.Match
    for part_number_found in part_number_finder.finditer(schematic[y]):
        part_number_start: tuple[int, int] = (part_number_found.start(), y)
        part_numbers[part_number_start] = int(part_number_found[0])
        for x in range(part_number_found.start(), part_number_found.end(), 1):
            part_number_positions[(x, y)] = part_number_start

print(f'Found {len(part_numbers)} part numbers.')

# store the detected gear ratios in a list, so we can sum it up afterward
gear_ratios: list[int] = []

# Step 2: search entire schematic, position by position
# when '*' is found, check to see if it's a gear, and, if so, calculate the gear ratio
gear_count: int = 0
for x, y in itertools.product(range(x_max), range(y_max)):
    if schematic[y][x] == '*':
        # let the set help us keep track of how many unique part numbers are adjacent
        adjacent_part_numbers: set[tuple[int, int]] = set()
        for x1, y1 in itertools.product(range(x-1, x+2, 1), range(y-1, y+2, 1)):
            if (x1, y1) in part_number_positions:
                adjacent_part_numbers.add(part_number_positions[(x1, y1)])
        if len(adjacent_part_numbers) == 2:
            gear_count += 1
            gear_ratios.append(part_numbers[adjacent_part_numbers.pop()] * part_numbers[adjacent_part_numbers.pop()])

print(f'Found {gear_count} gears.')

# Step 3: sum the gear ratios
print(f'Adjacent gear ratio sum = {sum(gear_ratios)}')
