import math
import pprint

input_filename: str = 'test_path'
# input_filename: str = 'sample_data'
# input_filename: str = 'input.txt'

# Let's do Dijkstra's! https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm


class HeatMap:

    heatmap: list[list[int]]
    unvisited_nodes: dict
    visited_nodes: dict
    start: tuple
    current: tuple
    end: tuple

    def __init__(self, filename: str):
        self.heatmap = [[int(c) for c in line.rstrip()] for line in open(filename)]
        self.max_y: int = len(self.heatmap)
        self.max_x: int = len(self.heatmap[0])

    def initialize(self) -> None:
        all_points = [(y, x) for y in range(self.max_y) for x in range(self.max_x)]
        self.unvisited_nodes: dict[tuple: int] = {point: [math.inf, []] for point in all_points}
        self.visited_nodes: dict[tuple: int] = {}
        self.start = (0, 0)
        self.end = (self.max_y - 1, self.max_x - 1)
        self.unvisited_nodes[self.start] = [0, []]
        self.current = self.start

    def up_down_left_right_from_current(self):
        adjacents = []
        if self.current[0] - 1 >= 0:
            adjacents.append((self.current[0] - 1, self.current[1]))
        if self.current[0] + 1 < self.max_y:
            adjacents.append((self.current[0] + 1, self.current[1]))
        if self.current[1] - 1 >= 0:
            adjacents.append((self.current[0], self.current[1] - 1))
        if self.current[1] + 1 < self.max_x:
            adjacents.append((self.current[0], self.current[1] + 1))

        return adjacents

    def get_valid_adjacent_points(self) -> list[tuple]:
        adjacents = self.up_down_left_right_from_current()
        unvisited_adjacents = [adjacent for adjacent in adjacents if adjacent not in self.visited_nodes]
        filtered_adjacents = []
        for point in unvisited_adjacents:
            if len(self.unvisited_nodes[self.current][1]) < 3:
                filtered_adjacents.append(point)
            else:
                pys = [py[0] for py in self.unvisited_nodes[self.current][1][-3:]]
                four_y_in_a_row = all([pt == point[0] for pt in pys])
                pxs = [px[1] for px in self.unvisited_nodes[self.current][1][-3:]]
                four_x_in_a_row = all([pt == point[1] for pt in pxs])
                # print(f'Previous 3 steps of {self.current} = {pys} ({four_y_in_a_row}), {pxs} ({four_x_in_a_row})')
                if not four_y_in_a_row and not four_x_in_a_row:
                    # print(f'Previous 3 steps of {self.current} = {pys} ({four_y_in_a_row}), {pxs} ({four_x_in_a_row})')
                    filtered_adjacents.append(point)
                else:
                    print(f'not considering {point} - too many consecutive steps in the same direction')

        return filtered_adjacents

    def get_min_unvisited(self) -> tuple:
        min_next = math.inf
        min_node = None
        for node in self.unvisited_nodes:
            if self.unvisited_nodes[node][0] < min_next:
                min_node = node
                min_next = self.unvisited_nodes[node][0]
        return min_node

    def solve(self):
        self.initialize()

        while True:
            adjacents = self.get_valid_adjacent_points()

            # print(f'{self.current}={self.unvisited_nodes[self.current][0]} is adjacent to {adjacents}')

            for point in adjacents:
                # print(f'  evaluating {point}={self.heatmap[point[0]][point[1]]}')
                new_weight = self.unvisited_nodes[self.current][0] + self.heatmap[point[0]][point[1]]
                if new_weight < self.unvisited_nodes[point][0]:
                    self.unvisited_nodes[point][0] = new_weight
                    self.unvisited_nodes[point][1] = self.unvisited_nodes[self.current][1] + [self.current]

            self.visited_nodes[self.current] = self.unvisited_nodes[self.current]
            del self.unvisited_nodes[self.current]

            self.current = self.get_min_unvisited()
            # print(f'Path to {self.current} is {self.unvisited_nodes[self.current][1]}')

            if self.current == self.end:
                print(f'Path from {self.start} to {self.end} loses {self.unvisited_nodes[self.current][0]} heat')
                pprint.pprint(self.unvisited_nodes[self.current][1])
                return self.unvisited_nodes[self.current][0]


if __name__ == '__main__':
    h = HeatMap(input_filename)
    print(h.solve())
