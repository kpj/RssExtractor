import os
import html, json
import urllib.request

import feedparser
from feedgen.feed import FeedGenerator

from bs4 import BeautifulSoup


class Feed(object):
    def __init__(self, url):
        self.obj = feedparser.parse(url)
        self.cache_fname = 'cache.json'

    def _retrieve_url(self, url):
        """ Url request with caching
        """
        if os.path.exists(self.cache_fname):
            with open(self.cache_fname) as fd:
                cache = json.load(fd)
        else:
            cache = {}

        if url in cache:
            return cache[url]

        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page, 'lxml')
        body = soup.find('body')
        text = str(body)

        cache[url] = text
        with open(self.cache_fname, 'w') as fd:
            json.dump(cache, fd)

        return text

    def _get_content(self, entry):
        if 'content' in entry:
            assert len(entry.content) == 1
            body = entry.content[0].value
            return html.unescape(body)
        else:
            return self._retrieve_url(entry.link)

    def get_feed(self):
        fg = FeedGenerator()

        fg.title(self.obj.feed.title)
        fg.link(href=self.obj.feed.link, rel='alternate')
        fg.description(self.obj.feed.subtitle)

        for e in self.obj.entries[:4]:
            fe = fg.add_entry()

            fe.id(e.link)
            fe.title(e.title)
            fe.description(self._get_content(e))

        return fg.rss_str()
