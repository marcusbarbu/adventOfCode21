class Token:
    def __init__(self, o, close, score, scoreb):
        self.o = o
        self.c = close
        self.score = score
        self.scoreb = scoreb

TOKENS = [Token('<','>',25137, 4), Token('(',')',3, 1), Token('[',']',57, 2), Token('{','}',1197,3)]
OPENS = [t.o for t in TOKENS]
CLOSES = [t.c for t in TOKENS]

OCD = {t.o: t.c for t in TOKENS}
CSD = {t.c: t.score for t in TOKENS}
OSD = {t.o: t.score for t in TOKENS}

CLOSESCORES = {t.c:t.scoreb for t in TOKENS}


print(CSD)

class Line:
    def __init__(self, raw):
        self.raw = raw
    
    def parse_is_incomlete(self):
        stack = []
        for r in self.raw:
            if r in OPENS:
                stack.append(r)
            else:
                test = stack.pop()
                if r != OCD[test]:
                    print(f'First illegal char is {r}')
                    return False, None

        print("Line is legal")
        if len(stack) >0:
            return True, stack
        return False, None

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

def match_stack(stack):
    closers = []
    while len(stack) > 0:
        opener = stack.pop()
        closers.append(OCD[opener])
    return closers
        
def score_stack(closers):
    score = 0
    for c in closers:
        print(score)
        score *= 5
        score += CLOSESCORES[c]
    return score

scores = []
lines = test_data.splitlines()
lines = open('input','r').read().splitlines()
for l in lines:
    ll = Line(l)
    incomplete, stack = ll.parse_is_incomlete()
    if incomplete:
        print(f'Incomplete with stack {stack}')
        closers = match_stack(stack)
        print(f"Closers {closers}")
        scores.append(score_stack(closers))
    print(f'Scores: {scores}')

print(sorted(scores)[len(scores)//2])
