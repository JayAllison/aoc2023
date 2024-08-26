"use strict";

const fs = require('fs');

// this works for Objects but not for Classes
function pretty_print_object(s) {
    console.log(JSON.stringify(s, undefined, 2));
}

// must use full path when executing node in vscode, because vscode does not start node in the script's directory...
// const filename = '/home/jay/source/aoc2023/day10/sample1.txt';
// const filename = '/home/jay/source/aoc2023/day10/sample2.txt';
const filename = '/home/jay/source/aoc2023/day10/input.txt';

let lines = fs.readFileSync(filename, 'utf-8').split(/\r?\n/).filter(l => l.length > 0);

// a two-dimensional array [y, x] of the pipe map
const pipe_map = lines.map(l => [...l]);

function get_next_step(y, x, direction) {
    // console.log(`  Going ${direction} from (${x}, ${y}) via ${pipe_map[y][x]}`);
    if (pipe_map[y][x] === '.') {
        return [undefined, undefined, undefined];
    }
    else if (pipe_map[y][x] === '|') {
        if (direction === 'south')
            return [y + 1, x, direction];
        else if (direction === 'north')
            return [y - 1, x, direction];
    }
    else if (pipe_map[y][x] === '-') {
        if (direction === 'east')
            return [y, x + 1, direction];
        else if (direction === 'west')
            return [y, x - 1, direction];
    }
    else if (pipe_map[y][x] === 'L') {
        if (direction === 'south')
            return [y, x + 1, 'east'];
        else if (direction === 'west')
            return [y - 1, x, 'north'];
    }
    else if (pipe_map[y][x] === 'J') {
        if (direction === 'east')
            return [y - 1, x, 'north'];
        else if (direction === 'south')
            return [y, x - 1, 'west'];
    }
    else if (pipe_map[y][x] === '7') {
        if (direction === 'east')
            return [y + 1, x, 'south'];
        else if (direction === 'north')
            return [y, x - 1, 'west'];
    }
    else if (pipe_map[y][x] === 'F') {
        if (direction === 'west')
            return [y + 1, x, 'south'];
        else if (direction === 'north')
            return [y, x + 1, 'east'];
    }

    // this should only happen when we're checking around S for a step to take and find a piece of the pipe that isn't a path out of S
    console.log(`Unable to find next step: (${x}, ${y}) = ${pipe_map[y][x]} -> ${direction}`);
    return [undefined, undefined, undefined];
}
// find the starting point ('S') in the puzzle grid
let s_y, s_x;
[s_y, s_x] = [0, 0];
s_finder: for (let pipe_map_y = 0; pipe_map_y < pipe_map.length; pipe_map_y++) {
    for (let pipe_map_x = 0; pipe_map_x < pipe_map[pipe_map_y].length; pipe_map_x++) {
        if (pipe_map[pipe_map_y][pipe_map_x] === 'S') {
            [s_y, s_x] = [pipe_map_y, pipe_map_x]
            console.log(`Found S @ (${s_x}, ${s_y})`);
            break s_finder;
        }
    }
}
// keep track of how many steps we have taken
let step_count = 0;

// we need to determine which way to go from S
const steps_from_s = [[s_y - 1, s_x, 'north'], [s_y + 1, s_x, 'south'], [s_y, s_x - 1, 'west'], [s_y, s_x + 1, 'east']];
let try_y, try_x, try_direction;
let next_y, next_x, next_direction;
for ([try_y, try_x, try_direction] of steps_from_s) {
    let test_y, test_x, test_direction;
    [test_y, test_x, test_direction] = get_next_step(try_y, try_x, try_direction);
    if (test_direction) {
        // console.log(`Starting from S at (${try_x}, ${try_y}), headed ${try_direction}`);
        [next_y, next_x, next_direction] = [try_y, try_x, try_direction];
        step_count++;
        break;
    }
}

// walk the path
while (next_y != s_y || next_x != s_x) {
    [next_y, next_x, next_direction] = get_next_step(next_y, next_x, next_direction);
    // console.log(`From (${next_x}, ${next_y}), headed ${next_direction}`);
    step_count++;
}

console.log(`Furthest path distance from S is ${step_count/2}`);
