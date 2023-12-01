import re

# input_filename = 'sample_data'
input_filename = 'input.txt'

# use a regular expression to find a single digit in the string
digit_regex = re.compile(r'\d')

the_sum = 0

for line in open(input_filename):
    # using findall() gives us a list[] of all of the matches back,
    # so that we can then easily ask for the first one and the last one
    digits = digit_regex.findall(line)
    number_string = digits[0] + digits[-1]
    the_sum += int(number_string)

print(the_sum)
