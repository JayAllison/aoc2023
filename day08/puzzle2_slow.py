import datetime
import re

# input_filename = 'sample_data3'
input_filename: str = 'input.txt'

node_parser = re.compile(r'(\w+) = \((\w+), (\w+)\)')
with open(input_filename) as file:
    instructions = file.readline().rstrip()
    file.readline()
    node_groups = [node_parser.match(line).groups() for line in file.readlines()]
    nodes = {g[0]: (g[1], g[2]) for g in node_groups}

little_feedback = 1_000_000
big_feedback = little_feedback * 100
count = 0
start = datetime.datetime.now()
print(f'{start} ', end='')
next_steps = [node for node in nodes if node.endswith('A')]
while True:
    direction = instructions[count % len(instructions)]
    next_steps = [nodes[next_step][0] if direction == 'L' else nodes[next_step][1] for next_step in next_steps]
    count += 1
    if count % big_feedback == 0:
        now = datetime.datetime.now()
        print(f'\n{now} ({now-start}) ', end='')
    elif count % (little_feedback * 10) == 0:
        print('+', end='', flush=True)
    elif count % little_feedback == 0:
        print('.', end='', flush=True)
    if all([next_step.endswith('Z') for next_step in next_steps]):
        print()
        print(f'Total steps requires to reach all **Z nodes = {count}')
        break
