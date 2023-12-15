# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'


def hash_it(step: str) -> int:
    the_hash = 0
    for c in step:
        the_hash += ord(c)
        the_hash *= 17
        the_hash %= 256
    return the_hash


steps = open(input_filename).readline().rstrip().split(',')
print(steps)
hashes = [hash_it(step) for step in steps]
print(hashes)
print(sum(hashes))
