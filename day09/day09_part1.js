"use strict";

const fs = require('fs');

// this works for Objects but not for Classes
function pretty_print_object(s) {
    console.log(JSON.stringify(s, undefined, 2));
}

// must use full path when executing node in vscode, because vscode does not start node in the script's directory...
// const filename = '/home/jay/source/aoc2023/day09/sample.txt';
const filename = '/home/jay/source/aoc2023/day09/input.txt';

let lines = fs.readFileSync(filename, 'utf-8').split(/\r?\n/).filter(l => l.length > 0);
// pretty_print_object(lines);

const histories = lines.map(line => line.split(/\s+/).map(Number));

function calculate_predictions(running_total, history) {
    const deltas = [history];
    let current_delta = deltas[0];

    // moving backward - recreate the sequence that generated this round
    while (true) {
        const next_delta = [];
        deltas.push(next_delta);
        for (let i = 1; i < current_delta.length; i++)
            next_delta.push(current_delta[i] - current_delta[i-1]);
        current_delta = next_delta;
        if (next_delta.every(x => !x))
            break;
    }

    // now, move forward again to eventually extend the original sequence
    deltas.at(-1).push(0);
    for (let i = deltas.length - 2; i > 0; i--)
        deltas[i-1].push(deltas[i-1].at(-1) + deltas[i].at(-1));

    return running_total + deltas[0][deltas[0].length-1];
}

const answer = histories.reduce(calculate_predictions, 0);
console.log(answer);
