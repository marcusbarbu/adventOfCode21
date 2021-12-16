from os import POSIX_FADV_RANDOM


test_data = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''

btest = '''1911191111
1119111991
9999999111
9999911199
9999119999
9999199999
9111199999
9199999111
9111911191
9991119991
'''


class ChitonCave:
    def __init__(self, raw):
        self.raw = raw
        self.rows = [[int(x) for x in l] for l in raw.splitlines()]
        self.max_row = len(self.rows)
        self.max_col = len(self.rows[0])
    
    def get_neighbors(self, row, col):
        options = []
        for i in range(-1, 2):
            nr = row + i
            nc = col + i
            if nr in range(0, self.max_row) and (nr, col) != (row, col):
                options.append((nr, col))
            if nc in range(0, self.max_col) and (row, nc) != (row, col):
                options.append((row, nc))
        # print(f'Options for {row},{col}: {options}')
        return options
    
    def dijkstra(self):
        start = (0, 0)
        distances = {}
        prev = {}
        nodes = set()
        for row in range(len(self.rows)):
            for col in range(len(self.rows[row])):
                pos = (row, col)
                distances[pos] = 123123123123
                prev[pos] = None
                nodes.add(pos)
        distances[start] = 0
        nodes.add(start)

        while len(nodes) > 0:
            for cur, val in sorted(list(distances.items()), key= lambda x: x[1]):
                if cur in nodes:
                    break
            else:
                # print(f'Did i remember how to for else? {cur}')
                pass
            nodes.remove(cur)
            print(f'Current node addr {cur}. Unvisited: {len(nodes)}')
            neighbors = self.get_neighbors(cur[0],cur[1])
            for n in neighbors:
                if n not in nodes:
                    continue
                ndist = distances[cur] + self.rows[cur[0]][cur[1]]
                if ndist < distances[n]:
                    distances[n] = ndist
                    prev[n] = cur
        return distances, prev
    
    def find_path_score(self, distances, prevs):
        cur = (self.max_row - 1, self.max_col - 1)
        path = [cur]
        score = distances[cur]
        while cur != (0,0):
            # print(f'{cur}->')
            cur = prevs[cur]
            path.append(cur)
        # print(f'{cur}')
        return path, score

    def print_path(self, path):
        rows = []
        for r in range(len(self.rows)):
            row = []
            for c in range(len(self.rows[r])):
                if (r, c) in path:
                    row.append(str(self.rows[r][c]))
                else:
                    row.append('.')
            rows.append(''.join(row))
        print('\n'.join(rows))
        
    def secondary_calc(self, path):
        score = 0
        for r,c in path[:-1]:
            score += self.rows[r][c]
        return score


cc = ChitonCave(test_data)
cc = ChitonCave(open('input','r').read())
# cc = ChitonCave(btest)
fn = cc.get_neighbors(0,0)
dists, prevs = cc.dijkstra()
path, score = cc.find_path_score(dists, prevs)
cc.print_path(path)
print(f'Final score: {score}')
print(f'Secondary calc: {cc.secondary_calc(path)}')