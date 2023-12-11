# input_filename: str = 'sample_data'  # answer should be 1
# input_filename: str = 'sample_data3'  # answer should be 4
# input_filename: str = 'sample_data4'  # answer should be 4
# input_filename: str = 'sample_data6'  # answer should be 8
# input_filename: str = 'sample_data7'  # answer should be 10
input_filename: str = 'input.txt'

inside_mark = ' '
outside_mark = 'O'


def display_map(pipe_map: list) -> None:
    print('='*len(pipe_map[0]))
    for row in pipe_map:
        print(''.join(row))
    print('='*len(pipe_map[0]))
    print()


def find_s(pipe_map: list) -> tuple[int | None, int | None]:
    for y in range(len(pipe_map)):
        for x in range(len(pipe_map[y])):
            if pipe_map[y][x] == 'S':
                return y, x
    return None, None


def step_away_from_s(pipe_map: list, s_y: int, s_x: int) -> tuple[int | None, int | None, str | None]:
    # check each direction and find one that leaves S properly
    steps_from_s = [(s_y - 1, s_x, 'north'), (s_y + 1, s_x, 'south'), (s_y, s_x - 1, 'west'), (s_y, s_x + 1, 'east')]
    for try_y, try_x, try_direction in steps_from_s:
        test_y, test_x, test_direction = get_next_step(pipe_map, try_y, try_x, try_direction)
        if test_direction:
            return try_y, try_x, try_direction

    return None, None, None


def clear_all_but_path(pipe_map: list, path_points: set) -> None:
    for y in range(len(pipe_map)):
        for x in range(len(pipe_map[y])):
            if (y, x) not in path_points:
                pipe_map[y][x] = inside_mark


# TODO: could this be simplified???
def get_next_step(pipe_map: list, y: int, x: int, direction: str) -> tuple[int | None, int | None, str | None]:
    if pipe_map[y][x] == '.':  # this should never happen, except when we're searching for ways to leave S
        return None, None, None
    elif pipe_map[y][x] == '|':
        if direction == 'south':
            return y + 1, x, direction
        elif direction == 'north':
            return y - 1, x, direction
    elif pipe_map[y][x] == '-':
        if direction == 'east':
            return y, x + 1, direction
        elif direction == 'west':
            return y, x - 1, direction
    elif pipe_map[y][x] == 'L':
        if direction == 'south':
            return y, x + 1, 'east'
        elif direction == 'west':
            return y - 1, x, 'north'
    elif pipe_map[y][x] == 'J':
        if direction == 'east':
            return y - 1, x, 'north'
        elif direction == 'south':
            return y, x - 1, 'west'
    elif pipe_map[y][x] == '7':
        if direction == 'east':
            return y + 1, x, 'south'
        elif direction == 'north':
            return y, x - 1, 'west'
    elif pipe_map[y][x] == 'F':
        if direction == 'west':
            return y + 1, x, 'south'
        elif direction == 'north':
            return y, x + 1, 'east'

    # this should only happen when we're checking around S for a step to take
    # print(f'Unable to find next step: ({x}, {y}) = {pipe_map[y][x]} -> {direction}')
    return None, None, None


def get_right_side(direction: str) -> str:
    # if you are facing 'direction' then which direction is to your right?
    match direction:
        case 'north':
            return 'east'
        case 'south':
            return 'west'
        case 'east':
            return 'south'
        case 'west':
            return 'north'


def mark_outside_of(pipe_map: list, y: int, x: int, direction: str, path_points: set) -> None:
    # print(f'Checking outside of ({y},{x}) {direction}')
    match direction:
        case 'north':
            y -= 1
        case 'south':
            y += 1
        case 'east':
            x += 1
        case 'west':
            x -= 1
    if (y, x) not in path_points and 0 <= y < len(pipe_map) and 0 <= x < len(pipe_map[0]):
        # print(f'  Marking ({y},{x})')
        pipe_map[y][x] = outside_mark
        # display_map(pipe_map)


def mark_adjacent_outsides(pipe_map: list) -> bool:
    found_any = False
    for y in range(len(pipe_map)):
        for x in range(len(pipe_map[y])):
            if pipe_map[y][x] == outside_mark:
                for ty in range(max(y - 1, 0), min(y + 2, len(pipe_map)), 1):
                    for tx in range(max(x - 1, 0), min(x + 2, len(pipe_map[y])), 1):
                        if pipe_map[ty][tx] == inside_mark:
                            found_any = True
                            pipe_map[ty][tx] = outside_mark

    return found_any


def count_map(pipe_map: list) -> tuple[int, int]:
    inside_count = 0
    outside_count = 0
    for pipe_row in pipe_map:
        inside_count += pipe_row.count(inside_mark)
        outside_count += pipe_row.count(outside_mark)
    return inside_count, outside_count


def main():
    # a map of the pipes, indexed by (y, x)
    pipe_map: list[list[str]] = [list(line.rstrip()) for line in open(input_filename).readlines()]

    # keep track of which points are on the path
    s_y, s_x = find_s(pipe_map)
    path_points: set[tuple[int, int]] = {(s_y, s_x)}

    # we need to determine which way to go from S - there will be two, and we'll take the first one we come to
    next_y, next_x, next_direction = step_away_from_s(pipe_map, s_y, s_x)

    # follow the path back to S
    while next_y != s_y or next_x != s_x:
        path_points.add((next_y, next_x))
        next_y, next_x, next_direction = get_next_step(pipe_map, next_y, next_x, next_direction)

    # now that we have the path, clear the grid of everything that is not the path itself
    clear_all_but_path(pipe_map, path_points)

    # display the path
    print('Before:')
    display_map(pipe_map)

    # follow the path again, marking the "outside" to the right
    # to the right is arbitrary, because I don't have a good way to determine actual inside vs outside
    current_y, current_x, current_direction = step_away_from_s(pipe_map, s_y, s_x)
    while current_y != s_y or current_x != s_x:
        mark_outside_of(pipe_map, current_y, current_x, get_right_side(current_direction), path_points)
        next_y, next_x, next_direction = get_next_step(pipe_map, current_y, current_x, current_direction)
        # mark again after turning corner - this will only have an effect for outside corners
        # we will still be missing the outside diagonal, but it turns out that does not affect the outcome
        if next_direction != current_direction:
            mark_outside_of(pipe_map, current_y, current_x, get_right_side(next_direction), path_points)
        current_y, current_x, current_direction = next_y, next_x, next_direction

    # display the path
    # display_map(pipe_map)

    # expand the outside we've found so far to all adjacent empty space
    found = True
    while found:
        found = mark_adjacent_outsides(pipe_map)
        # display the path
        # print('Filling in...')
        # display_map(pipe_map)

    # display the path
    print('After:')
    display_map(pipe_map)

    # count marks - we might have inside and outside backwards, since we just randomly picked one, so count both
    inside_count, outside_count = count_map(pipe_map)

    # for this puzzle, the inside is always smaller than the outside
    print()
    print(min(inside_count, outside_count))


if __name__ == '__main__':
    main()
