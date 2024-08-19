"use strict";

// const filename = '/home/jay/source/aoc2023/day01/sample.txt';
const filename = '/home/jay/source/aoc2023/day01/input.txt';

const fs = require('fs');
const lines = fs.readFileSync(filename, 'utf-8').split(/\r?\n/).filter(l => l.length > 0);
// console.log(lines);


// This section of code is an accumulator -- I would use array.reduce instead of array.forEach
// The general rule of thumb I use is "don't use forEach when another function will suffice".
// I typically use forEach when I need a "side effect", like I/O
const INITIAL_VALUE = 0

const sum = lines.reduce((accumulator, line) => {
    const regex = /(\d)/;
    let calibration_value = parseInt(regex.exec(line)[1]) * 10 + 
        parseInt(regex.exec(line.split('').reverse().join(''))[1]);
    return accumulator + calibration_value;
}, INITIAL_VALUE)

console.log(sum);
