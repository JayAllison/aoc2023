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


def roll_column_north(platform: list, column_number: int) -> None:
    column = get_column(platform, column_number)
    # print(f'Before: {''.join(column)}')
    start = 0
    while start < len(column):
        if column[start:].count('#'):
            end = column.index('#', start)
        else:
            end = len(column)

        o_count = column[start:end].count('O')

        for i in range(start, end):
            if i < start + o_count:
                column[i] = 'O'
            else:
                column[i] = '.'

        start = end + 1
    # print(f'After:  {''.join(column)}\n')
    set_column(platform, column_number, column)


def calculate_load(platform: list) -> int:
    load = 0
    platform_length = len(platform)
    for i in range(platform_length):
        o_count = platform[i].count('O')
        load += o_count * (platform_length - i)
    return load


def solve(filename: str) -> int:
    platform = [[*line.rstrip()] for line in open(filename).readlines()]
    for column_number in range(len(platform[0])):
        roll_column_north(platform, column_number)
    display_platform(platform)
    return calculate_load(platform)


if __name__ == '__main__':
    print(solve(input_filename))
