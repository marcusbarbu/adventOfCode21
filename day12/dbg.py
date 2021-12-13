example='''start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end'''

mine = '''start,A,c,A,c,A,b,A,b,A,end
start,A,c,A,c,A,b,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,d,b,A,end
start,A,c,A,c,A,b,d,b,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,b,A,c,A,b,A,end
start,A,c,A,b,A,c,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,b,A,c,A,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,c,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,end
start,A,b,A,c,A,c,A,b,A,end
start,A,b,A,c,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,b,A,c,A,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,end
start,A,b,A,b,A,c,A,c,A,end
start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,end
start,A,b,d,b,A,c,A,c,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,end
start,b,A,c,A,c,A,b,A,end
start,b,A,c,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,b,A,c,A,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,end
start,b,A,b,A,c,A,c,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,end
start,b,d,b,A,c,A,c,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end
'''


ex_lines = set(example.splitlines())
mine_lines = set(mine.splitlines())

diff = mine_lines.difference(ex_lines)

for d in diff:
    print(d)