import re

# input_filename = 'sample_data'
input_filename = 'input.txt'

digit_regex = re.compile(r'\d')

sum = 0

for line in open(input_filename):
    digits = digit_regex.findall(line)
    digit_string = digits[0] + digits[-1]
    sum += int(digit_string)

print(sum)
