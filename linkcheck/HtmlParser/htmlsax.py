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

from HTMLParser import HTMLParser

from ..containers import ListDict


class Parser(HTMLParser, object):
    html_doc = u""
    handler = None
    encoding = "iso8859-1"

    def __init__(self, handler):
        self.handler = handler
        super(Parser, self).__init__()

    def to_dict(self, attrs):
        attrs_dict = ListDict()
        for k, v in attrs:
            if type(k) == str:
                k = k.decode(self.encoding, "ignore")
            if type(v) == str:
                v = v.decode(self.encoding, "ignore")
            attrs_dict[k] = v
        return attrs_dict

    def handle_startendtag(self, tag, attrs):
        print "Encountered a start end tag:", tag, attrs
        self.handler.start_end_element(tag, self.to_dict(attrs))  #, tag.text.strip())

    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag, attrs
        if type(tag) == str:
            tag = tag.decode(self.encoding, "ignore")
        self.handler.start_element(tag, self.to_dict(attrs))  #, tag.text.strip())

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag
        if hasattr(self.handler, 'end_element'):
            self.handler.end_element(tag)

    def handle_data(self, data):
        print "Encountered some data  :", data
        if hasattr(self.handler, 'characters'):
            if type(data) == str:
                data = data.decode(self.encoding, "ignore")
            self.handler.characters(data)

    def flush(self):
        pass

    def get_lineno(self):
        return self.lineno

    def last_lineno(self):
        return 1  # self.last_lineno

    def column(self):
        return 1  # self.column

    def last_column(self):
        return 1  # self.last_column

    def pos(self, text):
        return 1  # self.pos

    def peek(self, peek_len):
        return self.rawdata[:peek_len]

    def handle_comment(self, data):
        print "Comment  :", data
        if hasattr(self.handler, 'comment'):
            self.handler.comment(data)

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c

    def handle_decl(self, data):
        print "Decl     :", data
        if hasattr(self.handler, 'doctype'):
            self.handler.doctype(data[7:])

    def handle_pi(self, data):
        print "Pi     :", data
        if hasattr(self.handler, 'pi'):
            self.handler.pi(data)


def parser(handler = None):
    return Parser(handler)
