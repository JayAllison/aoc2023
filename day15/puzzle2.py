from collections import defaultdict
# import pprint

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


def display_boxes(bxs: dict) -> None:
    for bx in bxs:
        print(f'{bx}: ', end='')
        for lns in bxs[bx]:
            print(f'[{lns} {boxes[bx][lns]}] ', end='')
        print()


def hash_it(stp: str) -> int:
    the_hash = 0
    for c in stp:
        the_hash += ord(c)
        the_hash *= 17
        the_hash %= 256
    return the_hash


steps = open(input_filename).readline().rstrip().split(',')

# start with empty boxes
boxes = defaultdict(dict)

# step is lens label plux operation
# box number is hash of lens label
# if operator is '-' remove lens from box (move other lenses forward)
# if operator is '=' then step includes focal length of lens that needs to go into box
# if lens label is already in box, replace with new focal length
# otherwise, lens add to end
# focusing power of each box is (box number + 1) * slot number of lens * lens focal length

for step in steps:
    if '-' in step:
        label = step.rstrip('-')
        box = hash_it(label)
        if label in boxes[box]:
            del boxes[box][label]
    elif '=' in step:
        label, focal = step.split('=')
        box = hash_it(label)
        boxes[box][label] = int(focal)  # this only works in Python 3 because dicts now maintain insertion order
    else:
        print(f'unknown operation {step}')
    # print(f'{step}')
    # display_boxes(boxes)

focusing_power = 0
for box in boxes:
    if boxes[box]:
        slot = 1
        lens_power = 0
        for lens in boxes[box]:
            lens_power = (box + 1) * slot * boxes[box][lens]
            # print(f'{box + 1} * {slot} * {boxes[box][lens]} = {lens_power}')
            slot += 1
            focusing_power += lens_power

print(focusing_power)
