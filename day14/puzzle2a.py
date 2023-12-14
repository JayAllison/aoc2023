from functools import cache
import pprint

input_filename: str = 'sample_data'
# input_filename: str = 'input.txt'


def display_platform(platform: list | tuple) -> None:
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
    return platform[row_number].copy()


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


# make a mutable but not hashable translation
def listify(static_platform: tuple) -> list:
    return [list(row) for row in static_platform]


# make a hashable but not mutable translation
def tuplify(platform: list) -> tuple:
    return tuple(tuple(row) for row in platform)


# using tuple as the data structure so that we can memoize this function
@cache
def spin_cycle(static_platform: tuple) -> tuple:
    platform = listify(static_platform)
    for column_number in range(len(platform[0])):
        roll_column_north(platform, column_number)
    for row_number in range(len(platform)):
        roll_row_west(platform, row_number)
    for column_number in range(len(platform[0])):
        roll_column_south(platform, column_number)
    for row_number in range(len(platform)):
        roll_row_east(platform, row_number)
    return tuplify(platform)


@cache
def calculate_load(platform: tuple) -> int:
    load = 0
    platform_length = len(platform)
    for i in range(platform_length):
        o_count = platform[i].count('O')
        load += o_count * (platform_length - i)
    return load


def print_progress(i: int) -> None:
    if i % 10_000 == 0 and i > 0:
        print('*', flush=True)
    if i % 1_000 == 0 and i > 0:
        print('+', end='', flush=True)
    if i % 100 == 0 and i > 0:
        print('.', end='', flush=True)


def predict(weights, start, requested) -> int:
    return weights[((requested - start) % len(weights)) + start]


def solve(filename: str, spin_cycles: int) -> int:
    static_platform: tuple[tuple] = tuplify([[*line.rstrip()] for line in open(filename).readlines()])

    # TODO: this does not work, but it's got to be close, right???
    arrangements_seen = [static_platform]
    weights = {0: calculate_load(static_platform)}
    start_of_cycle = 0

    for i in range(spin_cycles):
        static_platform = spin_cycle(static_platform)
        weights[i+1] = calculate_load(static_platform)
        if static_platform in arrangements_seen:
            end_of_cycle = i
            print(f'Repeated platform found ending at {end_of_cycle}')
            start_of_cycle = arrangements_seen.index(static_platform)
            print(f'Repeats from {start_of_cycle}')
            break
        arrangements_seen.append(static_platform)

    pprint.pprint(weights)
    return predict(weights, start_of_cycle, spin_cycles)


if __name__ == '__main__':
    print(solve(input_filename, 1_000_000_000))
