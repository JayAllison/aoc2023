from collections import defaultdict
from functools import cache
import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


def display_platform(platform: list) -> None:
    print('='*10)
    for row in platform:
        print(''.join(row))
    print('='*10)


def get_column(platform: list, column_number: int) -> list:
    return [row[column_number] for row in platform]


def set_column(platform: list, column_number: int, column: list) -> None:
    for row in platform:
        row[column_number] = column.pop(0)


def get_row(platform: list, row_number: int) -> list:
    return platform[row_number].copy()  # do I really need the copy, or could this just be a reference to the original?


def set_row(platform: list, row_number: int, row: list) -> None:
    for i in range(len(platform[row_number])):
        platform[row_number][i] = row.pop(0)


def roll_left(rock_list: list):
    # print(f'Before: {''.join(column)}')
    start = 0
    while start < len(rock_list):
        if rock_list[start:].count('#'):
            end = rock_list.index('#', start)
        else:
            end = len(rock_list)

        o_count = rock_list[start:end].count('O')

        for i in range(start, end):
            if i < start + o_count:
                rock_list[i] = 'O'
            else:
                rock_list[i] = '.'

        start = end + 1
    # print(f'After:  {''.join(column)}\n')


def roll_column_north(platform: list, column_number: int) -> None:
    column = get_column(platform, column_number)
    roll_left(column)
    set_column(platform, column_number, column)


def roll_column_south(platform: list, column_number: int) -> None:
    column = get_column(platform, column_number)
    column.reverse()
    roll_left(column)
    column.reverse()
    set_column(platform, column_number, column)


def roll_row_west(platform: list, row_number: int) -> None:
    row = get_row(platform, row_number)
    roll_left(row)
    set_row(platform, row_number, row)


def roll_row_east(platform: list, row_number: int) -> None:
    row = get_row(platform, row_number)
    row.reverse()
    roll_left(row)
    row.reverse()
    set_row(platform, row_number, row)


def calculate_load(platform: list) -> int:
    load = 0
    platform_length = len(platform)
    for i in range(platform_length):
        o_count = platform[i].count('O')
        load += o_count * (platform_length - i)
    return load


def spin_cycle(platform) -> None:
    for column_number in range(len(platform[0])):
        roll_column_north(platform, column_number)
    for row_number in range(len(platform)):
        roll_row_west(platform, row_number)
    for column_number in range(len(platform[0])):
        roll_column_south(platform, column_number)
    for row_number in range(len(platform)):
        roll_row_east(platform, row_number)


def print_progress(i: int) -> None:
    if i % 10_000 == 0 and i > 0:
        print('*', flush=True)
    if i % 1_000 == 0 and i > 0:
        print('+', end='', flush=True)
    if i % 100 == 0 and i > 0:
        print('.', end='', flush=True)


# TODO: generate this with code rather than copying and pasting it from the terminal
lookup_table = {
    215: 96071, 
    216: 96059,
    217: 96065, 
    218: 96069, 
    219: 96056, 
    220: 96027, 
    221: 95998, 
    222: 95967, 
    223: 95934, 
    224: 95901, 
    225: 95854, 
    226: 95820, 
    227: 95795, 
    228: 95768, 
    229: 95751, 
    230: 95750, 
    231: 95734, 
    232: 95737, 
    233: 95757, 
    234: 95759, 
    235: 95784, 
    236: 95830, 
    237: 95858, 
    238: 95880, 
    239: 95908, 
    240: 95920, 
    241: 95964, 
    242: 96007, 
    243: 96014, 
    244: 96043, 
    245: 96068, 
    246: 96061, 
    247: 96060, 
    248: 96074, 
    249: 96059,
    250: 96057, 
    251: 96036, 
    252: 95988, 
    253: 95968, 
    254: 95943, 
    255: 95891, 
    256: 95855, 
    257: 95829, 
    258: 95785, 
    259: 95769, 
    260: 95760, 
    261: 95740, 
    262: 95735, 
    263: 95746, 
    264: 95747, 
    265: 95760, 
    266: 95793, 
    267: 95820, 
    268: 95859, 
    269: 95889, 
    270: 95898, 
    271: 95921, 
    272: 95973, 
    273: 95997, 
    274: 96015, 
    275: 96052, 
    276: 96058, 
    277: 96062, 
    278: 96069, 
    279: 96064, 
    280: 96060, 
    281: 96066, 
    282: 96026, 
    283: 95989, 
    284: 95977, 
    285: 95933, 
    286: 95892, 
    287: 95864, 
    288: 95819, 
    289: 95786, 
    290: 95778, 
    291: 95750, 
    292: 95741, 
    293: 95744, 
    294: 95736, 
    295: 95748, 
    296: 95769, 
    297: 95783, 
    298: 95821, 
    299: 95868, 
    300: 95879, 
    301: 95899, 
    302: 95930, 
    303: 95963, 
    304: 95998, 
    305: 96024, 
    306: 96042, 
    307: 96059
}


def predict(i: int) -> int:
    start = 215
    return lookup_table[((i - start) % len(lookup_table)) + start]


def solve(filename: str, spin_cycles: int) -> int:
    platform = [[*line.rstrip()] for line in open(filename).readlines()]
    for i in range(spin_cycles):
        print_progress(i)
        spin_cycle(platform)
        current_load = calculate_load(platform)
        predicted_load = predict(i)
        if i > 215:
            if current_load != predicted_load:
                print(f'for {i=} {predicted_load=} != {current_load=}')
        # display_platform(platform)
    return calculate_load(platform)


if __name__ == '__main__':
    cycles = 100_000
    # cycles = 1_000_000_000
    # print(solve(input_filename, cycles))
    print(predict(1000000000-1))