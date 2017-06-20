# coding: utf-8
from trie import TrieTree
from utils import extract_urls, extract_meta


class NewsPaper(object):

    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.trie = TrieTree()
        self.mapper = {}
        self.meta = {}

        self._init()

    @property
    def categories(self):
        pass

    def _init(self):
        self.meta = extract_meta(self.url)
        for url, title in extract_urls(self.url, domain=self.meta['domain'], netloc=self.meta['netloc']):
            self.trie.insert(url)
            if url not in self.mapper:
                self.mapper[url] = title


def sina():
    newspaper = NewsPaper('http://www.sina.com.cn', title=u'新浪网')
    html = newspaper.trie.print_html(newspaper.mapper)
    print html


if __name__ == '__main__':
    sina()