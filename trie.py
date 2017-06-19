# coding: utf-8
from collections import deque

class TrieNode(object):

    def __init__(self, value=None, level=0, path=None):
        self.data = {}
        self.is_doc = False
        self.level = level
        self.path = path
        self.value = value


class TrieTree(object):

    def __init__(self):
        self.root = TrieNode('root')

    def insert(self, path):
        node = self.root
        
        steps = path.split('/')
        for level, step in enumerate(steps):
            child = node.data.get(step)
            if not child:
                node.data[step] = TrieNode(step, level=level+1)
            node = node.data.get(step)

        node.path = path
        node.is_doc = True

    def dft(self):
        """Depth-First traverse"""
        node = self.root
        stack = []
        stack.append(node)
        
        while True:
            if len(stack) == 0:
                break

            node = stack.pop()

            yield node

            for step, child in node.data.iteritems():
                stack.append(child)  

    def bft(self):
        """Breadth-First traverse"""
        node = self.root
        queue = deque()
        queue.appendleft(('root',node))
        
        while True:
            if len(queue) == 0:
                break

            value, node = queue.popleft()
            
            yield node.level, value, node.path

            for step, child in node.data.iteritems():
                queue.append((step,child))

    def aggregate_by_level(self):
        """"""
        data = {}
        for node in self.dft():
            level = node.level
            path = node.path
            if level not in data:
                data[level] = {
                    'num': 0,
                    'nodes': []
                }
            if path:
                data[level]['num'] += 1
                data[level]['nodes'].append(path)
        return data
            

    def print_tree(self):
        """print trie tree"""
        for node in self.dft():
            if node.level == 0:
                print node.value, node.path
            else:
                print ' ' * (node.level * 2), node.value, node.path

if __name__ == '__main__':
    trie = TrieTree()
    trie.insert('a/b/c')
    trie.insert('a/b/d')
    trie.insert('a/c/e/f')
    trie.insert('a/c/e/g')
    trie.print_tree()
    data = trie.aggregate_by_level()
    for level, value in data.iteritems():
        print level, value['num']
