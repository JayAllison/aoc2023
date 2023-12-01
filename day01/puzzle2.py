import re

# input_filename = 'sample_data2'
input_filename = 'input.txt'

digit_regex_forward = re.compile(r'\d|one|two|three|four|five|six|seven|eight|nine')
digit_regex_reverse = re.compile(r'\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin')

the_sum = 0

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

for line in open(input_filename):
    # print(line)
    forward_digits = digit_regex_forward.findall(line)
    reverse_digits = digit_regex_reverse.findall(line[::-1])
    digit_string = conversion[forward_digits[0]] + conversion[reverse_digits[0]]
    print(digit_string)
    the_sum += int(digit_string)

print(the_sum)
