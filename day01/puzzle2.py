import re

# input_filename = 'sample_data2'
input_filename = 'input.txt'

# use a regular expression to find all single digits in the string by number and *most* single digits by name
# ex: searching forward, this will find 'eight' but not 'two' in eightwo
#     searching in reverse, this will find 'two' but not 'eight' in eightwo
# that's not perfect, but it's good enough for this solution, because we don't need very digit, just first & last
digit_regex_forward = re.compile(r'\d|one|two|three|four|five|six|seven|eight|nine')
digit_regex_reverse = re.compile(r'\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin')

# map the digit by name (forward or backward) or by digit string to the digit string
conversion = {
    '1': '1',
    'one': '1',
    'eno': '1',
    '2': '2',
    'two': '2',
    'owt': '2',
    '3': '3',
    'three': '3',
    'eerht': '3',
    '4': '4',
    'four': '4',
    'ruof': '4',
    '5': '5',
    'five': '5',
    'evif': '5',
    '6': '6',
    'six': '6',
    'xis': '6',
    '7': '7',
    'seven': '7',
    'neves': '7',
    '8': '8',
    'eight': '8',
    'thgie': '8',
    '9': '9',
    'nine': '9',
    'enin': '9',
}

the_sum = 0

for line in open(input_filename):
    # use regex to search the string for the first digit, either the number or the name
    first_digit = digit_regex_forward.search(line)[0]
    # use regex search the reversed string for the last digit, either the number or the name
    last_digit = digit_regex_reverse.search(line[::-1])[0]
    number_string = conversion[first_digit] + conversion[last_digit]
    the_sum += int(number_string)

print(the_sum)
