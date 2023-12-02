from dataclasses import dataclass, field
from pprint import pprint

@dataclass
class Game:
    ID: int
    red: list[int] = field(default_factory=list)
    blue: list[int] = field(default_factory=list)
    green: list[int] = field(default_factory=list)


red_limit = 12
green_limit = 13
blue_limit = 14

# input_filename = 'sample_data'
input_filename = 'input.txt'

games = []

for line in open(input_filename):
    game_name, cubes_drawn = line.lstrip().rstrip().split(':')
    this_game = Game(int(game_name.lstrip().rstrip().split(' ')[1]))
    games.append(this_game)

    cube_sets = cubes_drawn.lstrip().rstrip().split(';')
    for cube_set in cube_sets:
        colors_and_counts = cube_set.lstrip().rstrip().split(',')
        for color_and_count in colors_and_counts:
            count, color = color_and_count.lstrip().rstrip().split(' ')
            match color:
                case 'red':
                    this_game.red.append(int(count))
                case 'green':
                    this_game.green.append(int(count))
                case 'blue':
                    this_game.blue.append(int(count))

possible_IDs = []

for game in games:
    good = True
    for red_count in game.red:
        if red_count > red_limit:
            good = False
    for green_count in game.green:
        if green_count > green_limit:
            good = False
    for blue_count in game.blue:
        if blue_count > blue_limit:
            good = False
    if good:
        possible_IDs.append(game.ID)

print(sum(possible_IDs))
