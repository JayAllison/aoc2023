from dataclasses import dataclass, field
from pprint import pprint

@dataclass
class Game:
    ID: int
    max_red: int = 0
    max_blue: int = 0
    max_green: int = 0


# input_filename = 'sample_data'
input_filename = 'input.txt'

games = []

# example line to parse: `Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red`
#   split on the colon --------|
#   then split on the space --|
#   then split on the semi-colons ----------------------|------------------------|
#   then split on the spaces, then compare the color words
#   before each split, strip any leading and trailing whitespace
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
                    this_game.max_red = max(int(count), this_game.max_red)
                case 'green':
                    this_game.max_green = max(int(count), this_game.max_green)
                case 'blue':
                    this_game.max_blue = max(int(count), this_game.max_blue)

powers = []

for game in games:
    power = game.max_red * game.max_green * game.max_blue
    powers.append(power)

print(sum(powers))
