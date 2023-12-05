from collections import deque
import datetime
import pprint
import re

# input_filename = 'sample_data'
input_filename = 'input.txt'


class AlmanacMap:

    ranges: list[list[int]] = None  # how could I initialize this to a unique empty list?

    def __init__(self, lines_to_parse):
        # pprint.pprint(self.ranges)
        self.parse(lines_to_parse)

    def parse(self, lines):
        self.ranges = [[int(i) for i in _line.split()] for _line in lines]
        # pprint.pprint(self.ranges)

    def map(self, x: int) -> int:
        for _range in self.ranges:
            if _range[1] <= x < _range[1] + _range[2]:
                return _range[0] + (x - _range[1])
        return x


ss_lines: list[str] = []
sf_lines: list[str] = []
fw_lines: list[str] = []
wl_lines: list[str] = []
lt_lines: list[str] = []
th_lines: list[str] = []
hl_lines: list[str] = []

# parse the input file
with open(input_filename) as file:
    seeds_line = file.readline().rstrip()

    ss = False
    sf = False
    fw = False
    wl = False
    lt = False
    th = False
    hl = False

    while line := file.readline():
        line = line.rstrip()
        match line:
            case '':
                ss = False
                sf = False
                fw = False
                wl = False
                lt = False
                th = False
                hl = False
                continue
            case 'seed-to-soil map:':
                ss = True
                continue
            case 'soil-to-fertilizer map:':
                sf = True
            case 'fertilizer-to-water map:':
                fw = True
            case 'water-to-light map:':
                wl = True
            case 'light-to-temperature map:':
                lt = True
            case 'temperature-to-humidity map:':
                th = True
            case 'humidity-to-location map:':
                hl = True
            case _:
                if ss:
                    ss_lines.append(line)
                elif sf:
                    sf_lines.append(line)
                elif fw:
                    fw_lines.append(line)
                elif wl:
                    wl_lines.append(line)
                elif lt:
                    lt_lines.append(line)
                elif th:
                    th_lines.append(line)
                elif hl:
                    hl_lines.append(line)

seeds: deque[int] = deque([int(i) for i in re.findall(r'\d+', seeds_line)])
seed_to_soil = AlmanacMap(ss_lines)
soil_to_fertilizer = AlmanacMap(sf_lines)
fertilizer_to_water = AlmanacMap(fw_lines)
water_to_light = AlmanacMap(wl_lines)
light_to_temperature = AlmanacMap(lt_lines)
temperature_to_humidity = AlmanacMap(th_lines)
humidity_to_location = AlmanacMap(hl_lines)

min_location = None
# patterns I've looked for - does it repeat? No.
while seeds:
    seed_start = seeds.popleft()
    seed_range = seeds.popleft()
    print(f'{datetime.datetime.now()} Checking {seed_start} + {seed_range}...')
    count = 0
    for seed in range(seed_start, seed_start+seed_range+1, 1):
        count += 1
        soil = seed_to_soil.map(seed)
        fert = soil_to_fertilizer.map(soil)
        water = fertilizer_to_water.map(fert)
        light = water_to_light.map(water)
        temp = light_to_temperature.map(light)
        hum = temperature_to_humidity.map(temp)
        loc = humidity_to_location.map(hum)
        if min_location is None:
            min_location = loc
            print(min_location)
        elif loc < min_location:
            min_location = loc
            print(min_location)

print(min_location)
