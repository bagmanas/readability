#! /usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
from html.parser import HTMLParser


class NewsParser(HTMLParser):
    def __init__(self, useful_tags=None, useless_tags=None):
        self.useful_tags = useful_tags or set()
        self.useless_tags = useless_tags or set()
        self.stack_tag = deque()
        self.text = []
        self.current_attrs = {}
        self.curr_paragraph = ""
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.current_attrs = dict(attrs)
        self.stack_tag.append(tag)

    def handle_endtag(self, tag):
        while self.stack_tag and tag != self.stack_tag.pop():
            continue
        if tag in self.useful_tags:
            self.text.append(self.curr_paragraph)
            self.curr_paragraph = ""

    def handle_data(self, data):
        if not self.stack_tag:
            return

        if any(map(lambda x: x in self.stack_tag, self.useless_tags)):
            return

        if self.stack_tag[-1] == 'a':
            if any(map(lambda x: x in self.stack_tag, self.useful_tags)):
                link = "{}[{}]".format(data, self.current_attrs['href'])
                self.curr_paragraph += link

        if self.stack_tag[-1] in self.useful_tags:
            self.curr_paragraph += data

    def get_text(self):
        return "\n".join(filter(None, self.text))

    def error(self, message):
        pass
