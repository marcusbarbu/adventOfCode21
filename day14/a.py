import re
from collections import Counter
test_input = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

'''

lines = list(test_input.splitlines())
# lines = list(open('input','r').read().splitlines())
template = lines[0]

changes = []
for l in lines[1:]:
    if len(l) > 0:
        target, new = l.split('->')[:2]
        changes.append((target.strip(), new.strip()))

print(template)
print(changes)

def evaluate_changes(orig: str, change_list):
    dd = {}
    for target, change in change_list:
        if target in orig:
            for find in re.finditer(f'(?={target})', orig):
                index = find.start()
                print(f'found {target} => {change} at {index}')
                dd[index] = change
    output = []
    for i, c in enumerate(orig):
        output.append(c)
        print(f'Orig {c} at {i}')
        if i in dd.keys():
            print(f'Inserting {dd[i]}')
            output.append(dd[i])
    return ''.join(output)

for i in range(10):
    template = evaluate_changes(template, changes)
    print(f'Template {template}')

c = Counter(template)
print(c)
total = c.most_common()
most = total[0][1]
least = total[-1][1]

print(f'Most ({most})-least ({least}) = {most - least}')