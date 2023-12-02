from dataclasses import dataclass
import re


@dataclass
class Game:
    ID: int
    max_red: int = 0
    max_blue: int = 0
    max_green: int = 0


RED_LIMIT = 12
GREEN_LIMIT = 13
BLUE_LIMIT = 14

# input_filename = 'sample_data'
input_filename = 'input.txt'

games = []

# example line to parse: `Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red`
full_line_regex = re.compile(r'Game (\d*):(.*)$')
color_count_regex = re.compile(r'(\d+) (red|green|blue)')

for line in open(input_filename):
    game_id, cubes_drawn = full_line_regex.match(line).groups()
    this_game = Game(int(game_id))
    games.append(this_game)

    for cube_set in cubes_drawn.lstrip().rstrip().split(';'):
        for count, color in color_count_regex.findall(cube_set):
            match color:
                case 'red':
                    this_game.max_red = max(int(count), this_game.max_red)
                case 'green':
                    this_game.max_green = max(int(count), this_game.max_green)
                case 'blue':
                    this_game.max_blue = max(int(count), this_game.max_blue)

# Puzzle 1 calculation - is everything under the MAX?
possible_IDs = [g.ID for g in games if (g.max_red <= RED_LIMIT and g.max_green <= GREEN_LIMIT and g.max_blue <= BLUE_LIMIT)]
print(sum(possible_IDs))
