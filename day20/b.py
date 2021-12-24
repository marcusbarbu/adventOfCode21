import copy
import bitarray
import bitarray.util
from collections import defaultdict

def board_to_tupls(board, default):
    d = defaultdict(lambda: default)
    for r in range(len(board)):
        for c in range(len(board[r])):
            cur = board[r][c]
            if cur == '#':
                d[(r,c)] = True
            else:
                d[(r,c)] = False
                
    return d, len(board), c

def parse(in_str):
    algo = []
    cur = []
    is_algo = True
    for l in in_str.splitlines():
        if len(l) == 0:
            is_algo = not is_algo
        if is_algo:
            algo.append(l)
        else:
            cur.append(l)
    algo = ''.join(algo)
    algo = [c == '#' for c in algo]

    cur,r,c = board_to_tupls(cur, False)
    return algo, cur, r, c


class Board:
    def __init__(self, raw):
        a, b, rows, cols = parse(raw)
        self.lookup_table = a
        self.internal_state = b
        self.alternating = self.lookup_table[0]
        if self.alternating:
            self.external_state = not self.lookup_table[0]
        self.rows, self.cols = rows, cols
        self.minr, self.minc = 0, 0
    
    
    def find_min_max_eval(self):
        return (self.minr - 1, self.minc - 1), (self.rows + 1, self.cols + 1)
    
    def __repr__(self) -> str:
        out = []
        min_coord, max_coord = self.find_min_max_eval()
        print(f'Min {min_coord} max {max_coord}')
        for r in range(min_coord[0], max_coord[0]+1):
            row = []
            for c in range(min_coord[1], max_coord[1]+1):
                if self.internal_state[(r,c)]:
                    row.append('#')
                else:
                    row.append(' ')
            out.append(''.join(row))
        return '\n'.join(out) 
    
    def eval_point(self, r, c):
        b = bitarray.bitarray()
        for row in range(r-1, r+2):
            for col in range(c-1, c+2):
                pt = (row, col)
                val = self.internal_state[pt]
                if val:
                    b.append(1)
                else:
                    b.append(0)
        num = bitarray.util.ba2int(b)
        return num

    def step(self):
        print(f'At this step, all external pixels should be: {self.external_state}')
        print(f'Starting length: {len(self.internal_state)}')
        out = []
        d = defaultdict(lambda: self.external_state)
        minpt, maxpt = self.find_min_max_eval()
        for r in range(minpt[0], maxpt[0]+1):
            for c in range(minpt[1], maxpt[1]+1):
                n = self.eval_point(r, c)
                d[(r,c)] = self.lookup_table[n]
        self.internal_state = d
        print(f'ending length: {len(self.internal_state)}')
        if self.alternating:
            self.external_state = not self.external_state
        self.minr -= 1
        self.minc -= 1
        self.rows += 1
        self.cols += 1
    
    def count(self):
        return len([x for x in self.internal_state.items() if x[1]])

b = Board(open('test_input','r').read())
b = Board(open('input','r').read())
print(b)
for i in range(50):
    b.step()
    # print(b)
    print(f'After {i+1} steps, {b.count()} pixels lit')

print(f'After {i+1} steps, {b.count()} pixels lit')