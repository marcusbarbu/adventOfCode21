repls = {'forward':'horiz += (', 'down': 'depth += (', 'up': 'depth -= ('}
horiz = 0
depth = 0
with open('input','r') as infile:
    for line in infile.readlines():
        if len(line) > 2:
            line = line.strip()
            line += ')'
            for find, repl in repls.items():
                line = line.replace(find, repl)
            exec(line)
print(f"Horizontal: {horiz}, Depth: {depth}, Product: {horiz*depth}")