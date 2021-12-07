import math

test_input = '16,1,2,0,4,2,7,1,2,14'
values = [int(x) for x in test_input.split(',')]
values = [int(x) for x in open('input','r').read().split(',')]

sv = sorted(values)
print(f'{sv}')

mean = sum(sv)//len(sv)
print(f'{mean}')

costs = []
for mean in range(mean - 1, mean + 2):
    ncs = []
    for x in values:
        diff = abs(mean - x)
        c = (diff * (diff + 1)) / 2
        ncs.append(c)
    costs.append(sum(ncs))
    
print(f'Min: {min(costs)}')
