#!/usr/bin/env python3
import sys

TEST_DATA = [ 199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

def make_windows(data_in, wl):
    wins = []
    for i in range(0, len(data_in) - (wl-1)):
        wins.append(sum([int(z) for z in data_in[i:i+wl]]))
    print(wins)
    return wins

def check_change(wins):
    prev = 0
    gt = -1
    for w in wins:
        if w > prev:
            gt+=1
        prev = w
    print(gt) 

if __name__ == '__main__':
    windows = make_windows(sys.stdin.readlines(), 3)
    check_change(windows)