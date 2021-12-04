import copy
test_data = '''
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''

with open('input', 'r') as infile:
    test_data = infile.read()

dl = [int('0b'+line.strip(),0) for line in test_data.split() if len(line) > 2]
bitwidth = len(test_data.split()[3])

def get_bit_from_problem_index(p_i):
    global bitwidth
    return bitwidth - (p_i)

def get_hot_not_bits(num_list):#, condition_index=None, condition_value=0):
    global bitwidth
    nl_len = len(num_list)
    counts = [0] * bitwidth
    hots = 0
    nots = 0
    for n in num_list:
        # print(f"Considering {bin(n)}")
        # if condition_index:
        #     if (n & (condition_value << (bitwidth - condition_index))) != (condition_value << (bitwidth - condition_index)):
        #         print("not hot enough")
        #         continue
        counts = [counts[i]+1 if (n & (1 << i)) != 0 else counts[i] for i in range(bitwidth) ]
    for b in range(bitwidth):
        # print(counts[b], nl_len/2)
        hots |= (1 << b) if counts[b] >= nl_len/2 else 0
        nots |= (1 << b) if counts[b] < nl_len/2 else 0
    return hots, nots

def filter_by_condition(orig_list, index, value):
    i = bitwidth - index
    if value == 1:
        return [n for n in orig_list if n & (1 << i) != 0]
    if value == 0:
        return [n for n in orig_list if n & (1 << i) == 0]

def get_hot_bit_at_index(hot_val, index):
    fixed_index = bitwidth - index
    v = hot_val & (1 << fixed_index)
    print(bin(hot_val), bin(v))
    if v != 0:
        return 1
    else:
        return 0

def oxygen(orig_list):
    l = copy.deepcopy(orig_list)
    index = 1
    while len(l) > 1:
        print(f"List: {[bin(n) for n in l]}: {len(l)}")
        hot, _ = get_hot_not_bits(l)
        hot_val = get_hot_bit_at_index(hot, index)
        print(f"Hot val at {index} for {bin(hot)} is {hot_val}")
        l = filter_by_condition(l, index, hot_val)
        index += 1
    print(l)
    return l[0]

def co2(orig_list):
    l = copy.deepcopy(orig_list)
    index = 1
    while len(l) > 1:
        print(f"List: {[bin(n) for n in l]}: {len(l)}")
        _, nott = get_hot_not_bits(l)
        not_val = get_hot_bit_at_index(nott, index)
        print(f"Not val at {index} for {bin(nott)} is {not_val}")
        l = filter_by_condition(l, index, not_val)
        index += 1
    print(l)
    return l[0]

oxy = oxygen(dl)
co2 = co2(dl)
print(f"{oxy * co2}")