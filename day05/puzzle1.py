import re

# input_filename = 'sample_data'
input_filename = 'input.txt'


class AlmanacMap:

    lines: list[str] = None
    _ranges: list[list[int]] = None

    def __init__(self):
        self.lines = []

    def parse(self):
        self._ranges = [[int(i) for i in _line.split()] for _line in self.lines]

    def map(self, x: int) -> int:
        for _range in self._ranges:
            if _range[1] <= x < _range[1] + _range[2]:
                return _range[0] + (x - _range[1])
        return x


# we don't need to know which mapper is which, we just need to cascade sequentially (thanks, Francis!)
mappers: list[AlmanacMap] = []

# break up the input file into groups of lines that we can then parse
with open(input_filename) as file:
    seeds_line: str = file.readline().rstrip()

    while line := file.readline():
        line = line.rstrip()
        if not line:
            new_mapper: AlmanacMap = AlmanacMap()
            mappers.append(new_mapper)
        elif ':' not in line:
            new_mapper.lines.append(line)

# parse each group of lines
for mapper in mappers:
    mapper.parse()

seeds: list[int] = [int(i) for i in re.findall(r'\d+', seeds_line)]

# map each seed all the way through and store the result
locations: list[int] = []
for n in seeds:
    for mapper in mappers:
        n = mapper.map(n)
    locations.append(n)

# display the smallest result
print(min(locations))
