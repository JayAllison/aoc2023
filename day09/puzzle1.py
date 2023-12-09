import pprint

# input_filename = 'sample_data'
input_filename: str = 'input.txt'

histories: list[list[int]] = [[int(i) for i in line.split()] for line in open(input_filename).readlines()]

# evaluate each history list that we were given
for history in histories:
    deltas: list[list[int]] = [history]
    di = 0

    # find the deltas for each stage of the process, until the deltas for the entire stage are all zero
    while True:
        next_delta: list[int] = []
        deltas.append(next_delta)
        for i in range(1, len(deltas[di]), 1):
            next_delta.append(deltas[di][i] - deltas[di][i-1])
        di += 1
        if not any(next_delta):
            break

    # working backwards, predict the next value at each stage, until we have a projection for the original history
    deltas[-1].append(0)
    for si in range(len(deltas)-2, 0, -1):
        deltas[si-1].append(deltas[si-1][-1] + deltas[si][-1])

# sum up the new predicted value on each history
print(sum([h[-1] for h in histories]))
