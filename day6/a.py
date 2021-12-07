import time
import copy
test_input = '''3,4,3,1,2'''

start_set = [int(x) for x in test_input.split(',')]
start_set = [int(x) for x in open('input','r').read().split(',')]
print(start_set)

def step_fish(initial):
    new_fish = []
    out_set = []
    for fish in range(len(initial)):
        cur = initial[fish]
        if cur == 0:
            new_fish.append(8)
            cur = 7
        out_set.append(cur - 1)
    return out_set + new_fish


fish = copy.deepcopy(start_set)
for i in range(256):
    a = time.perf_counter()
    fish = step_fish(fish)
    b = time.perf_counter()
    # print(f"After {i}: {fish}")
    print(f'Step {i}: {b - a}')

print(f'Total fish: {len(fish)}')