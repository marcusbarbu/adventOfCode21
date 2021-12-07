import time
import copy
from collections import defaultdict
test_input = '''3,4,3,1,2'''

# start_set = [int(x) for x in test_input.split(',')]
start_set = [int(x) for x in open('input','r').read().split(',')]
def step_fish_dict(fdict):
    out_dict = defaultdict(int)
    for i in range(9):
        if i == 0:
            out_dict[8] += fdict[i]
            out_dict[6] += fdict[i]        
        else:
            out_dict[i-1] += fdict[i]
    return out_dict


fish = copy.deepcopy(start_set)
fish_dict = defaultdict(int)
for f in fish:
    fish_dict[f] += 1

for i in range(256):
    # print(f"Day {i}: {fish_dict}")
    # print(f'Total fish: {sum(fish_dict.values())}')
    a = time.perf_counter()
    fish_dict = step_fish_dict(fish_dict)
    b = time.perf_counter()
    print(f'Step {i}: {b-a}')

print(f'Total fish: {sum(fish_dict.values())}')