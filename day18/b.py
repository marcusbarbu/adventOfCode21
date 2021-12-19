import math
from dataclasses import dataclass, field
from typing import Any, Optional
from ppbtree import *

def pt(node):
    return print_tree(node, nameattr='label', left_child='left', right_child='right')

@dataclass
class Node:
    label: str
    rawlist: Optional[Any] = None
    val: Optional[int] = 0
    isleaf: Optional[bool] = False
    left: Optional[Any] = None
    right: Optional[Any] = None
    parent: Optional[Any] = None

    def __repr__(self) -> str:
        return f'{self.val}' if self.isleaf else f'[{self.left},{self.right}]'
    
    def is_pair(self):
        return (self.left is not None) and (self.right is not None) and self.left.isleaf and self.right.isleaf

class SnailTree:
    def __init__(self, linestr, label=''):
        self.raw = linestr
        self.root = Node(rawlist=eval(self.raw), isleaf=False, parent=None, label="root{}".format(label))
        self.parse_node()
    
    def add(self, r_root):
        left = self.root
        right = r_root.root
        self.root = Node(isleaf=False, parent=None, label='root')
        left.parent = self.root
        right.parent = self.root
        self.root.left = left
        self.root.right = right

    def parse_node(self, root=None):
        if root is None:
            root = self.root
        if not root.isleaf and (root.left is None and root.right is None):
            line = root.rawlist
            if isinstance(line, int):
                root.val = line
                root.isleaf = True
                root.label = str(root.val)
            elif isinstance(line, list):
                root.val = None
                root.isleaf = False
                root.left = Node(rawlist=line[0], parent=root, label="l")
                root.right = Node(rawlist=line[1], parent=root, label='r')
        if root.left is not None:
            self.parse_node(root=root.left)
        if root.right is not None:
            self.parse_node(root=root.right)
    
    def find_next_left_leaf(self, node):
        current = node
        if current == self.root:
            return None
        if not current:
            return None
        parent = node.parent
        if parent.left is not None and node is not parent.left: #easieset case, node is in the same chain
            if parent.left.isleaf:
                return parent.left
            else: #walk the neighboring node down the right hand side
                parent = parent.left
                current = parent.right
                while current:
                    if current.isleaf:
                        return current
                    current = current.right
        else:
            return self.find_next_left_leaf(parent)

    def find_next_right_leaf(self, node):
        current = node
        if current == self.root:
            return None
        if not current:
            return None
        parent = node.parent
        if parent.right is not None and node is not parent.right: #easieset case, node is in the same chain
            if parent.right.isleaf:
                return parent.right
            else: #walk the neighboring node down the left hand side
                parent = parent.right
                current = parent.left
                while current:
                    if current.isleaf:
                        return current
                    current = current.left
        else:
            return self.find_next_right_leaf(parent)

        
    def find_explosions_once(self, node=None, depth=0):
        if node is None:
            node = self.root

        if node.left is not None:
            if self.find_explosions_once(node.left, depth+1):
                return True

        if depth >= 4 and node.is_pair(): # if we're a pair at depth 4 or greater

            left_leaf = self.find_next_left_leaf(node)
            right_leaf = self.find_next_right_leaf(node)

            if left_leaf:
                left_leaf.val += node.left.val
                left_leaf.label = str(left_leaf.val)
            if right_leaf:
                right_leaf.val += node.right.val
                right_leaf.label = str(right_leaf.val)

            # turn this node into a 0 leaf
            node.isleaf = True
            node.val = 0
            node.label = '0'
            node.right = None
            node.left = None

            return True
        if node.right is not None:
            if self.find_explosions_once(node.right, depth+1):
                return True
        return False
    
    def find_splits_once(self, node=None):
        if node is None:
            node = self.root
        if node.isleaf and node.val >= 10:
            lval = math.floor(node.val / 2)
            rval = math.ceil(node.val / 2)
            node.isleaf = False
            node.label = f'was{node.val}'
            node.val = 0
            node.left = Node(rawlist=lval, label=str(lval), isleaf=True, val=lval, parent=node)
            node.right = Node(rawlist=rval, label=str(rval), isleaf=True, val=rval, parent=node)
            return True
        if node.left is not None:
            if self.find_splits_once(node.left):
                return True
        if node.right is not None:
            if self.find_splits_once(node.right):
                return True
        return False
    
    def find_all_reductions(self, dbg=False):
        # pt(self.root)
        i = 0
        exploded = False
        split = False
        running = True
        while running:
            exploded = self.find_explosions_once()
            if exploded:
                if dbg:
                    print(f"exploded: {self.root}")
            if not exploded:
                split = self.find_splits_once()
                if dbg:
                    print(f"splitted: {self.root}")
            running = exploded or split
            if dbg:
                pt(self.root)

    def get_magnitude(self, node=None):
        if node is None:
            node = self.root
        if node.isleaf:
            return node.val
        total = 0
        if node.left:
            total += 3 * self.get_magnitude(node.left)
        if node.right:
            total += 2 * self.get_magnitude(node.right)
        return total

test_input = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

lines = test_input.splitlines()
lines = open('input','r').read().splitlines()
root = SnailTree(lines[0], label='orig')


mags = []
for a in lines:
    for b in lines:
        a_tree = SnailTree(a, label='a')
        b_tree = SnailTree(b, label='b')
        a_tree.add(b_tree)
        a_tree.find_all_reductions()
        mags.append(a_tree.get_magnitude())

print(max(mags))