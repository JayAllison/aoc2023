from dataclasses import dataclass
from collections import deque
# from pprint import pprint

# input_filename: str = 'sample_data'; button_press_count = 1
# input_filename: str = 'sample_data2'; button_press_count = 1000
input_filename: str = 'input.txt'; button_press_count = 1000

# define our constants for this puzzle
FLIP_FLOP = '%'
CONJUNCTION = '&'

OFF = 'off'
ON = 'on'

HIGH = 'high'
LOW = 'low'


@dataclass
# -------------------------------------------------------------------------------------------------
# this dataclass represents a pulse, from one module to another:  source --level--> destination
# -------------------------------------------------------------------------------------------------
class Pulse:

    source: str
    level: str
    destination: str

    def __str__(self):
        # represent the pulse in the same text format as the examples
        return f'{self.source} -{self.level}-> {self.destination}'


# -------------------------------------------------------------------------------------------------
# this is the Module base/parent class and will also represent the simplistic broadcaster module
# -------------------------------------------------------------------------------------------------
class Module:

    destinations: list[str]

    _name: str
    _type: str
    _current_value: str | dict = None

    def __init__(self, name: str, module_type: str, destinations: list[str]):
        self._name = name
        self._type = module_type
        self.destinations = destinations

    def add_source(self, source_module_name) -> None:
        pass  # most modules don't care about tracking this...

    def _send_pulses(self, level: str) -> list[Pulse]:
        next_pulses = []

        for destination in self.destinations:
            next_pulses.append(Pulse(self._name, level, destination))

        return next_pulses

    def process_pulse(self, pulse: str, source_module: str) -> list[Pulse]:
        return self._send_pulses(pulse)  # the broadcaster just passes along the input pulse to the destination(s)


# -------------------------------------------------------------------------------------------------
# this derived/child class represents the flip-flop module
# -------------------------------------------------------------------------------------------------
class FlipFlopModule(Module):

    def __init__(self, name: str, module_type: str, destinations: list[str]):
        super().__init__(name, module_type, destinations)
        self._current_value = OFF

    def process_pulse(self, pulse: str, source_module: str) -> list:
        next_pulse = None

        if pulse == LOW:
            if self._current_value == OFF:
                self._current_value = ON
                next_pulse = HIGH
            elif self._current_value == ON:
                self._current_value = OFF
                next_pulse = LOW
            else:
                print(f'this should not happen: {self._name} {self._current_value=}')
        elif pulse == HIGH:
            pass
        else:
            print(f'this should not happen: {self._name} {pulse=}')

        next_pulses = []
        if next_pulse:
            next_pulses = self._send_pulses(next_pulse)

        return next_pulses


# -------------------------------------------------------------------------------------------------
# this derived/child class represents the conjunction module
# -------------------------------------------------------------------------------------------------
class ConjunctionModule(Module):

    def __init__(self, name: str, module_type: str, destinations: list[str]):
        super().__init__(name, module_type, destinations)
        self._current_value = {}

    def add_source(self, source_module_name) -> None:
        self._current_value[source_module_name] = LOW

    def process_pulse(self, pulse: str, source_module: str) -> list:
        self._current_value[source_module] = pulse
        if all([inp == HIGH for inp in self._current_value.values()]):
            next_pulse = LOW
        else:
            next_pulse = HIGH

        return self._send_pulses(next_pulse)


# -------------------------------------------------------------------------------------------------
# use the Abstract Factory Pattern to create the various Module types
# -------------------------------------------------------------------------------------------------
def module_factory(name: str, module_type: str, destinations: list[str]) -> Module:
    if module_type == FLIP_FLOP:
        return FlipFlopModule(name, module_type, destinations)
    elif module_type == CONJUNCTION:
        return ConjunctionModule(name, module_type, destinations)
    else:
        return Module(name, module_type, destinations)


def parse_input_into_modules(filename: str) -> dict[str: Module]:
    mappings = [line.rstrip().split(' -> ') for line in open(filename)]
    modules = {}

    # break down the module name, module operation, and module destination(s) for each module
    for entry in mappings:
        ops = FLIP_FLOP + CONJUNCTION
        op = None
        module_name = entry[0]
        if entry[0][0] in ops:
            op = entry[0][0]
            module_name = entry[0][1:]
        destinations = entry[1].split(', ')
        modules[module_name] = module_factory(module_name, op, destinations)  # ask the factory for the proper module

    # let each module know which other modules are sending pulses to it
    for module_name in modules:
        for input_module_name in modules:
            if module_name in modules[input_module_name].destinations:
                modules[module_name].add_source(input_module_name)

    return modules


def solve(filename: str, press_count: int) -> int:
    modules = parse_input_into_modules(filename)

    low_count = 0
    high_count = 0

    # per the instructions, this cannot be handled recursively; it must be handled in a cascading style
    for i in range(press_count):
        first_pulse = Pulse('button', LOW, 'broadcaster')  # pushing the button sends a low pulse to the broadcaster
        pulses = deque([first_pulse])  # using a queue for efficient pop'ing

        while pulses:
            pulse = pulses.popleft()
            # print(pulse)

            if pulse.level == LOW:
                low_count += 1
            if pulse.level == HIGH:
                high_count += 1

            # although not explicitly called out in the instructions, this is not an error, as shown in the 2nd example
            if pulse.destination not in modules:
                continue

            resulting_pulses = modules[pulse.destination].process_pulse(pulse.level, pulse.source)
            pulses.extend(resulting_pulses)

    # print(f'{low_count} * {high_count} = {low_count * high_count}')
    return low_count * high_count


if __name__ == '__main__':
    print(solve(input_filename, button_press_count))
