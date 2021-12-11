from collections import defaultdict
from typing import List
import time
test_data = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''


class Cave:
    def __init__(self, raw):
        self.rows = []
        self.parse(raw)
        self.max_row = len(self.rows)
        self.max_col = len(self.rows[0])
        print(f'MR: {self.max_row} MC: {self.max_col}')
        self.total_flashes = 0
    
    def __repr__(self) -> str:
        return '\n'.join(['  '.join([str(x) for x in r]) for r in self.rows])
    
    def parse(self, raw):
        rl = raw.splitlines()
        for r in rl:
            c = [int(x) for x in r]
            self.rows.append(c)
        
    def step(self):
        flashes = []
        for r in range(len(self.rows)):
            for c in range(len(self.rows[r])):
                self.rows[r][c] += 1
                if self.rows[r][c] > 9:
                    print(f'Original flash: {r}:{c}')
                    flashes.append((r,c))
        print("Before flashes")
        print(self)
        print("ENDBefore flashes")
        return self.handle_flashes(flashes)
    
    def handle_flashes(self, flashes: List):
        index = 0
        while len(flashes) > index:
            r, c = flashes[index]
            adjacents = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nr = r+i
                    nc = c+j
                    if nr < 0 or nr >= self.max_row or nc < 0 or nc >= self.max_col or (i == 0 and j == 0):
                        # print(f'{nr}:{nc} was too great')
                        continue
                    else:
                        adjacents.append((nr,nc))
            print(f'Adjacents for {r}:{c} -> {adjacents}')
            for ar, ac in adjacents:
                if self.rows[ar][ac] > 9:
                    continue
                self.rows[ar][ac] += 1
                if self.rows[ar][ac] > 9:
                    print(f'Secondary flash: {ar}:{ac}')
                    flashes.append((ar,ac))
            index += 1
        for r, c in flashes:
            self.rows[r][c] = 0
        self.total_flashes += len(flashes)
        print(f'Single round len: {len(flashes)}')
        if len(flashes) == 100:
            return True
        return False

small_data = '''11111
19991
19191
19991
11111'''
# c = Cave(test_data)
# c = Cave(small_data)
c = Cave(open('input','r').read())
print(c.rows)

i = 0
res = False
while not res:
    res = c.step()
    print(c)
    print(f'After round {i}, {c.total_flashes} flashes')
    # time.sleep(5)
    i += 1
    if res:
        print(f"Round number: {i}")
        break