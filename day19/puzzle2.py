from dataclasses import dataclass
from pprint import pprint
import re
from typing import Union

input_filename: str = 'sample_data'
# input_filename: str = 'input.txt'

MAX_RATING = 4000

test_parser = re.compile(r'(\w)([<>])(\w+):(\w+)')


@dataclass
class Rule:
    destination_name: str
    category: str | None
    operator: str | None
    value: int | None


@dataclass
class Connection:

    category: str | None
    operator: str | None
    value: int | None
    destination_name: str
    destination: 'Node'


class Node:

    name: str
    parent: 'Node'
    children: dict[str: Connection]  # Python 3: all dicts are ordered by insertion

    # can't use the new '|' type operator when using forward references :(
    def __init__(self, name: str, parent: Union['Node', None]):
        self.name = name
        self.parent = parent
        self.children = {}


def parse_workflows(rules: str) -> list[Rule]:
    parsed_rules = []
    rules_list = rules.split(',')
    for rule in rules_list:
        if ':' in rule:
            category, test, value, destination = test_parser.match(rule).groups()
            parsed_rules.append(Rule(destination, category, test, int(value)))
        else:
            parsed_rules.append(Rule(rule, None, None, None))
    return parsed_rules


def parse_input(filename: str) -> dict:
    halves = open(filename).read().split('\n\n')
    workflow_lines = halves[0].split('\n')  # for Part 2, we are only interested in the rules and can ignore the parts
    workflows_pieces = [line.rstrip('}').split('{') for line in workflow_lines]
    workflows = {pieces[0]: parse_workflows(pieces[1]) for pieces in workflows_pieces}
    return workflows


def calculate_combinations(node: Node) -> int:
    stack = []
    filters = {'x': [], 'm': [], 'a': [], 's': []}

    current_node: Node = node
    while current_node:
        explanation = f' -> {current_node.name}'
        if current_node.parent:
            conn: Connection = current_node.parent.children[current_node.name]
            explanation = f'{conn.category} {conn.operator} {conn.value}' + explanation
            if conn.category:
                filters[conn.category].append([conn.operator, conn.value])
                # TODO: add inverse of previous branch's rules, so we don't double-count
        else:
            explanation = 'START' + explanation
        stack.append(explanation)
        current_node = current_node.parent

    # while stack:
    #     print(stack.pop())
    # print()
    # pprint(filters)
    # print()

    product = 1
    for category in filters:
        accepted = [1 for _i in range(MAX_RATING + 1)]
        accepted[0] = 0
        for operator, value in filters[category]:
            if operator == '<':
                for i in range(value, MAX_RATING + 1, 1):
                    accepted[i] = 0
            elif operator == '>':
                for i in range(1, value + 1, 1):
                    accepted[i] = 0
        count = sum(accepted)
        product *= count

    return product


def build_node(rule: Rule, parent: Node, workflows: dict) -> int | None:
    node: Node = Node(rule.destination_name, parent)
    conn: Connection = Connection(rule.category, rule.operator, rule.value, rule.destination_name, node)
    parent.children[rule.destination_name] = conn

    combinations = 0
    if node.name == 'R':
        pass
    elif node.name == 'A':
        combinations += calculate_combinations(node)
    else:
        for rule in workflows[node.name]:
            combinations += build_node(rule, node, workflows)

    return combinations


def build_tree(workflows: dict) -> int:
    root_node: Node = Node('in', None)
    combinations = 0
    for rule in workflows[root_node.name]:
        combinations += build_node(rule, root_node, workflows)

    return combinations


def solve(filename: str) -> int:
    workflows: dict[str, list[Rule]] = parse_input(filename)
    # pprint(workflows)
    return build_tree(workflows)


if __name__ == '__main__':
    print(solve(input_filename))
