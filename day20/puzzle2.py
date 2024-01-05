from collections import deque
# from pprint import pprint
from math import prod

input_filename: str = 'input.txt'

mappings = [line.rstrip().split(' -> ') for line in open(input_filename)]
modules = {}

# break down the module name, module operation, module destination(s), and initial value for each module
for entry in mappings:
    ops = '%&'
    op = None
    module_name = entry[0]
    if entry[0][0] in ops:
        op = entry[0][0]
        module_name = entry[0][1:]
    destinations = entry[1].split(', ')
    value = 'off' if op == '%' else {} if op == '&' else None
    modules[module_name] = [op, value, destinations]


# conjunction module initial value needs a little bit more work - have to track all connected input sources
for module_name in modules:
    if modules[module_name][0] == '&':
        for input_module_name in modules:
            if module_name in modules[input_module_name][2]:
                modules[module_name][1][input_module_name] = 'low'

# pprint(modules)
# print()

# determine what controls the input to rx - the puzzle takes forever to actually get a low signal to rx,
# but fortunately we only have to go back one set of modules to quickly see a repeating pattern of inputs
rx_driver = None  # which module drives rx (it turns out that there is only one, and it's a conjunction)
upstream = None  # which modules drive this conjunction - once they're all high, the conjunction will drive rx low
for module_name in modules:
    if 'rx' in modules[module_name][2]:
        rx_driver = module_name
        print(f'"rx" is driven by "{rx_driver}"')
        print(f'"{rx_driver}" type is "{modules[rx_driver][0]}"')
        upstream = list(modules[rx_driver][1].keys())
        print(f'"{rx_driver}" inputs are {upstream}')

multiples = {module_name: 0 for module_name in upstream}
confirmed = True
run_length = 100_000

# per the instructions, this cannot be handled recursively, it must be handled in a cascading style
for button_presses in range(1, run_length + 1, 1):
    pulses = deque()
    pulses.append(['broadcaster', 'low', 'button'])

    while pulses:
        module_name, pulse, source_module = pulses.popleft()
        # print(f'{source_module} -{pulse}-> {module_name}')

        # try to figure out the pattern that will be required upstream to trigger jm to send low to rx
        if module_name == rx_driver and pulse == 'high':
            if multiples[source_module] == 0:
                # store off the cycle for this input
                multiples[source_module] = button_presses
                print(f' - {source_module} high to {module_name} after {multiples[source_module]}')
            else:
                # confirm that the cycle is consistent
                if button_presses % multiples[source_module] != 0:
                    print(f'!! {source_module} high to {module_name} after {button_presses}, not a multiple!')
                    confirmed = False

        if module_name == 'rx':  # this will not happen for a very, very, very long time...
            if pulse == 'low':
                print(button_presses)
                exit()

        # although not explicitly called out in the instructions, this is not an error, as shown in the 2nd example
        if module_name not in modules:
            # print(f'  !! no module named {module_name} !!')
            continue

        module = modules[module_name]
        op = module[0]
        value = module[1]
        destinations = module[2]

        cascade: bool = True

        if op == '%':
            if pulse == 'low':
                if value == 'off':
                    module[1] = 'on'
                    next_pulse = 'high'
                elif value == 'on':
                    module[1] = 'off'
                    next_pulse = 'low'
                else:
                    print(f'this should not happen: {value=}')
            elif pulse == 'high':
                cascade = False
            else:
                print(f'this should not happen: {pulse=}')

        elif op == '&':
            # print(f'    & {module_name}')
            value[source_module] = pulse
            if all([inp == 'high' for inp in value.values()]):
                next_pulse = 'low'
            else:
                next_pulse = 'high'

        else:
            next_pulse = pulse

        if cascade:
            for destination in destinations:
                # print(f'  queueing {module_name}->{next_pulse}->{destination}')
                pulses.append([destination, next_pulse, module_name])

if confirmed:
    print(f'Multiples confirmed after {run_length} button presses.')

# it turned out that all of the repeating values were prime numbers already,
# so you get the LCM simply by multiplying them all together
print(prod(multiples.values()))
