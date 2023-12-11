# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


def display_image(image: list[list[str]]) -> None:
    print()
    for row in image:
        print(''.join(row))
    print()


def row_expansion_needed(image: list[list[str]], row: int) -> bool:
    row_test = set(image[row])
    return len(row_test) == 1


def add_row(image: list[list[str]], row: int) -> None:
    image.insert(row, image[row].copy())


def column_expansion_needed(image: list[list[str]], column: int) -> bool:
    column_test = set([row[column] for row in image])
    return len(column_test) == 1


def add_column(image: list[list[str]], column: int) -> None:
    for row in image:
        row.insert(column, '.')


def expand(image: list[list[str]]) -> None:
    row = 0
    while row < len(image):
        if row_expansion_needed(image, row):
            add_row(image, row)
            row += 1
        row += 1

    column = 0
    while column < len(image[0]):
        if column_expansion_needed(image, column):
            add_column(image, column)
            column += 1
        column += 1


def find_galaxies(image: list[list[str]]) -> list[tuple[int, int]]:
    galaxy_locations: list[tuple[int, int]] = []
    for y in range(len(image)):
        for x in range(len(image[y])):
            if image[y][x] == '#':
                galaxy_locations.append((y, x))
    return galaxy_locations


def measure_galaxies(galaxies: list[tuple[int, int]]) -> int:
    total = 0
    for g1 in galaxies:
        for g2 in galaxies:
            total += abs(g2[0] - g1[0]) + abs(g2[1] - g1[1])
    return total // 2  # TODO: fix this the right way?


def main():
    image = [[c for c in line.rstrip()] for line in open(input_filename).readlines()]

    expand(image)
    galaxies = find_galaxies(image)
    lengths_sum = measure_galaxies(galaxies)

    print(lengths_sum)


if __name__ == '__main__':
    main()
