class Token:
    def __init__(self, o, close, score):
        self.o = o
        self.c = close
        self.score = score

TOKENS = [Token('<','>',25137), Token('(',')',3), Token('[',']',57), Token('{','}',1197)]
OPENS = [t.o for t in TOKENS]
CLOSES = [t.c for t in TOKENS]

OCD = {t.o: t.c for t in TOKENS}
CSD = {t.c: t.score for t in TOKENS}
OSD = {t.o: t.score for t in TOKENS}

print(CSD)

class Line:
    def __init__(self, raw):
        self.raw = raw
    
    def parse(self):
        stack = []
        for r in self.raw:
            if r in OPENS:
                stack.append(r)
            else:
                test = stack.pop()
                if r != OCD[test]:
                    print(f'First illegal char is {r}')
                    return CSD[r]

        print("Line is legal")
        return 0

test_data = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''

score = 0

lines = test_data.splitlines()
lines = open('input','r').read().splitlines()
for l in lines:
    ll = Line(l)
    score += ll.parse()
    print(f'Present score: {score}')

print(f'Final score: {score}')