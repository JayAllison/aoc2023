from collections import defaultdict

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


# generate the same format/style output as the example, to make comparison easier
def display_boxes(boxes: dict, step) -> None:
    print(f'After "{step}":')
    for box in boxes:
        if boxes[box]:
            print(f'Box {box}: ', end='')
            for lns in boxes[box]:
                print(f'[{lns} {boxes[box][lns]}] ', end='')
            print()
    print()


# the hashing algorithm from part 1
def hash_it(step: str) -> int:
    the_hash = 0
    for c in step:
        the_hash += ord(c)
        the_hash *= 17
        the_hash %= 256
    return the_hash


# each step in the initialization sequence contains a lens label plus an operation
# the operation affects the box number identified by the HASH of lens label
# if operator is '-':
#   remove specified lens from box, if present (and move other lenses forward)
# if operator is '=':
#   step includes focal length of lens that needs to go into box
#   if lens label is already in box, replace with new focal length, in that same position
#   otherwise, add lens and focal length to end
#
# focusing power of each lens is (box number + 1) * one-based slot number of lens * lens focal length
# focusing power of system is sum of lens focusing powers


def execute_initialization_sequence(filename: str) -> dict:
    sequence = open(filename).readline().rstrip().split(',')  # there is only one line in the input file

    # a dictionary to look up a box's contents by the box number; using defaultdict to start with all empty boxes
    # the value will be another dictionary, mapping lens label to focal length, in order of insertion
    boxes = defaultdict(dict)

    for step in sequence:
        if '-' in step:
            label = step.rstrip('-')
            box = hash_it(label)
            if label in boxes[box]:
                del boxes[box][label]
        elif '=' in step:
            label, focal = step.split('=')
            box = hash_it(label)
            boxes[box][label] = int(focal)  # this only works in Python 3 because dicts now maintain insertion order
        # display_boxes(boxes, step)
    return boxes


def calculate_focusing_power(boxes: dict) -> int:
    focusing_power = 0
    for box in boxes:
        if boxes[box]:
            slot = 1  # focusing power of slot is one-based, not zero-based
            for lens in boxes[box]:
                lens_power = (box + 1) * slot * boxes[box][lens]
                # print(f'{box + 1} * {slot} * {boxes[box][lens]} = {lens_power}')
                slot += 1
                focusing_power += lens_power

    return focusing_power


def configure_lenses(filename: str) -> int:
    boxes = execute_initialization_sequence(filename)
    return calculate_focusing_power(boxes)


if __name__ == '__main__':
    print(configure_lenses(input_filename))
