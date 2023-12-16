from functools import cache
import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


def display_layout(layout: list[str]):
    for row in layout:
        print(row)


def display_energized(layout: list[str], energized_points: set):
    for y in range(len(layout)):
        for x in range(len(layout[y])):
            if (y, x) in energized_points:
                print('#', end='')
            else:
                print('.', end='')
        print()


def move_in_direction(y: int, x: int, direction: str) -> tuple[int, int]:
    if direction == 'north':
        y -= 1
    elif direction == 'south':
        y += 1
    elif direction == 'east':
        x += 1
    elif direction == 'west':
        x -= 1

    return y, x


def get_next_steps(layout: list[str], current: tuple) -> list[tuple]:
    y, x, direction = current
    # print(f'({y},{x}) {layout[y][x]} {direction} -> ', end='')
    next_steps = []
    match layout[y][x]:
        case '.':  # pass straight through in any direction
            y, x = move_in_direction(y, x, direction)
            if 0 <= y < len(layout) and 0 <= x < len(layout[y]):
                next_steps.append((y, x, direction))

        case '/':  # redirect east -> north, west -> south, north -> east, south -> west
            if direction == 'north':
                new_direction = 'east'
            elif direction == 'south':
                new_direction = 'west'
            elif direction == 'east':
                new_direction = 'north'
            elif direction == 'west':
                new_direction = 'south'
            else:
                new_direction = 'unknown'

            y, x = move_in_direction(y, x, new_direction)
            if 0 <= y < len(layout) and 0 <= x < len(layout[y]):
                next_steps.append((y, x, new_direction))

        case '\\':  # redirect east -> south, west -> north, north -> west, south -> east
            if direction == 'north':
                new_direction = 'west'
            elif direction == 'south':
                new_direction = 'east'
            elif direction == 'east':
                new_direction = 'south'
            elif direction == 'west':
                new_direction = 'north'
            else:
                new_direction = 'unknown'

            y, x = move_in_direction(y, x, new_direction)
            if 0 <= y < len(layout) and 0 <= x < len(layout[y]):
                next_steps.append((y, x, new_direction))

        case '-':  # east -> east, west -> west, north -> east & west, south -> east & west
            if direction == 'east' or direction == 'west':
                y, x = move_in_direction(y, x, direction)
                if 0 <= y < len(layout) and 0 <= x < len(layout[y]):
                    next_steps.append((y, x, direction))
            elif direction == 'north' or direction == 'south':
                new_direction = 'east'
                y1, x1 = move_in_direction(y, x, new_direction)
                if 0 <= y1 < len(layout) and 0 <= x1 < len(layout[y]):
                    next_steps.append((y1, x1, new_direction))

                new_direction = 'west'
                y2, x2 = move_in_direction(y, x, new_direction)
                if 0 <= y2 < len(layout) and 0 <= x2 < len(layout[y]):
                    next_steps.append((y2, x2, new_direction))

        case '|':  # north -> north, south -> south, east -> north & south, west -> north & south
            if direction == 'north' or direction == 'south':
                y, x = move_in_direction(y, x, direction)
                if 0 <= y < len(layout) and 0 <= x < len(layout[y]):
                    next_steps.append((y, x, direction))
            elif direction == 'east' or direction == 'west':
                new_direction = 'north'
                y1, x1 = move_in_direction(y, x, new_direction)
                if 0 <= y1 < len(layout) and 0 <= x1 < len(layout[y]):
                    next_steps.append((y1, x1, new_direction))

                new_direction = 'south'
                y2, x2 = move_in_direction(y, x, new_direction)
                if 0 <= y2 < len(layout) and 0 <= x2 < len(layout[y]):
                    next_steps.append((y2, x2, new_direction))

    # print(next_steps)
    return next_steps


def energize(filename: str) -> int:
    layout = [line.rstrip() for line in open(filename)]
    # display_layout(layout)

    active = [(0, 0, 'east')]  # starting point, starting direction
    visited: set[tuple[int, int]] = {(0, 0)}
    visited_size = len(visited)
    visited_unchanged_count = 100_000_000
    last_count = None

    while active and visited_unchanged_count > 0:
        if visited_size == len(visited):
            visited_unchanged_count -= 1
            if visited_size != last_count:
                last_count = visited_size
                print(visited_size)
        visited_size = len(visited)
        current_step = active.pop(0)
        visited.add((current_step[0], current_step[1]))
        active.extend(get_next_steps(layout, current_step))

    # display_energized(layout, visited)
    return len(visited)


if __name__ == '__main__':
    print(energize(input_filename))
