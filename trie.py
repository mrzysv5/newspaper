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
        self._max_level_num = -1
        self._min_level_num = -1
        self._max_url_num = -1
        self._min_url_num = -1

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
        stack = [self.root]
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
        max_level_num = 0
        min_level_num = 1
        max_url_num = 0
        min_url_num = 1

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

            num = data[level]['num']
            print num
            if level > max_level_num:
                max_level_num = level

            if num > max_url_num:
                max_url_num = num

        self._max_level_num = max_level_num
        self._min_level_num = min_level_num
        self._max_url_num = max_url_num
        self._min_url_num = min_url_num

        return data

    def calculate(self):
        """"""
        level_data = self.aggregate_by_level()
        max_level_num = self._max_level_num
        min_level_num = self._min_level_num
        max_url_num = self._max_url_num
        min_url_num = self._min_url_num

        print max_level_num, min_level_num
        print max_url_num, min_url_num

        def format2standard(level, num):
            l = (level - min_level_num) / float(max_level_num - min_level_num)
            p = (num - min_url_num ) / float(max_url_num - min_url_num)
            return l * p

        for level, value in level_data.iteritems():
            level_data[level]['p'] = format2standard(level, value['num'])

        import codecs
        import json
        with codecs.open('sina', 'w') as f:
            f.write(json.dumps(level_data, ensure_ascii=False))

    def categories(self):
        pass


    def print_tree(self):
        """print trie tree"""
        for node in self.dft():
            if node.level == 0:
                print node.value, node.path
            else:
                print ' ' * (node.level * 2), node.value, node.path

    def print_html(self, data=None):
        stack = []
        cur_level = -1
        stack_html = []

        for node in self.dft():
            level = node.level
            path = node.path if node.path else 'empty'
            if data:
                title = data[path] if node.path else 'empty'
            if level > cur_level:
                if data:
                    stack.append('<ul><li><a href="http://%s" target="_blank">%s' % (path, title))
                    stack_html.append((level, '</a></li></ul>'))
                else:
                    stack.append('<ul><li>%s' % (node.path))
                    stack_html.append((level, '</li></ul>'))
            elif level == cur_level:
                if data:
                    stack.append('<li><a href="http://%s" target="_blank">%s' % (path, title))
                    stack_html.append((level, '</a></li>'))
                else:
                    stack.append('<li>' + node.path)
                    stack_html.append((level, '</li>'))
            else:
                while True:
                    if len(stack_html) == 0:
                        break
                    l, html = stack_html.pop()
                    if l + 1 == level:
                        stack_html.append((l, html))
                        break
                    stack.append(html)
                if data:
                    stack.append('<ul><li><a href="http://%s" target="_blank">%s' % (path, title))
                    stack_html.append((level, '</a></li></ul>'))
                else:
                    stack.append('<ul><li>' + node.path)
                    stack_html.append((level, '</li></ul>'))
            cur_level = level
        while len(stack_html):
            _, html = stack_html.pop()
            stack.append(html)

        print ''.join(stack)


if __name__ == '__main__':
    trie = TrieTree()
    trie.insert('a/b/c')
    trie.insert('a/b/d')
    trie.insert('a/c/e/f')
    trie.insert('a/c/e/g')
    print trie.print_html()