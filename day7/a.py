test_input = '16,1,2,0,4,2,7,1,2,14'

values = [int(x) for x in test_input.split(',')]
values = [int(x) for x in open('input','r').read().split(',')]
median = sorted(values)[len(values)//2]
print(f'median: {median} len: {len(values)}')

deltas = [abs(x - median) for x in values]
print(f'deltas: {deltas} {sum(deltas)}')
