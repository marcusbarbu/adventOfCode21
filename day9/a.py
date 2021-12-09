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
    

    def is_low_point(self, row, col):
        options = []
        for i in range(-1, 2):
            options.append((row + i, col))
            options.append((row, col+i))
        checks = [self.rows[x][y] for (x, y) in options if (x,y) != (row, col) and x in range(0, len(self.rows)) and y in range(0, len(self.rows[0]))]
        target = self.rows[row][col]
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
        

b = Board(test_input)
b = Board(open('input','r').read())
lows = b.find_lows()
score = b.score_points(lows)

print(f'Found score: {score} from lows: {lows}')