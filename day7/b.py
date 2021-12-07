import math

test_input = '16,1,2,0,4,2,7,1,2,14'
values = [int(x) for x in test_input.split(',')]
values = [int(x) for x in open('input','r').read().split(',')]

sv = sorted(values)
print(f'{sv}')

mean = sum(sv)//len(sv)
print(f'{mean}')

ncs = []
for x in values:
    diff = abs(mean - x)
    c = (diff * (diff + 1)) / 2
    ncs.append(c)
    
print(f'{sum(ncs)}')
