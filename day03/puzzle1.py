import re
import itertools
from pprint import pprint

# input_filename: str = 'sample_data'
# input_filename: str = 'sample2'
input_filename: str = 'input.txt'

# read in the input and find the bounds
schematic: list[str] = [line.rstrip() for line in open(input_filename)]
X_MAX: int = len(schematic[0])  # number of columns
Y_MAX: int = len(schematic)  # number of rows

# the unique identifier of each part number is its starting position
# store every position containing a digit, mapping to the starting point of that full part number
part_number_positions: dict[tuple[int, int]: tuple[int, int]] = {}

# store every part number starting point mapped to the value of the part number
part_numbers: dict[tuple[int, int]: int] = {}

# Step 1: search for all part numbers, and store off their locations and values
part_number_finder: re.Pattern = re.compile(r'[0-9]+')
for y in range(Y_MAX):
    part_number_found: re.Match
    for part_number_found in part_number_finder.finditer(schematic[y]):
        part_number_start: tuple[int, int] = (part_number_found.start(), y)
        part_numbers[part_number_start] = int(part_number_found[0])
        for x in range(part_number_found.start(), part_number_found.end(), 1):
            part_number_positions[(x, y)] = part_number_start

print(f'Found {len(part_numbers)} part numbers.')

# store all found part number starting positions in a set, so we only include each part number once
adjacent_part_number_starting_positions: set[tuple[int, int]] = set()

# Step 2: find symbols and check adjacent positions for the presence of a part number
symbol_count: int = 0
for x, y in itertools.product(range(X_MAX), range(Y_MAX)):
    if schematic[y][x] not in '0123456789.':
        symbol_count += 1
        for x1, y1 in itertools.product(range(x-1, x+2, 1), range(y-1, y+2, 1)):
            if (x1, y1) in part_number_positions:
                adjacent_part_number_starting_positions.add(part_number_positions[(x1, y1)])

print(f'Found {symbol_count} symbols.')
print(f'Found {len(adjacent_part_number_starting_positions)} adjacent part numbers.')

# Step 3: sum the part numbers that we identified
adjacent_part_numbers: list[int] = [part_numbers[p] for p in adjacent_part_number_starting_positions]
print(f'Adjacent part number sum = {sum(adjacent_part_numbers)}')
