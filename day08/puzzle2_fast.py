import math
import re

# input_filename = 'sample_data3'
input_filename: str = 'input.txt'


# from https://stackoverflow.com/questions/15347174/python-finding-prime-factors - thanks, folks!
def find_prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


# parse the input into a sequence of turns, then a lookup table of directions
node_parser = re.compile(r'(\w+) = \((\w+), (\w+)\)')
with open(input_filename) as file:
    instructions = file.readline().rstrip()
    file.readline()
    node_groups = [node_parser.match(line).groups() for line in file.readlines()]
    nodes = {g[0]: (g[1], g[2]) for g in node_groups}

# Part 2 asks to start with every node ending in 'A' and then go to any node ending in 'Z'
next_steps = [node for node in nodes if node.endswith('A')]

# through experimentation, I've found that each 'A' goes to the same 'Z' and repeats the same number of steps each cycle
# ie, for my input: VCA gets to GLZ in 18113, then gets back to GLZ in another 18113, etc.
# So, there is a consistent, repeating length for each path - just need to find point where all of those paths converge

counts = []

# since we know each path repeats consistently, we only need to count the steps in the first pass down each path
# this is basically the same as Part 1, for each path
for next_step in next_steps:
    first_step = next_step
    count = 0
    while True:
        direction = instructions[count % len(instructions)]
        next_step = nodes[next_step][0] if direction == 'L' else nodes[next_step][1]
        count += 1
        if next_step.endswith('Z'):
            print(f'{first_step} to {next_step} in {count}')
            counts.append(count)
            break

# find the prime factors for each path
prime_factors = [find_prime_factors(c) for c in counts]

# use set to eliminate duplicates from the combined list of prime factors, so we end up with only one of each factor
common_factors = {f1 for f in prime_factors for f1 in f}

# multiply all of the non-duplicate prime factors together to find the first convergence point
print(f'The first convergence point for all {len(counts)} paths is {math.prod(list(common_factors)):,}')
