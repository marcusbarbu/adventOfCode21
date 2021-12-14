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
lines = list(open('input','r').read().splitlines())
template = lines[0]

changes = []
for l in lines[1:]:
    if len(l) > 0:
        target, new = l.split('->')[:2]
        t = target.strip()
        n = new.strip()
        changes.append((t, t[0]+n, n+t[1]))
        print(f'{t}->{n} creates {t[0]+n} and {n+t[1]}')

def split_pairs(template):
    pairs = [template[i:i+2] for i in range(0, len(template)-1)]
    return Counter(pairs)

def evaluate_changes(pair_dict, changelist, letter_counter):
    new_counter = Counter()
    for pair, _ in pair_dict.items():
        new_counter[pair] = 0
    for target, a1, a2 in changelist:
        try:
            target_count = pair_dict[target]
            print(f'{target_count} {target} creates {target_count} {a1} and {target_count} {a2}')
            letter_counter[a1[1]] += target_count
            new_counter[a1] += target_count
            new_counter[a2] += target_count 
        except Exception as e:
            print(f"Failed to insert at {a1}/{a2} {target} with exc {e}")
    return new_counter, letter_counter


tdict = split_pairs(template)
letter_counter = Counter(template)
print(tdict)
for i in range(40):
    tdict, letter_counter = evaluate_changes(tdict, changes, letter_counter)
    print(f'Template {i} {tdict}')
    # print(f'Iter {i}')


# c = Counter(''.join(out))
print(letter_counter)
total = letter_counter.most_common()
most = total[0][1]
least = total[-1][1]

print(f'Most ({most})-least ({least}) = {most - least}')
