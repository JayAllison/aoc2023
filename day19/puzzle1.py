import pprint
import re

# input_filename: str = 'sample_data'
input_filename: str = 'input.txt'

test_parser = re.compile(r'(\w)([<>])(\w+):(\w+)')


def parse_workflow(rules: str) -> list:
    parsed_rules = []
    rules_list = rules.split(',')
    for rule in rules_list:
        if ':' in rule:
            category, test, value, destination = test_parser.match(rule).groups()
            parsed_rules.append([category, test, int(value), destination])
        else:
            parsed_rules.append(rule)
    return parsed_rules


def parse_input(filename: str) -> tuple[dict, list]:
    halves = open(filename).read().split('\n\n')
    workflow_lines = halves[0].split('\n')
    parts_lines = halves[1].rstrip().split('\n')

    workflows_pieces = [line.rstrip('}').split('{') for line in workflow_lines]
    workflows = {pieces[0]: parse_workflow(pieces[1]) for pieces in workflows_pieces}

    parts = [{c.split('=')[0]: int(c.split('=')[1]) for c in l.lstrip('{').rstrip('}').split(',')} for l in parts_lines]

    return workflows, parts


def evaluate(part: list, workflows: dict) -> str:
    start = 'in'
    # print(f'{start} -> ', end='')
    workflow = workflows[start]

    while True:
        for step in workflow:
            if isinstance(step, str):
                if step == 'A' or step == 'R':
                    # print(f'{step}')
                    return step
                else:
                    # print(f'{step} -> ', end='')
                    workflow = workflows[step]
                    break
            else:
                category, test, value, destination = step
                if test == '<':
                    if part[category] < value:
                        # print(f'{destination} -> ', end='')
                        if destination == 'A' or destination == 'R':
                            # print(f'{destination}')
                            return destination
                        workflow = workflows[destination]
                        break
                elif test == '>':
                    if part[category] > value:
                        # print(f'{destination} -> ', end='')
                        if destination == 'A' or destination == 'R':
                            # print(f'{destination}')
                            return destination
                        workflow = workflows[destination]
                        break
                else:
                    print(f'this should not happen: {test}')


def solve(filename: str) -> int:
    workflows, parts = parse_input(filename)

    accepted_parts = []
    for part in parts:
        conclusion = evaluate(part, workflows)
        if conclusion == 'A':
            # print(f'{conclusion} -> accepted!')
            accepted_parts.append(part)
        # else:
        #     print(f'{conclusion} -> rejected!')

    pprint.pprint(accepted_parts)
    score = sum([sum(part.values()) for part in accepted_parts])
    return score


if __name__ == '__main__':
    print(solve(input_filename))
