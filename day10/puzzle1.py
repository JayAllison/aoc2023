# input_filename: str = 'sample_data'
# input_filename: str = 'sample_data2'
input_filename: str = 'input.txt'


# a map of the pipes, indexed by (y.x)
pipe_map: list[str] = [line for line in open(input_filename).readlines()]


def get_next_step(y: int, x: int, direction: str) -> tuple[int | None, int | None, str | None]:
    if pipe_map[y][x] == '.':
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
    print(f'Unable to find next step: ({x}, {y}) = {pipe_map[y][x]} -> {direction}')
    return None, None, None


s_y, s_x = (0, 0)
# this is inefficient, because it does not break out early, but it works
for pipe_map_y in range(len(pipe_map)):
    for pipe_map_x in range(len(pipe_map[pipe_map_y])):
        if pipe_map[pipe_map_y][pipe_map_x] == 'S':
            s_y, s_x = (pipe_map_y, pipe_map_x)
            print(f'Found S @ ({s_x}, {s_y})')

# keep track of how many steps we have taken
step_count: int = 0

# we need to determine which way to go from S
steps_from_s = [(s_y - 1, s_x, 'north'), (s_y + 1, s_x, 'south'), (s_y, s_x - 1, 'west'), (s_y, s_x + 1, 'east')]
for try_y, try_x, try_direction in steps_from_s:
    test_y, test_x, test_direction = get_next_step(try_y, try_x, try_direction)
    if test_direction:
        print(f'Starting from S at ({try_x}, {try_y}), headed {try_direction}')
        next_y, next_x, next_direction = try_y, try_x, try_direction
        step_count += 1
        break

# walk the path
while next_y != s_y or next_x != s_x:
    print(f'From ({next_x}, {next_y}), ', end='', flush=True)
    next_y, next_x, next_direction = get_next_step(next_y, next_x, next_direction)
    print(f'headed {next_direction}')
    step_count += 1

print(f'Furthest path distance from S is {step_count//2}')
