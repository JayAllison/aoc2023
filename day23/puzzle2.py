import datetime
# from pprint import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


# using a class just so I don't have to pass so many variables into each method
class Hiker:

    trail_map: list[str]
    max_y: int
    end_y: int
    max_x: int

    def __init__(self, filename):
        self.trail_map = [line.rstrip() for line in open(filename)]
        self.max_y = len(self.trail_map)
        self.end_y = self.max_y - 1
        self.max_x = len(self.trail_map[0])  # assumes every row is the same width

    def get_valid_adjacent_steps(self, loc: tuple) -> list[tuple]:
        steps: list[tuple[int, int]] = []
        y, x = loc

        potentials = [(_y, x) for _y in (y - 1, y + 1) if 0 <= _y < self.max_y]  # check N and S for steps within range
        potentials += [(y, _x) for _x in (x - 1, x + 1) if 0 <= _x < self.max_x]  # check W and E for steps within range

        for py, px in potentials:
            if self.trail_map[py][px] != '#':  # Part 2: anything that is not "forest" is okay to walk on
                steps.append((py, px))

        return steps

    # find starting point (the only '.' on the first row)
    # find valid next steps, don't go backwards
    # walk to the end (the only '.' on the last row)

    def hike(self) -> int:
        sy: int = 0
        sx: int = self.trail_map[sy].index('.')

        paths: list[list[tuple[int, int]]] = [[(sy, sx)]]
        lengths: list[int] = []

        start = datetime.datetime.now()

        while paths:
            path = paths.pop()
            if path[-1][0] == self.end_y:
                lengths.append(len(path) - 1)  # path is complete, save off len, but don't count the starting point
                print(f'{datetime.datetime.now() - start} Path {len(lengths)}: reached end after {len(path) - 1} steps, with {len(paths)} other paths still in progress - max is {max(lengths)}')
            else:
                # for each valid adjacent step that is not reversing our current path, move forward
                for next_step in self.get_valid_adjacent_steps(path[-1]):
                    if next_step not in path:
                        paths.append(path + [next_step])
                        # pprint(paths)

        # pprint(sorted(lengths, reverse=True))
        return max(lengths)


if __name__ == '__main__':
    print(Hiker(input_filename).hike())
