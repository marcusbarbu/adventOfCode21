test_input='''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''

def parse_input(inputstr: str):
    boards = inputstr.split('\n\n')
    calls = boards[0]
    return calls, boards[1:]


class Board:
    def __init__(self, initstr: str):
        self.rows = []
        self.initstr = initstr
        self.marks = []
        self.populate()
        self.bingo = False
    
    def populate(self):
        self.rows = [[int(x) for x in row.split()] for row in self.initstr.splitlines()]
        n_rows = len(self.rows)
        n_cells = len(self.rows[0])
        self.marks = [[False]*n_cells for _ in range(n_rows)]
    
    def call(self, num):
        done = False
        for i, r in enumerate(self.rows):
            for j,c in enumerate(r):
                if c == num:
                    self.marks[i][j] = True
                    # print(f"Hit for {num} {i} {j}")
                    done = True
                    break
            if done:
                break
    
    def check(self):
        for row in self.marks:
            if row == [True] * len(row):
                self.bingo = True
                return True
        cols = [[False] * len(self.rows) for _ in range(len(self.rows[0]))]
        for i, row in enumerate(self.marks):
            for j, mark in enumerate(row):
                cols[j][i] = mark

        for col in cols:
            if col == [True] * len(col):
                self.bingo = True
                return True
        return False

    def unmarked_sum(self):
        s = 0
        for i, row in enumerate(self.rows):
            for j, cell in enumerate(row):
                if not self.marks[i][j]:
                    s += cell
        return s
    
    def __repr__(self) -> str:
        l = ['Begin Board:']
        for row in self.rows:
            l.append('-'.join([str(r) for r in row]))
        for m in self.marks:
            l.append('-'.join(['x' if r else 'o' for r in m ]))
        l.append('End')
        return '\n'.join(l)



calls, boardstrs = parse_input(test_input)
with open('input','r') as infile:
    calls, boardstrs = parse_input(infile.read())

boards = []
for b in boardstrs:
    br = Board(b)
    boards.append(br)
    # print(br)


call_nums = [int(x) for x in calls.strip().split(',')]
bingos = []
for cn in call_nums:
    # print(f"Calling {cn}")
    for i,b in enumerate(boards):
        if i not in bingos:
            b.call(cn)
            # print(b)
            if b.check():
                s = b.unmarked_sum()
                total = cn * s
                print(f"Bingo board {i} score {s} * {cn} == {total}")
                bingos.append(i)