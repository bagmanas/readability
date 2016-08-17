#! /usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from configparser import ConfigParser
from .NewsParser import NewsParser
from .utils import get_html, url_to_path, writer

if __name__ == '__main__':
    # Configuration
    config = ConfigParser()
    config.read(filenames="readability/config.ini")
    useful_tags = set(config["ParserSettings"]['UsefulTags'].split(","))
    useless_tags = set(config["ParserSettings"]['UselessTags'].split(","))
    len_line = int(config["TextSettings"]['LineMaxLen'])

    # Get url
    cmd_parser = ArgumentParser()
    cmd_parser.add_argument('url')
    url = cmd_parser.parse_args().url

    # Parse and write
    parser = NewsParser(useful_tags, useless_tags)
    parser.feed(get_html(url))
    writer(url_to_path(url), parser.get_text(), width=len_line)
