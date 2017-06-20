# coding: utf-8
import chardet
from urlparse import urlparse
import requests
from bs4 import BeautifulSoup
import traceback
from functools import partial
import tldextract


def encode2utf8(raw_text):
    chardet_result = chardet.detect(raw_text)

    if chardet_result['encoding'] != 'utf-8':
        return raw_text.decode(chardet_result['encoding'], errors='ignore').encode('utf-8')

    return raw_text


def extract_meta(url):
    parser_result = urlparse(url)
    extract_result = tldextract.extract(url)
    meta = {
        'schema': parser_result.scheme,
        'netloc': parser_result.netloc,
        'subdomain': extract_result.subdomain,
        'domain': extract_result.domain,
        'suffix': extract_result.suffix
    }
    return meta


def extract_anchor(anchor, url=None):
    href = anchor.get('href', '')
    if href == '':
        return '', ''

    parse_result = urlparse(href)

    fragment = parse_result.fragment
    href = href.replace('#'+fragment, '')

    href = href.replace('http://', '').replace('https://', '').replace('//', '').strip()
    href = href.rstrip('/')

    if url and href.startswith('/'):
        href = url + href

    if url and href.startswith('../'):
        href = href.replace('..', url)

    title = anchor.get_text().strip()

    return href, title


def filter_anchor(anchor, domain=None):
    href, title = anchor
    if href == ' ' or href == u' ' or href.startswith('javascript') or href == '':
        return False

    if href.startswith('tel:') or href.startswith('mailto:'):
        return False

    if title == ' ' or title == u' ':
        return False

    # filter external urls
    if domain and domain not in href:
        return False

    return True


def extract_urls(url, strict=True, domain=None, netloc=None):
    """A function to extract urls from a given url"""
    try:
        resp = requests.get(url)
        raw_html = encode2utf8(resp.content)
        soup = BeautifulSoup(raw_html, 'html.parser')
        anchors = soup.find_all('a')
        anchors = filter(partial(filter_anchor, domain=domain), map(partial(extract_anchor, url=netloc), anchors))
        return list(set(anchors))
    except Exception as e:
        print traceback.print_exc()
        return None


if __name__ == '__main__':
    url = 'http://www.sina.com.cn'
    urls = extract_urls(url, domain='sina', netloc='www.sina.com.cn')
    for url, title in urls:
        print url, title