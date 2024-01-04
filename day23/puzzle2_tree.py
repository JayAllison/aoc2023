import datetime
import sys

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

# Python's default recursion limit of 1,000 is not sufficient for this puzzle
sys.setrecursionlimit(10_000)

start = datetime.datetime.now()


class Node:

    parent: 'Node'  # using forward reference type hints
    coord: tuple[int, int]
    children: list['Node']

    def __init__(self, parent: 'Node', coord: tuple[int, int]):
        self.parent = parent
        self.coord = coord
        self.children = []

    def depth(self) -> int:
        count = 1
        current = self
        while current.parent:
            count += 1
            current = current.parent
        return count

    def is_in_path(self, coord: tuple[int, int]) -> bool:
        current = self
        while current:
            if current.coord == coord:
                return True
            current = current.parent
        return False

    # def prune(self, child):
    #     self.children.remove(child)


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

    def get_valid_adjacent_steps(self, loc: tuple) -> list[tuple[int, int]]:
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

    def expand(self, node: Node, lengths: list[int]) -> None:
        if node.coord[0] == self.end_y:
            length = node.depth() - 1  # don't count the starting point in the path length
            lengths.append(length)  # path is complete, save path length
            print(f'{datetime.datetime.now() - start} Path {len(lengths)}: reached end after {length} steps - max is {max(lengths)}')
        else:
            # for each valid adjacent step that is not reversing our current path, move forward
            for next_step in self.get_valid_adjacent_steps(node.coord):
                if not node.is_in_path(next_step):
                    new_node = Node(node, next_step)
                    node.children.append(new_node)
                    self.expand(new_node, lengths)

    def hike(self) -> int:
        sy: int = 0
        sx: int = self.trail_map[sy].index('.')

        path_tree = Node(None, (sy, sx))
        lengths: list[int] = []

        self.expand(path_tree, lengths)

        return max(lengths)


if __name__ == '__main__':
    print(Hiker(input_filename).hike())
