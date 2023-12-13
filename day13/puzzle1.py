# import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


def get_row(pattern: list, row: int) -> list:
    return pattern[row]


def get_column(pattern: list, column: int) -> list:
    return [row[column] for row in pattern]


def find_horizontal_reflection_point(pattern: list) -> int | None:
    size = len(pattern)
    for row in range(0, size - 1, 1):
        # print(f'Starting with row {row}')
        matching = True
        i = 0
        while matching:
            # print(f'  comparing rows {row - i} and {row + i + 1}')
            if get_row(pattern, row - i) != get_row(pattern, row + i + 1):
                matching = False
            elif row - i == 0 or row + i + 1 == size - 1:
                # print(f'found match at row {row + 1}')
                return row + 1
            i += 1

    return None


def find_vertical_reflection_point(pattern: list) -> int | None:
    size = len(pattern[0])
    for column in range(0, size - 1, 1):
        # print(f'Starting with column {column}')
        matching = True
        i = 0
        while matching:
            # print(f'  comparing columns {column - i} and {column + i + 1}')
            if get_column(pattern, column - i) != get_column(pattern, column + i + 1):
                matching = False
            elif column - i == 0 or column + i + 1 == size - 1:
                # print(f'found match at column {column + 1}')
                return column + 1
            i += 1

    return None


def find_reflection_values(pattern: list) -> int:
    if h_value := find_horizontal_reflection_point(pattern):
        return h_value * 100
    elif v_value := find_vertical_reflection_point(pattern):
        return v_value
    else:
        print('Failed to find reflection for pattern!')
        return 0


def solve(filename: str) -> int:
    patterns = [[row for row in pattern.split('\n')] for pattern in open(filename).read().rstrip().split('\n\n')]
    summary = 0
    for pattern in patterns:
        summary += find_reflection_values(pattern)
    return summary


if __name__ == '__main__':
    print(solve(input_filename))
