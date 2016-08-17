#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import textwrap
from contextlib import closing
from urllib.parse import urlparse


def get_html(url):
    with closing(requests.get(url)) as page:
        return page.text


def writer(path, text, width=80, charset='cp1251'):
    directory, file = path.rsplit("/", 1)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, "w", encoding=charset) as f:
        gen = (line.strip() for line in text.splitlines() if line.strip())
        lines = (textwrap.fill(line, width=width) for line in gen)
        f.write("\n\n".join(lines))


def url_to_path(url, root="."):
    o = urlparse(url)
    path, _, file = o.path.strip('/').rpartition('/')
    if file.endswith(('.html', '.php', '.shtml')):
        file, _, _ = file.rpartition('.')
    return "{}/{}/{}/{}.txt".format(root, o.netloc, path, file)
