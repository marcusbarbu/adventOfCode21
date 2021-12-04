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

bit_width = len(test_data.split()[3])
dl = [int('0b'+line.strip(),0) for line in test_data.split() if len(line) > 2]
inv_counts = [0] * bit_width
for d in dl:
    inv_counts = [inv_counts[i]+1 if (d & (1 << i)) != 0 else inv_counts[i] for i in range(bit_width) ]
    print(f"After adding {bin(d)}, counts: {inv_counts}")
inv_counts = inv_counts[::-1] #inverse bit ordering
hot_bit = int('0b' + ''.join(['1' if inv_counts[i] > len(dl)//2 else '0' for i in range(len(inv_counts))]), 0)
not_bit = int('0b' + ''.join(['0' if inv_counts[i] > len(dl)//2 else '1' for i in range(len(inv_counts))]), 0)
gamma = hot_bit
epsilon = not_bit
print(f"Gamma: {gamma} Epsilon: {epsilon} Power: {gamma * epsilon}")