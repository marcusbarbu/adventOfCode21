from collections import defaultdict
test_input = '''
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''

def parse(data):
    output = []
    lines = data.splitlines()
    for l in lines:
        if len(l) > 1:
            uniques = l.split('|')[0].split()
            chal = l.split('|')[1].split()
            output.append((uniques, chal))
    return output

dl = parse(test_input)
dl = parse(open('input', 'r').read())

class SevenSeg:
    LEN_MAP = {2:1, 3:7, 4:4, 5:(2, 3, 5), 6:(6,9,0), 7:8}

    def __init__(self, cal_vals, uniques):
        self.uniques = uniques
        self.cal_vals = cal_vals
        self.segment_dict = {}
        self.cal_dict = defaultdict(list)
        self.lookup_dict = {}
        self.initial_fix()
    
    def initial_fix(self):
        for seq in self.cal_vals:
            if len(seq) in SevenSeg.LEN_MAP.keys():
                self.cal_dict[SevenSeg.LEN_MAP[len(seq)]].append(seq)
        self.six_nine_zero()
        self.two_three_five()

    def six_nine_zero(self):
        options = self.cal_dict[(6,9,0)]

        four_seq = self.cal_dict[(4)][0]
        seven_seq = self.cal_dict[(7)][0]
        eight_seq = self.cal_dict[(8)][0]
        one = self.cal_dict[1][0]

        for o in options:
            for c in seven_seq:
                if c not in o:
                    # self.segment_dict['a'] = c
                    # print(f'Found segment a: {c}')
                    self.cal_dict[6] = o
                    break
        options.pop(options.index(self.cal_dict[6]))

        for o in options:
            for c in eight_seq:
                if c not in o and c in four_seq:
                    self.segment_dict['g'] = c
                    self.cal_dict[0] = o
                    print(f'we think seg is {c} val is {o}')
                    # break
        options.pop(options.index(self.cal_dict[0]))




        print(options)
        self.cal_dict[9] = options[0]
        del(self.cal_dict[(6,9,0)])

        for c in self.cal_dict[9]:
            if c not in self.cal_dict[6] and c in one:
                self.segment_dict['a'] = c

        b = one.replace(self.segment_dict['a'], '')
        self.segment_dict['b'] = b
    
    def two_three_five(self):
        options = self.cal_dict[(2,3,5)]
        a_char = self.segment_dict['a']
        for o in options:
            print(o)
            if a_char not in o:
                print(f'Found 5: {o}')
                self.cal_dict[5] = o
                break
            else:
                print(f'{a_char} in {o}')
                pass
        options.pop(options.index(self.cal_dict[5]))
        for o in options:
            if self.segment_dict['b'] not in o:
                # print(f'Found 2: {o}')
                self.cal_dict[2] = o
                break
        options.pop(options.index(self.cal_dict[2]))
        self.cal_dict[3] = options[0]
        del(self.cal_dict[(2,3,5)])
    
    def lookup_unique(self, u):
        for k, v in self.cal_dict.items():
            if isinstance(v, list):
                val = set(v[0])
            else:
                val = set(v)
            us = set(u)
            if us == val:
                print(f'found num {k}')
                return str(k)
    
    
    def calc_val(self):
        nums = []
        for u in self.uniques:
            nums.append(self.lookup_unique(u))
        return int(''.join(nums))

    
total = 0
for d in dl:
    print(f'Testing {d[0]}')
    ssd = SevenSeg(*d)
    val = ssd.calc_val()
    print(f'Single score {val}')
    total += val

print(f'Total: {total}')