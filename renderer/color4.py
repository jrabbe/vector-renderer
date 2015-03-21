#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

class Color4(object):

    def __init__(self, r, g, b, a=1.0):
        """
        Initialize a color instance from its component. Each component is given in the range
        of 0.0 to 1.0.

        Keyword arguments:
        r -- the red component
        g -- the green component
        b -- the blue component
        a -- the alpha component (default 1.0)
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return '[R={} G={} B={} A={}]'.format(self.r, self.g, self.b, self.a)

    def get(self, attr, min_value=0.0, max_value=1.0, format=float):
        value = self.__getattribute__(attr)
        return format(value * (max_value - min_value) + min_value)
