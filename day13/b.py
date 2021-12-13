test_input = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''

class Transparency:
    def __init__(self, raw):
        self.raw = raw
        self.coords = set()
        self.folds = []
        self.max_x =0
        self.max_y =0
        self.parse()

    def parse(self):
        lines = self.raw.splitlines()
        fold_starts = 0
        for i,l in enumerate(lines):
            if len(l) == 0:
                fold_starts = i
                break
            x, y = l.split(',')[:2]
            x, y = int(x), int(y)
            self.coords.add((x,y))
        folds = lines[fold_starts+1:]
        for f in folds:
            dir_chr, val = f.split('=')[:2]
            self.folds.append((dir_chr[-1], int(val)))
    
    def fold(self, fold_index=0, coords = None):
        new_coords = set()
        if coords is None:
            coords = self.coords
        direction, location = self.folds[fold_index] 
        for x,y in coords:
            if direction == 'x':
                if x > location:
                    x = location - (x - location)
                new_coords.add((x,y))
            if direction == 'y':
                if y > location:
                    y = location - (y - location)
                new_coords.add((x,y))
        return new_coords
    
    def all_folds(self):
        start_coords = self.coords
        for f in range(len(self.folds)):
            start_coords = self.fold(f, start_coords)
            # print(f'Coords: {start_coords}, len: {len(start_coords)}')
        self.coords = start_coords
        return self.coords

    def __repr__(self):
        max_r = max([r[1] for r in self.coords])
        max_c = max([r[0] for r in self.coords])
        output_array = [['.'] * (max_c + 1) for _ in range(max_r + 1)]
        for r, c in self.coords:
            try:
                output_array[c][r] = '#'
            except Exception as e:
                print(f"failed on {c}:{r} {e}")
        s = ''
        array_lines = []
        for o in output_array:
            array_lines.append(''.join(o))
        s = '\n'.join(array_lines)
        return s


t = Transparency(test_input)
t = Transparency(open('input','r').read())
# t.all_folds()
coords = t.fold(0)
coords = t.all_folds()
# print(f'Coords: {coords} Num dots: {len(coords)}')

print(t)