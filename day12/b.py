import copy
test_input = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''

tib = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''

tic = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''

class Cave:
    def __init__(self, name: str):
        self.name = name
        self.start = (name == "start")
        self.end = (name == "end")
        self.big = (name.upper() == name) and not (self.start or self.end)
        self.small = not self.big and not (self.start or self.end)
        self.neighbors = []
    
    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
    
    def __repr__(self):
        return f'Cave {self.name} with neighbors {[n.name for n in self.neighbors]}'


class CaveGraph:
    def __init__(self, raw: str):
        self.raw = raw
        self.caves = {}
        self.parse()
        self.start = self.caves['start']
        self.end = self.caves['end']
    
    def parse(self):
        lines = self.raw.splitlines()
        for l in lines:
            a, b = l.split('-')[:2]
            if a not in self.caves.keys():
                acave = Cave(a)
                self.caves[a] = acave
            acave = self.caves[a]
            if b not in self.caves.keys():
                bcave = Cave(b)
                self.caves[b] = bcave
            bcave = self.caves[b]
            acave.add_neighbor(bcave)
            bcave.add_neighbor(acave)

    def __repr__(self):
        nlt = '\n\t'
        return f'CaveGraph with nodes: {nlt}{nlt.join([str(n) for n in self.caves.values()])}'
    

    def traverse(self, node=None, traversed=set(), double_traversed=False):
        count = 0
        paths = []
        if node is None:
            node = self.start
        if node == self.end:
            return 1, [[node]]
        
        for neighbor in node.neighbors:
            if neighbor.small and neighbor in traversed and double_traversed or neighbor == self.start:
                continue
            elif neighbor.small and neighbor in traversed and not double_traversed and neighbor != self.start:
                nc, np = self.traverse(neighbor, {*traversed | set([node, neighbor])}, True)
                count += nc
                for n in np:
                    paths.append([node] + n)
            else:
                nc, np = self.traverse(neighbor, {*traversed | set([node, neighbor])}, double_traversed)
                count += nc
                for n in np:
                    paths.append([node] + n)
        return count, paths




    
cg = CaveGraph(test_input)
cg = CaveGraph(tib)
cg = CaveGraph(tic)
cg = CaveGraph(open('input','r').read())
print(cg)

print("PATHS::::")
count, paths = cg.traverse()
for p in paths:
    print(','.join([c.name for c in p]))
print(f'Total Count {count}')