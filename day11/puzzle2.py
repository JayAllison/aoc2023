# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

# SCALE = 2  # Part 1
# SCALE = 10  # Part 2, ex 1
# SCALE = 100  # Part 2, ex 2
SCALE = 1_000_000  # Part 2 - no answer given for example


def row_expansion_needed(image: list[list[str]], row: int) -> bool:
    row_test: set[str] = set(image[row])
    return len(row_test) == 1


def column_expansion_needed(image: list[list[str]], column: int) -> bool:
    column_test: set[str] = set([row[column] for row in image])
    return len(column_test) == 1


def expand(image: list[list[str]]) -> tuple[list[int], list[int]]:
    rows_to_expand: list[int] = []
    for row in range(len(image)):
        if row_expansion_needed(image, row):
            rows_to_expand.append(row)

    columns_to_expand: list[int] = []
    for column in range(len(image[0])):
        if column_expansion_needed(image, column):
            columns_to_expand.append(column)

    return rows_to_expand, columns_to_expand


def find_galaxies(image: list[list[str]]) -> list[tuple[int, int]]:
    galaxy_locations: list[tuple[int, int]] = []
    for y in range(len(image)):
        for x in range(len(image[y])):
            if image[y][x] == '#':
                galaxy_locations.append((y, x))
    return galaxy_locations


def measure_galaxies(galaxies: list[tuple[int, int]], expanded_rows: list[int], expanded_columns: list[int]) -> int:
    total: int = 0
    for g1 in galaxies:
        for g2 in galaxies:
            # measure Manhattan distance between the two, knowing that some of the steps need to be expanded
            y_distance = 0
            for y in range(min(g1[0], g2[0]), max(g1[0], g2[0]), 1):
                if y in expanded_rows:
                    y_distance += SCALE
                else:
                    y_distance += 1

            x_distance = 0
            for x in range(min(g1[1], g2[1]), max(g1[1], g2[1]), 1):
                if x in expanded_columns:
                    x_distance += SCALE
                else:
                    x_distance += 1

            total += y_distance + x_distance

    return total // 2  # TODO: fix this the right way by measuring each pair only once?


def main(filename: str):
    image: list[list[str]] = [[c for c in line.rstrip()] for line in open(filename).readlines()]

    expanded_rows, expanded_columns = expand(image)
    galaxies = find_galaxies(image)
    lengths_sum = measure_galaxies(galaxies, expanded_rows, expanded_columns)

    print(lengths_sum)


if __name__ == '__main__':
    main(input_filename)
