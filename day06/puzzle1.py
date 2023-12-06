import re

# input_filename = 'sample_data'
input_filename = 'input.txt'

with open(input_filename) as file:
    time_line = file.readline().rstrip().replace(' ', '')
    distance_line = file.readline().rstrip().replace(' ', '')

number_parser = re.compile(r'\d+')
times = [int(t) for t in number_parser.findall(time_line)]
distances = [int(d) for d in number_parser.findall(distance_line)]

ways = 1
for i in range(len(times)):
    count = 0
    for hold_time in range(times[i]):
        go_time = times[i] - hold_time
        go_distance = go_time * hold_time
        if go_distance > distances[i]:
            count += 1
    ways *= count

print(ways)
