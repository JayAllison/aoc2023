import re

# input_filename = 'sample_data'
input_filename = 'input.txt'

number_parser = re.compile(r'\d+')
with open(input_filename) as file:
    times = [int(t) for t in number_parser.findall(file.readline().rstrip())]
    distances = [int(d) for d in number_parser.findall(file.readline().rstrip())]

ways = 1
for i in range(len(times)):
    count = 0
    for hold_time in range(times[i]):
        if (times[i] - hold_time) * hold_time > distances[i]:
            count += 1
    ways *= count

print(ways)
