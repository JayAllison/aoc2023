import re

# input_filename = 'sample_data'
# input_filename = 'sample_data2'
input_filename: str = 'input.txt'

node_parser = re.compile(r'(\w+) = \((\w+), (\w+)\)')
with open(input_filename) as file:
    instructions = file.readline().rstrip()
    file.readline()
    node_groups = [node_parser.match(line).groups() for line in file.readlines()]
    nodes = {g[0]: (g[1], g[2]) for g in node_groups}

count = 0
next_step = 'AAA'
while True:
    direction = instructions[count % len(instructions)]
    # print(f'{count+1}: {direction} @ {next_step} -> ', end='')
    next_step = nodes[next_step][0] if direction == 'L' else nodes[next_step][1]
    # print(f'{next_step}')
    count += 1
    if count % 1000 == 0:
        print('.', end='', flush=True)
    if next_step == 'ZZZ':
        print()
        print(f'Total step requires to reach ZZZ = {count}')
        break
