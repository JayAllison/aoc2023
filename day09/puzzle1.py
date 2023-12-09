# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

# read in each line, split it into digit strings, then convert each string to an int, and store as a list of ints
histories: list[list[int]] = [[int(i) for i in line.split()] for line in open(input_filename).readlines()]

# predict each history list that we were given
for history in histories:
    deltas: list[list[int]] = [history]
    current_delta: list[int] = deltas[0]

    # find the deltas for each stage of the process, until the deltas for the entire stage are all zero
    while True:
        next_delta: list[int] = []
        deltas.append(next_delta)
        for i in range(1, len(current_delta), 1):
            next_delta.append(current_delta[i] - current_delta[i-1])
        current_delta = next_delta
        if not any(next_delta):
            break

    # predict the next value at each stage, until we have a prediction for the original history
    deltas[-1].append(0)
    for di in range(len(deltas) - 2, 0, -1):
        deltas[di - 1].append(deltas[di - 1][-1] + deltas[di][-1])

# sum up the new predicted values from each history
print(sum([h[-1] for h in histories]))
