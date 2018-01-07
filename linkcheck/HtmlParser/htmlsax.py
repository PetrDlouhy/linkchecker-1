# -*- coding: utf8 -*-
# Copyright (C) 2000-2018 Petr Dlouhy
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
Replacement for the built-in Html parser
"""

from bs4 import BeautifulSoup

from ..containers import ListDict


class Parser(object):
    html_doc = u""
    handler = None
    encoding = "iso8859-1"

    def __init__(self, handler):
        self.handler = handler

    def feed(self, feed_text):
        if type(feed_text) == bytes:
            feed_text = feed_text.decode(self.encoding)
        self.html_doc += feed_text

    def reset(self):
        self.html_doc = u""

    def flush(self):
        soup = BeautifulSoup(self.html_doc, 'html.parser')
        for tag in soup.find_all():
            attrs = ListDict()
            for k, v_list in tag.attrs.items():
                if type(v_list) != list:
                    v_list = [v_list]
                for v in v_list:
                    if type(v) == str:
                        v = v.decode(self.encoding, "ignore")
                    attrs[k] = v
            self.handler.start_element(tag.name, attrs, tag.text.strip())
            if hasattr(self.handler, 'characters'):
                self.handler.characters(tag.text)
            if (not tag.is_empty_element and
                hasattr(self.handler, 'end_element')):
                self.handler.end_element(tag.name)
            if tag.comments:
                for comment in tag.comments:
                    self.handler.comment(comment)

    def debug(self, text):
        raise NotImplementedError("number is not implemented")

    def lineno(self):
        return 0  # It seems, that getting line number of element is not implemented in BeatifulSoup, so this is faked

    def last_lineno(self):
        return 0

    def column(self):
        return 0

    def last_column(self):
        return 0

    def pos(self, text):
        return 0

    def peek(self, peek_len):
        raise NotImplementedError("Peeking is deprecated in favor of 'handler.start_element' attribute 'element_text'")


def parser(handler = None):
    return Parser(handler)
