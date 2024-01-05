from collections import deque
# from pprint import pprint

# input_filename: str = 'sample_data'; button_press_count = 1000
# input_filename: str = 'sample_data2'; button_press_count = 1000
input_filename: str = 'input.txt'; button_press_count = 1000

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
    modules[module_name] = [op, value, destinations]  # TODO: would making this a dataclass make cleaner code???


# conjunction module initial value needs a little bit more work - have to track all connected input sources
for module_name in modules:
    if modules[module_name][0] == '&':
        for input_module_name in modules:
            if module_name in modules[input_module_name][2]:
                modules[module_name][1][input_module_name] = 'low'

# pprint(modules)
# print()

# per the instructions, this cannot be handled recursively, it must be handled in a cascading style
low_count = 0
high_count = 0
for i in range(button_press_count):
    pulses = deque()
    pulses.append(['broadcaster', 'low', 'button'])

    # print()

    while pulses:
        module_name, pulse, source_module = pulses.popleft()
        # print(f'{source_module} -{pulse}-> {module_name}')

        if pulse == 'low':
            low_count += 1
        if pulse == 'high':
            high_count += 1

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

print(f'{low_count} * {high_count} = {low_count * high_count}')
