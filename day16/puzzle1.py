from functools import cache
# import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

# delta y and delta x to move in the specified direction
MOVES = {
    'north': (-1, 0),
    'south': (+1, 0),
    'east': (0, +1),
    'west': (0, -1)
}

# '/': redirect east -> north, west -> south, north -> east, south -> west
FORWARD_REFLECTION = {
    'north': 'east',
    'south': 'west',
    'east': 'north',
    'west': 'south'
}


# '\\' redirect east -> south, west -> north, north -> west, south -> east
BACKWARD_REFLECTION = {
    'north': 'west',
    'south': 'east',
    'east': 'south',
    'west': 'north'
}


class Contraption:

    layout: tuple
    max_y: int
    max_x: int
    active_points: list
    energized_points: set
    repeats: set

    def __init__(self, filename: str):
        self.layout = tuple(line.rstrip() for line in open(filename))
        self.max_y = len(self.layout)
        self.max_x = len(self.layout[0])
        # display_layout(layout)

    def display_layout(self):
        for row in self.layout:
            print(row)

    def display_energized(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (y, x) in self.energized_points:
                    print('#', end='')
                else:
                    print('.', end='')
            print()

    def _reset(self, position: tuple):
        y, x, direction = position
        self.active_points = [position]
        self.energized_points = {(y, x)}
        self.repeats = set(position)
        self.get_next_steps.cache_clear()

    @staticmethod
    def move_in_direction(position: tuple) -> tuple[int, int, str]:
        y, x, direction = position
        dy, dx = MOVES[direction]
        return y + dy, x + dx, direction

    def is_valid_move(self, position: tuple) -> bool:
        y, x, direction = position
        if not (0 <= y < self.max_y and 0 <= x < self.max_x):
            return False  # x,y is out of bounds
        if position in self.repeats:
            return False  # we are re-entering a loop we've already done - no need to continue
        return True

    def get_next_move(self, current_position: tuple) -> tuple | None:
        next_position = self.move_in_direction(current_position)
        if self.is_valid_move(next_position):
            return next_position
        return None

    @cache
    def get_next_steps(self, current_position: tuple) -> list[tuple]:
        y, x, direction = current_position
        # print(f'({y},{x}) {layout[y][x]} {direction} -> ', end='')
        next_steps = []
        match self.layout[y][x]:
            case '.':  # pass straight through in any direction
                next_steps.append(self.get_next_move((y, x, direction)))

            case '/':  # redirect east -> north, west -> south, north -> east, south -> west
                next_steps.append(self.get_next_move((y, x, FORWARD_REFLECTION[direction])))

            case '\\':  # redirect east -> south, west -> north, north -> west, south -> east
                next_steps.append(self.get_next_move((y, x, BACKWARD_REFLECTION[direction])))

            case '-':  # east -> east, west -> west, north -> east & west, south -> east & west
                if direction == 'east' or direction == 'west':
                    next_steps.append(self.get_next_move((y, x, direction)))
                elif direction == 'north' or direction == 'south':
                    next_steps.append(self.get_next_move((y, x, 'east')))
                    next_steps.append(self.get_next_move((y, x, 'west')))

            case '|':  # north -> north, south -> south, east -> north & south, west -> north & south
                if direction == 'north' or direction == 'south':
                    next_steps.append(self.get_next_move((y, x, direction)))
                elif direction == 'east' or direction == 'west':
                    next_steps.append(self.get_next_move((y, x, 'north')))
                    next_steps.append(self.get_next_move((y, x, 'south')))

        # print(next_steps)
        # only return the valid moves; discard the None's
        return [step for step in next_steps if step is not None]

    def energize(self, y: int, x: int, direction: str) -> int:
        self._reset((y, x, direction))
        while self.active_points:
            current_step = self.active_points.pop(0)
            self.energized_points.add((current_step[0], current_step[1]))
            self.repeats.add(current_step)
            self.active_points.extend(self.get_next_steps(current_step))

        # display_energized(layout, visited)
        return len(self.energized_points)


def main():
    contraption = Contraption(input_filename)
    print(contraption.energize(0, 0, 'east'))


if __name__ == '__main__':
    main()
