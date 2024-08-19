"use strict";

// this works for Objects but not for Classes
function pretty_print_object(s) {
    console.log(JSON.stringify(s, undefined, 2));
}

// const filename = '/home/jay/source/aoc2023/day03/sample.txt';
const filename = '/home/jay/source/aoc2023/day03/input.txt';

const fs = require('fs');
let lines = fs.readFileSync(filename, 'utf-8').split(/\r?\n/).filter(l => l.length > 0);
// pretty_print_object(lines);

// first, find every symbol and store all of the coordinates around it, so we can use them later
let adjacent_coordinates = new Set();
const numbers = '1234567890';
const non_symbols = numbers + '.';
for (let y = 0; y < lines.length; y++) {
    for (let x = 0; x < lines[0].length; x++) {
        if (!non_symbols.includes(lines[y][x])) {
            // console.log(`Symbol ${lines[y][x]} found at (${x},${y})`);
            // record adjacent coordinates
            for (let y1 = y-1; y1 <= y+1; y1++) {
                for (let x1 = x-1; x1 <= x+1; x1++) {
                    if (x1 != x || y1 != y) {
                        const coord = `${x1},${y1}`;
                        // console.log(coord);
                        adjacent_coordinates.add(coord);
                    }
                }
            }
        }
    }
}

// second, find every part number on each line and check if any of its digits are a symbol-adjacent coordinate
// Again, dumb, but const does not mean the variable is static it just means the variable cannot be re-assigned
const part_numbers = [];
let line_number = 0;
lines.forEach(line => {
    const number_finder = /(\d+)/g;
    let found_number;
    while ((found_number = number_finder.exec(line)) != null) {
        const number = parseInt(found_number[1]);
        for (let i = found_number.index; i < number_finder.lastIndex; i++)
        {
            const coord = `${i},${line_number}`;
            if (adjacent_coordinates.has(coord)) {
                part_numbers.push(number);
                // console.log(`${coord}: ${number}`);
                break;
            }
        }
    }
    line_number++;
});

let sum = part_numbers.reduce((i, j) => i + j, 0);
console.log(sum);
