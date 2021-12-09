from queue import Queue
test_input = '''2199943210
3987894921
9856789892
8767896789
9899965678'''

class Board:
    def __init__(self, data_in):
        self.raw = data_in
        self.rows = []
        self.parse()
    
    def parse(self):
        for r in self.raw.splitlines():
            self.rows.append([int(x) for x in r])
    

    def is_low_point(self, row, col, visited=set()):
        options = []
        if row >= len(self.rows) or row < 0 or col >= len(self.rows[0]) or col < 0:
            return False
        target = self.rows[row][col]
        if target == 9:
            return False
        for i in range(-1, 2):
            options.append((row + i, col))
            options.append((row, col+i))
        checks = [self.rows[x][y] for (x, y) in options if (x,y) != (row, col) and x in range(0, len(self.rows)) and y in range(0, len(self.rows[0])) and (x,y) not in visited]
        if len(checks) == 0:
            return False
        if target < min(checks):
            return True
        else:
            return False
    
    def find_lows(self):
        points = []
        for r in range(len(self.rows)):
            for c in range(len(self.rows[r])):
                if self.is_low_point(r, c):
                    points.append((r, c))
        return points
    
    def score_points(self, pl):
        score = 0
        for (r,c) in pl:
            score += (self.rows[r][c] + 1)
        return score
    
    def find_basin(self, seed):
        max_r = len(self.rows)
        max_c = len(self.rows[0])
        nodes = Queue()
        nodes.put(seed)
        basin = set()
        visited = set()
        while nodes.qsize() > 0:
            r,c = nodes.get()
            if r >= max_r or r < 0  or c >= max_c or c < 0 or (r,c) in visited:
                continue
            visited.add((r,c))
            if self.rows[r][c] != 9:
                basin.add((r,c))
                for i in range(-1, 2):
                    a = (r+i, c)
                    b = (r, c+i)
                    print(f'Adding {a} and {b}')
                    nodes.put(a)
                    nodes.put(b)
        return basin

            


        
    
        

b = Board(test_input)
b = Board(open('input','r').read())
lows = b.find_lows()
score = b.score_points(lows)

sizes = []
for l in lows:
    basin = b.find_basin(l)
    sizes.append(len(basin))
    print(f'Basin for {l}: {len(basin)}: {basin}')

sizes = sorted(sizes)[-3:]
score = 1
for s in sizes:
    score *= s

print(f'Basin score: {score}')
