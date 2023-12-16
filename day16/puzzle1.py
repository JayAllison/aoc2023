from functools import cache
import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


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

    @staticmethod
    @cache
    def move_in_direction(position: tuple) -> tuple[int, int]:
        y, x, direction = position
        if direction == 'north':
            y -= 1
        elif direction == 'south':
            y += 1
        elif direction == 'east':
            x += 1
        elif direction == 'west':
            x -= 1

        return y, x

    def is_valid(self, position: tuple) -> bool:
        y, x, direction = position
        if not (0 <= y < self.max_y and 0 <= x < self.max_x):
            return False
        if position in self.repeats:
            return False
        return True

    @cache
    def get_next_steps(self, current_position: tuple) -> list[tuple]:
        y, x, direction = current_position
        # print(f'({y},{x}) {layout[y][x]} {direction} -> ', end='')
        next_steps = []
        match self.layout[y][x]:
            case '.':  # pass straight through in any direction
                y, x = self.move_in_direction(current_position)
                next_position = (y, x, direction)
                if self.is_valid(next_position):
                    next_steps.append(next_position)

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

                y, x = self.move_in_direction((y, x, new_direction))
                next_position = (y, x, new_direction)
                if self.is_valid(next_position):
                    next_steps.append(next_position)

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

                y, x = self.move_in_direction((y, x, new_direction))
                next_position = (y, x, new_direction)
                if self.is_valid(next_position):
                    next_steps.append(next_position)

            case '-':  # east -> east, west -> west, north -> east & west, south -> east & west
                if direction == 'east' or direction == 'west':
                    y, x = self.move_in_direction((y, x, direction))
                    next_position = (y, x, direction)
                    if self.is_valid(next_position):
                        next_steps.append(next_position)
                elif direction == 'north' or direction == 'south':
                    new_direction = 'east'
                    y1, x1 = self.move_in_direction((y, x, new_direction))
                    next_position = (y1, x1, new_direction)
                    if self.is_valid(next_position):
                        next_steps.append(next_position)

                    new_direction = 'west'
                    y2, x2 = self.move_in_direction((y, x, new_direction))
                    next_position = (y2, x2, new_direction)
                    if self.is_valid(next_position):
                        next_steps.append(next_position)

            case '|':  # north -> north, south -> south, east -> north & south, west -> north & south
                if direction == 'north' or direction == 'south':
                    y, x = self.move_in_direction((y, x, direction))
                    next_position = (y, x, direction)
                    if self.is_valid(next_position):
                        next_steps.append(next_position)
                elif direction == 'east' or direction == 'west':
                    new_direction = 'north'
                    y1, x1 = self.move_in_direction((y, x, new_direction))
                    next_position = (y1, x1, new_direction)
                    if self.is_valid(next_position):
                        next_steps.append(next_position)

                    new_direction = 'south'
                    y2, x2 = self.move_in_direction((y, x, new_direction))
                    next_position = (y2, x2, new_direction)
                    if self.is_valid(next_position):
                        next_steps.append(next_position)

        # print(next_steps)
        return next_steps

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
