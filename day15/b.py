import heapq
from dataclasses import dataclass, field
from typing import Any
from itertools import count


test_data = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''

@dataclass(order=True)
class HeapEntry:
    score: int
    key: Any=field(compare=False)
    active: Any=field(compare=False)
    uniq: int


class PriorityHeap:
    def __init__(self):
        self.heap = []
        self.lookup = {}
        self.counter = count()
    
    def remove_with_key(self, key):
        entry = self.lookup.pop(key)
        entry.active = False
    
    def insert_or_update(self, key, score):
        if key in self.lookup.keys():
            self.remove_with_key(key)
        uniq = next(self.counter)
        entry = HeapEntry(score, key, True, uniq)
        self.lookup[key] = entry
        heapq.heappush(self.heap, entry)
    
    def pop(self):
        while len(self.heap) > 0:
            item: HeapEntry = heapq.heappop(self.heap)
            if item.active:
                del self.lookup[item.key]
                return item.key, item.score
    
    def is_empty(self):
        return len(self.lookup) == 0

    def remaining(self):
        return len(self.lookup)
    
    def contains(self, key):
        return key in self.lookup.keys()
    
class ChitonCave:
    def __init__(self, raw):
        self.raw = raw
        self.rows = [[int(x) for x in l] for l in raw.splitlines()]
        self.max_orig_row = len(self.rows)
        self.max_orig_col = len(self.rows[0])
        self.max_row = self.max_orig_row * 5
        self.max_col = self.max_orig_col * 5
    
    def get_score(self, row, col):
        base_row = row % self.max_orig_row
        base_col = col % self.max_orig_col
        row_box = row // self.max_orig_row
        col_box = col // self.max_orig_col
        # print(f'Row_box {row_box} col_box {col_box}')
        base_score = self.rows[base_row][base_col]
        score_offset = row_box + col_box
        new_score = base_score + score_offset
        if new_score > 9:
            new_score -= 9
        # print(f'for {row}:{col} base is {base_row}:{base_col} so {score_offset}, score {base_score} -> {new_score}')
        return new_score

    def get_neighbors(self, row, col):
        options = []
        for i in range(-1, 2):
            nr = row + i
            nc = col + i
            if nr in range(0, self.max_row) and (nr, col) != (row, col):
                options.append((nr, col))
            if nc in range(0, self.max_col) and (row, nc) != (row, col):
                options.append((row, nc))
        # print(f'Options for {row},{col}: {options}')
        return options
    
    def dijkstra(self):
        start = (0, 0)
        distances = {}
        prev = {}
        lookup = {}

        ph = PriorityHeap()
        for row in range(self.max_row):
            for col in range(self.max_col):
                pos = (row, col)
                distances[pos] = 123123123123
                prev[pos] = None
                ph.insert_or_update(pos, distances[pos])
        distances[start] = 0
        ph.insert_or_update(start, distances[start])
        print(ph)
        while not ph.is_empty():
            cur, val = ph.pop()
            print(f'Current node addr {cur}. Unvisited: {ph.remaining()}')
            neighbors = self.get_neighbors(cur[0],cur[1])
            for n in neighbors:
                if not ph.contains(n):
                    continue
                ndist = distances[cur] + self.get_score(cur[0], cur[1])
                if ndist < distances[n]:
                    distances[n] = ndist
                    prev[n] = cur
                    ph.insert_or_update(n, ndist)
        return distances, prev
    
    def find_path_score(self, distances, prevs):
        cur = (self.max_row - 1, self.max_col - 1)
        path = [cur]
        score = distances[cur]
        while cur != (0,0):
            # print(f'{cur}->')
            cur = prevs[cur]
            path.append(cur)
        # print(f'{cur}')
        return path, score

    def print_board(self, path=None):
        rows = []
        for r in range(self.max_row):
            row = []
            for c in range(self.max_col):
                if path:
                    if (r, c) in path:
                        row.append(str(self.get_score(r,c)))
                    else:
                        row.append('.')
                else:
                    row.append(str(self.get_score(r,c)))
            rows.append(''.join(row))
        print('\n'.join(rows))
        
    def secondary_calc(self, path):
        score = 0
        for r,c in path[:-1]:
            score += self.get_score(r,c)
        return score


cc = ChitonCave(test_data)
cc = ChitonCave(open('input','r').read())
fn = cc.get_neighbors(0,0)
dists, prevs = cc.dijkstra()
path, score = cc.find_path_score(dists, prevs)
cc.print_board()
print(f'Final score: {score}')
print(f'Secondary calc: {cc.secondary_calc(path)}')