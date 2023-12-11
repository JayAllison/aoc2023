# input_filename: str = 'sample_data'  # answer should be 1
# input_filename: str = 'sample_data3'  # answer should be 4
# input_filename: str = 'sample_data4'  # answer should be 4
input_filename: str = 'sample_data6'  # answer should be 8
# input_filename: str = 'sample_data7'  # answer should be 10
# input_filename: str = 'input.txt'

path_mark = '`'
inside_mark = ' '
outside_mark = 'O'

# a map of the pipes, indexed by (y.x)
pipe_map: list[list[str]] = [list(line.rstrip()) for line in open(input_filename).readlines()]


def display_map():
    print('='*len(pipe_map[0]))
    for row in pipe_map:
        print(''.join(row))
    print('='*len(pipe_map[0]))


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


def get_next_outside(prev_dir, next_dir, out):
    new_outside = None
    if prev_dir == next_dir:
        return out
    else:
        if prev_dir == 'south' and next_dir == 'east':
            if out == 'west':
                new_outside = 'south'
            elif out == 'east':
                new_outside = 'north'
        elif prev_dir == 'south' and next_dir == 'west':
            if out == 'west':
                new_outside = 'north'
            elif out == 'east':
                new_outside = 'south'
        elif prev_dir == 'north' and next_dir == 'west':
            if out == 'west':
                new_outside = 'south'
            elif out == 'east':
                new_outside = 'north'
        elif prev_dir == 'north' and next_dir == 'east':
            if out == 'west':
                new_outside = 'north'
            elif out == 'east':
                new_outside = 'south'
        elif prev_dir == 'east' and next_dir == 'north':
            if out == 'north':
                new_outside = 'west'
            elif out == 'south':
                new_outside = 'east'
        elif prev_dir == 'east' and next_dir == 'south':
            if out == 'north':
                new_outside = 'east'
            elif out == 'south':
                new_outside = 'west'
        elif prev_dir == 'west' and next_dir == 'south':
            if out == 'north':
                new_outside = 'west'
            elif out == 'south':
                new_outside = 'east'
        elif prev_dir == 'west' and next_dir == 'north':
            if out == 'north':
                new_outside = 'east'
            elif out == 'south':
                new_outside = 'west'
        if new_outside is None:
            print(f'failed to find new outside for {prev_dir}->{next_dir},{out}')
        return new_outside


def mark_surrounding(sy, sx):
    if (sy, sx) not in path_points:
        for ty in range(max(sy-1, 0), min(sy+2, len(pipe_map)), 1):
            for tx in range(max(sx-1, 0), min(sx+2, len(pipe_map[0])), 1):
                print(f'({sy}, {sx}): checking ({ty}, {tx})')
                if (ty, tx) not in path_points and pipe_map[ty][tx] != outside_mark:
                    pipe_map[ty][tx] = outside_mark
                    print(f'  ({sy}, {sx}) -> ({ty}, {tx}):')
                    display_map()
                    print()
                    mark_surrounding(ty, tx)


def mark_outside(from_y, from_x, outside_direction):
    # the flaw in this simple approach is inside corners
    # for now, do not mark corners - let's see if that works...
    if not pipe_map[from_y][from_x] in 'F7LJ':
        my, mx = None, None
        if outside_direction == 'north':
            my, mx = from_y - 1, from_x
        elif outside_direction == 'south':
            my, mx = from_y + 1, from_x
        elif outside_direction == 'east':
            my, mx = from_y, from_x + 1
        elif outside_direction == 'west':
            my, mx = from_y, from_x - 1

        print(f'Outside is ({my}, {mx})')
        mark_surrounding(my, mx)


# keep track of which points are on the path
path_points: set[tuple[int, int]] = set()
s_y, s_x = (0, 0)
# this is inefficient, because it does not break out early, but it works
for pipe_map_y in range(len(pipe_map)):
    for pipe_map_x in range(len(pipe_map[pipe_map_y])):
        if pipe_map[pipe_map_y][pipe_map_x] == 'S':
            s_y, s_x = (pipe_map_y, pipe_map_x)
            path_points.add((s_y, s_x))
            # print(f'Found S @ ({s_x}, {s_y})')

# we need to determine which way to go from S
next_y, next_x, next_direction = None, None, None
first_y, first_x, first_direction = None, None, None
steps_from_s = [(s_y - 1, s_x, 'north'), (s_y + 1, s_x, 'south'), (s_y, s_x - 1, 'west'), (s_y, s_x + 1, 'east')]
for try_y, try_x, try_direction in steps_from_s:
    test_y, test_x, test_direction = get_next_step(try_y, try_x, try_direction)
    if test_direction:
        # print(f'Starting from S at ({try_x}, {try_y}), headed {try_direction}')
        next_y, next_x, next_direction = try_y, try_x, try_direction
        first_y = next_y
        first_x = next_x
        first_direction = next_direction
        break

# follow the path
while next_y != s_y or next_x != s_x:
    path_points.add((next_y, next_x))
    # print(f'From ({next_x}, {next_y}), ', end='', flush=True)
    next_y, next_x, next_direction = get_next_step(next_y, next_x, next_direction)
    # print(f'headed {next_direction}')

# now that we have the path, clear everything that is not the path
for pipe_map_y in range(len(pipe_map)):
    for pipe_map_x in range(len(pipe_map[pipe_map_y])):
        if (pipe_map_y, pipe_map_x) not in path_points:
            pipe_map[pipe_map_y][pipe_map_x] = inside_mark

# display the path
display_map()

# follow the path again, this time marking the "outside"
next_y, next_x, next_direction = first_y, first_x, first_direction

# arbitrarily pick a direction to be the outside
if first_direction == 'north' or first_direction == 'south':
    outside = 'east'
else:
    outside = 'south'

# outline the outside of the path
while next_y != s_y or next_x != s_x:
    # trace the outside
    print(f'Marking outside ({next_y}, {next_x}) to {outside}')
    mark_outside(next_y, next_x, outside)

    # print(f'From ({next_x}, {next_y}), ', end='', flush=True)
    previous_direction = next_direction
    next_y, next_x, next_direction = get_next_step(next_y, next_x, next_direction)
    outside = get_next_outside(previous_direction, next_direction, outside)
    # print(f'headed {next_direction}, outside is {outside}')

# display the ones we found
display_map()

# count marks - we might have inside and outside backwards, since we just randomly picked one, so count both
inside_count = 0
outside_count = 0
for pipe_row in pipe_map:
    inside_count += pipe_row.count(inside_mark)
    outside_count += pipe_row.count(outside_mark)

print()
print(inside_count, outside_count)
