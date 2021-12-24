from collections import defaultdict
from dataclasses import dataclass, Field
from typing import List, Optional, Tuple, Type
import math

test_input=open('test_input','r').read()

class Delta:
    def __init__(self, coord_a, coord_b):
        self.a = coord_a
        self.b = coord_b
        self.rel_diffs = []
        self.distance = 0
        self.calculate()

    def calculate(self):
        self.rel_diffs = [i - j for i, j in zip(self.a, self.b)]
        self.distance = math.sqrt(sum([v**2 for v in self.rel_diffs]))
    
    def __repr__(self) -> str:
        return f"Diff {self.a.label}->{self.b.label}: {self.rel_diffs} |{self.distance}|"

class Coord:
    INDEX_LIST = ['x','y','z']
    def __init__(self, x, y, z, label='', index=0):
        self.x = x
        self.y = y
        self.z = z
        self.single_distance = math.sqrt(x**2 + y**2 + z**2)
        self.label = label
        self.index = index

    def __getitem__(self, key):
        # return self.list[key] 
        return getattr(self, Coord.INDEX_LIST[key])

    def __setitem__(self, key, val):
        return setattr(self, Coord.INDEX_LIST[key], val)

    def __repr__(self) -> str:
        # return f'Coord {self.index} {self.label}: {self.x}, {self.y}, {self.z}'
        return f'{self.x}, {self.y}, {self.z}'
    
    def get_sequence(self):
        vec = [self.x, self.y, self.z]
        def roll(v):
            return [v[0],v[2],-v[1]]
        def turn(v):
            return [-v[1],v[0],v[2]]
        for i in range(2):
            for s in range(3):
                vec = roll(vec)
                yield vec
                for z in range(3):
                    vec = turn(vec)
                    yield(vec)
            vec = roll(turn(roll(vec)))
    
    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y and self.z == o.z
    
class Scanner:
    def __init__(self, index=0, is_root=False):
        self.scanner_id = index
        self.coords = []
        self.is_root = is_root
        self.deltas = []
        self.delta_set = set()
        self.raw_deltas = []
        self.root_location = Coord(0,0,0,"Scanner {} root".format(index))
    
    def add_coord(self, coord):
        coord.label = coord.label + 'S{}::{}'.format(self.scanner_id, len(self.coords))
        coord.index = len(self.coords)
        self.coords.append(coord)
        self.deltas.append([coord, set()])
        self.raw_deltas.append([coord, set()])

    def __repr__(self) -> str:
        output = []
        output.append(f'Scanner {self.scanner_id} @ {self.root_location}')
        for c in self.coords:
            output.append('\t' + str(c))
        return '\n'.join(output)
    
    def set_scanner_position(self, coord):
        self.root_location = coord
        # print(f'Setting scanner {self.scanner_id} position to {self.root_location}')
        for ci in range(len(self.coords)):
            c = self.coords[ci]
            c.x += coord.x
            c.y += coord.y
            c.z += coord.z
            self.coords[ci] = c
    
    def set_rotation_index(self, ri):
        for ci in range(len(self.coords)):
            c = self.coords[ci]
            new_c = Coord(*list(c.get_sequence())[ri], label=c.label)
            self.coords[ci] = new_c
    
    def get_delta_list_index(self, coord: Type[Coord]) -> List:
        for i, (c, l) in enumerate(self.deltas):
            if c == coord:
                return i
    
    def calculate_deltas(self):
        self.deltas = []
        self.delta_set = set()
        self.raw_deltas = []
        for c in self.coords:
            self.deltas.append([c, set()])
            self.raw_deltas.append([c, set()])
        for c1 in self.coords:
            for c2 in self.coords:
                if c1 == c2:
                    continue
                i = c1.index
                j = c2.index
                d = Delta(c1, c2)
                self.deltas[self.get_delta_list_index(c1)][1].add(d)
                self.raw_deltas[self.get_delta_list_index(c1)][1].add(d.distance)
                self.delta_set.add(d)
    
    def merge_scanner(self, scanner):
        # print(f'Merging with scanner: {scanner}')
        for c in scanner.coords:
            if c not in self.coords:
                self.add_coord(c)
            else:
                # print('duplicate!')
                pass

def parse(str_in) -> List[Type[Scanner]]:
    out = []
    original_len = 0
    cur_scanner_id = 0
    scanner = None
    for l in str_in.splitlines():
        if len(l) == 0:
            continue
        if "scanner" in l:
            if scanner is not None:
                out.append(scanner)
            s = l.split('scanner')[-1].strip().split()[0]
            cur_scanner_id = int(s)
            # print(f'Cur is {cur_scanner_id}')
            scanner = Scanner(index=cur_scanner_id, is_root=(cur_scanner_id == 0))
        else:
            vals = [int(x) for x in l.strip().split(',') if len(x) > 0]
            c = Coord(*vals)
            scanner.add_coord(c)
            original_len += 1
    if scanner is not None:
        out.append(scanner)
    return out, original_len

scanners, original_len = parse(test_input)
scanners, original_len = parse(open('input','r').read())

for s in scanners:
    s.calculate_deltas()
    # print(s)

target_scanners = scanners[1:]
base_scanner = scanners[0]

MATCH_TARGET = 10

while target_scanners:
    print(f'{len(target_scanners)} Scanners remaining')
    current_scanner_id = 0
    match = False
    for scanner in target_scanners:
        matches = []
        for coord, raw_deltas in scanner.raw_deltas:
            for base_coord, known_deltas in base_scanner.raw_deltas:
                if len(raw_deltas.intersection(known_deltas)) >= MATCH_TARGET:
                    # print(f'{coord} matches {base_coord}')
                    matches.append((coord, base_coord))
        if len(matches) >= 2:
            a = matches[0]
            b = matches[1]
            a_target, a_known = a
            b_target, b_known = b
            delta_target = Coord(*Delta(a_target, b_target).rel_diffs)
            delta_known = Coord(*Delta(a_known, b_known).rel_diffs)
            for rotation_index, rotate_delta_delta_target in enumerate(delta_target.get_sequence()):
                rdtc = Coord(*rotate_delta_delta_target) 
                if rdtc == delta_known:
                    match = True
                    new_a_target = None
                    new_a_target = list(a_target.get_sequence())[rotation_index]
                    new_a_target = Coord(*new_a_target)
                    # rel_delta = Delta(a_target, new_a_target) 
                    rel_delta = Delta(a_known, new_a_target)
                    # print(f'A -> rot(a) {a_target} -> {new_a_target}')
                    # print(f'D -> rot(d) {delta_target} -> {rotate_delta_delta_target}')
                    # print(f'Scanner {scanner.scanner_id} must be at {rel_delta}')
                    # print("Coords before: ")
                    # for c in scanner.coords:
                    #     print('\t {}'.format(c))
                    scanner.set_rotation_index(rotation_index)
                    scanner.set_scanner_position(Coord(*rel_delta.rel_diffs))
                    scanner.calculate_deltas()
                    # print("Coords after: ")
                    # for c in scanner.coords:
                    #     print('\t {}'.format(c))
                    base_scanner.merge_scanner(scanner)
                    break
            else:
                # print(f"{rotation_index} rotations wasn't enough")
                pass
            break
    if match:
        target_scanners.pop(target_scanners.index(scanner))
        base_scanner.calculate_deltas()


base_scanner_coord_set = set([tuple(list(c)) for c in base_scanner.coords])
print(f'Original {original_len}')
print(f'Part 1: {len(base_scanner.coords)}')
print(f'Part 1: {len(base_scanner_coord_set)}')
