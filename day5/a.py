import re
from collections import defaultdict

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

# all_lines, max_val = parse_input(test_input)
all_lines, max_val = parse_input(open('input','r').read())
pruned_lines = [tpl for tpl in all_lines if tpl[0][0]==tpl[1][0] or tpl[0][1]==tpl[1][1]]
print(pruned_lines, max_val)

hits = defaultdict(int)

for line in pruned_lines:
    (a, b), (c, d) = line
    if a == c:
        start = b if b < d else d
        end = d if start == b else b
        for j in range(start, end+1):
            hits[(a, j)] += 1
            # print(hits)
    if b == d:
        start = a if a < c else c
        end = c if start == a else a
        for j in range(start, end+1):
            hits[(j, b)] += 1
            # print(hits)

count = 0
for k, v in hits.items():
    if v >= 2:
        count += 1
print(f"count: {count}")