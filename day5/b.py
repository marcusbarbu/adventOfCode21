import re
from collections import defaultdict
import copy

test_input = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''

def parse_input(input_str):
    fmt = '(\d+),(\d+) -> (\d+),(\d+)'
    out = []
    cur_max = 0
    for line in input_str.splitlines():
        match = re.match(fmt, line)
        mg = [int(m) for m in match.groups()]
        cur_max = max(max(mg), cur_max)
        out.append(((mg[0], mg[1]), (mg[2], mg[3])))
    return out, cur_max

all_lines, max_val = parse_input(test_input)
all_lines, max_val = parse_input(open('input','r').read())

hits = defaultdict(int)

for line in all_lines:
    (a, b), (c, d) = line

    if a < c or b < d:
        start_row = a
        end_row = c
        start_col = b
        end_col = d
    else:
        start_row = c
        end_row = a
        start_col = d
        end_col = b

    # print(f'line: {start_row}:{start_col} -> {end_row}:{end_col}')
    if start_row == end_row:
        row_path = [start_row] * (end_col+1 - start_col)
        col_path = range(start_col, end_col+1)
    elif start_col == end_col:
        col_path = [start_col] * (end_row+1 - start_row)
        row_path = range(start_row, end_row+1)
    else:
        col_step = 1
        row_step = 1
        if start_col > end_col:
            col_step = -1
            end_col -= 2
        if start_row > end_row:
            row_step = -1
            end_row -= 2


        col_path = range(start_col, end_col+1, col_step)
        row_path = range(start_row, end_row+1, row_step)
        # print(f'diag path row: {row_path}:{list(row_path)} col: {col_path}:{list(col_path)}')

    path = zip(row_path, col_path)
    # cpath = copy.deepcopy(path)
    # print(f"line {line} path: {list(cpath)}")
    for r, c in path:
        # print(f'{r}:{c}')
        hits[(r,c)] += 1
        # print(hits)


count = 0
for k, v in hits.items():
    if v >= 2:
        count += 1
print(f"count: {count}")