"use strict";

// this works for Objects but not for Classes
function pretty_print_object(s) {
    console.log(JSON.stringify(s, undefined, 2));
}

// const filename = '/home/jay/source/aoc2023/day04/sample.txt';
const filename = '/home/jay/source/aoc2023/day04/input.txt';

const fs = require('fs');
let lines = fs.readFileSync(filename, 'utf-8').split(/\r?\n/).filter(l => l.length > 0);
// pretty_print_object(lines);

let score = 0;
lines.forEach(line => {
    // can turn this into a single line and use const;
    const [wins, nums] = line.split(':')[1].split('|').map(x => x.trim());
    let winners = wins.split(/\s+/).map(x => parseInt(x));
    let matching_numbers = nums.split(/\s+/).map(x => parseInt(x)).filter(x => winners.includes(x));
    console.log(matching_numbers);
    if (matching_numbers.length)
        score += 2**(matching_numbers.length-1);
});
console.log(score);
