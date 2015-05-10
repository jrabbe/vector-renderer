#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

class Segment(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return ((self.a == other.a and self.b == other.b)
            or (self.b == other.a and self.a == other.b))

    def __str__(self):
        return 'Segment[a={} b={}]'.format(self.a, self.b)

    def vertices(self):
        return [self.a, self.b]
