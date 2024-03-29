import re
from dataclasses import dataclass, field
from typing import Any, List, Tuple
test_input = 'target area: x=20..30, y=-10..-5'

@dataclass
class P2D:
    x: int
    y: int

    def __repr__(self) -> str:
        return f'x: {self.x} y: {self.y}'

@dataclass
class TargetRange:
    x_range: Tuple[int, int]
    y_range: Tuple[int, int]

    def contains(self, pos: P2D):
        # print(f'Is {pos.x} in {self.x_range[0]} to {self.x_range[1]}, {pos.y} in {self.y_range[0]}, {self.y_range[1]}')
        return pos.x in range(self.x_range[0], self.x_range[1] + 1) and (pos.y in range(self.y_range[0], self.y_range[1] + 1))
    
    def pos_is_below(self, pos: P2D):
        return pos.y < self.y_range[0] and pos.y < self.y_range[1]
    
    def __repr__(self) -> str:
        return f'X: {self.x_range[0]} -> {self.x_range[1]} Y: {self.y_range[0]} -> {self.y_range[1]}'

def parse(instr):
    m = re.match('target area: x=(-*\d+)..(-*\d+), y=(-*\d+)..(-*\d+)', instr)
    g = m.groups()
    x_range = (int(g[0]), int(g[1]))
    y_range = (int(g[2]), int(g[3]))
    return TargetRange(x_range, y_range)

def single_step(pos: P2D, vel: P2D, target: TargetRange):
    contains = False
    pos.x += vel.x
    pos.y += vel.y
    vel.y -= 1
    if vel.x < 0:
        vel.x += 1
    elif vel.x > 0:
        vel.x -= 1
    contains = target.contains(pos)
    return pos, vel, contains

def shoot(vel: P2D, target: TargetRange):
    pos = P2D(0,0)
    done = False
    heights = []
    while (not target.pos_is_below(pos)) and (not done):
        pos, vel, done = single_step(pos, vel, target)
        heights.append(pos.y)
    if done:
        return True, max(heights)
    else:
        return False, 0


target = parse(test_input)
target = parse(open('input','r').read())
heights = {}
yr_min = target.y_range[0] - 1
yr_max = abs(target.y_range[0]) + 1
for x in range(target.x_range[1] * 2):
    for y in range(yr_min, yr_max):
# for x in range(10):
#     for y in range(10):
        vel = P2D(x, y)
        key = (vel.x, vel.y)
        # print(f'Testing {vel}')
        success, height = shoot(vel, target)
        if success:
            heights[key] = height

print(max(heights.items(), key= lambda x: x[1]))
# print(heights.keys())
print(len(heights))

# shoot(P2D(6,9), target)
# shoot(P2D(7,9), target)