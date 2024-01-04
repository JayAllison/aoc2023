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

        yn: int = y - 1
        if yn >= 0 and self.trail_map[yn][x] == '.':  # cannot go north uphill
            steps.append((yn, x))

        ys: int = y + 1
        if ys < self.max_y and self.trail_map[ys][x] in '.vV':  # can go south downhill
            steps.append((ys, x))

        xw: int = x - 1
        if xw >= 0 and self.trail_map[y][xw] == '.':  # cannot go west uphill
            steps.append((y, xw))

        xe: int = x + 1
        if xe < self.max_x and self.trail_map[y][xe] in '.>':  # can go east downhill
            steps.append((y, xe))

        return steps

    # find starting point (the only '.' on the first row)
    # find valid next steps, don't go backwards
    # walk to the end (the only '.' on the last row)

    def hike(self) -> int:
        sy: int = 0
        sx: int = self.trail_map[sy].index('.')

        paths: list[list[tuple[int, int]]] = [[(sy, sx)]]
        lengths: list[int] = []

        while paths:
            path = paths.pop()
            if path[-1][0] == self.end_y:
                lengths.append(len(path) - 1)  # path is complete, save off len, but don't count the starting point
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
