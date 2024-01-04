# input_filename: str = 'sample_data'; steps_needed = 6
input_filename: str = 'input.txt'; steps_needed = 64


# using a class just so I don't have to pass so many variables into each method
class GardenStepper:

    steps_needed: int

    garden_map: list[str]
    max_y: int
    max_x: int

    def __init__(self, filename: str, steps: int):
        self.steps_needed = steps

        self.garden_map = [line.rstrip() for line in open(filename)]
        self.max_y = len(self.garden_map)
        self.max_x = len(self.garden_map[0])  # assumes every row is the same width

    def print_map_with_steps(self, steps: set[tuple]) -> None:
        for y in range(self.max_y):
            for x in range(self.max_y):
                if (y, x) in steps:
                    print('O', end='')
                else:
                    print(self.garden_map[y][x], end='')
            print()
        print()

    def get_valid_next_steps(self, loc: tuple) -> list[tuple]:
        steps = []
        y, x = loc
        potentials = [(_y, x) for _y in (y - 1, y + 1) if 0 <= _y < self.max_y]  # check N and S for steps within range
        potentials += [(y, _x) for _x in (x - 1, x + 1) if 0 <= _x < self.max_x]  # check W and E for steps within range
        for py, px in potentials:
            if self.garden_map[py][px] in '.S':  # potential is a valid next step if it is garden ('.' or 'S')
                steps.append((py, px))
        return steps

    def solve(self) -> int:
        # find the starting point
        sy, sx = (-1, -1)
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.garden_map[y][x] == 'S':
                    sy = y
                    sx = x

        current_positions: set[tuple] = {(sy, sx)}  # starting from the coordinates of 'S'

        # for each round, step out one from each previous position to find the next round of unique positions
        for i in range(self.steps_needed):
            next_steps = set()
            for coord in current_positions:
                next_steps.update(self.get_valid_next_steps(coord))
            current_positions = next_steps
            # self.print_map_with_steps(next_steps)

        return len(current_positions)


if __name__ == '__main__':
    print(GardenStepper(input_filename, steps_needed).solve())
