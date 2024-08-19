"use strict";

// const filename = '/home/jay/source/aoc2023/day02/sample.txt';
const filename = '/home/jay/source/aoc2023/day02/input.txt';

const fs = require('fs');
let lines = fs.readFileSync(filename, 'utf-8').split(/\r?\n/).filter(l => l.length > 0);
// console.log(lines);

const max = {red: 12, green: 13, blue: 14};
let count = 0;


// This is a really big "Anonymous function".  Most would say keep your anonymous functions shorter, because you can't name them
// I would break this out into it's own named function.  Same goes for the large inner functions.  For example:
const processLine = (line) => {
    // this variable can be "const" -- Seems dumb, but when you aren't changing the "reference", its considered const.
    // const in javascript just means that specific variable is not to be re-assigned -- you can however change values within the
    // object itself.

    // The general rule of thumb is to never use "let" unless you MUST
    const group = {red: 0, green: 0, blue: 0};

    const group_id = parseInt(/(\d+):/.exec(line)[1]);

    const color_counter = /(\d+)/; // type is RegExp
    line.split(': ')[1].split('; ').forEach(draw => {
        draw.split(', ').forEach(value_and_color => {
            switch (/(red|green|blue)/.exec(value_and_color)[1]) {
                case 'red':
                    group.red = Math.max(group.red, parseInt(color_counter.exec(value_and_color)[1]));
                    break;
                case 'green':
                    group.green = Math.max(group.green, parseInt(color_counter.exec(value_and_color)[1]));
                    break;
                case 'blue':
                    group.blue = Math.max(group.blue, parseInt(color_counter.exec(value_and_color)[1]));
                    break;
            }                    
        });
    });

    if (group.red <= max.red && group.green <= max.green && group.blue <= max.blue)
        count += group_id;
}

lines.forEach(processLine);

console.log(count);
