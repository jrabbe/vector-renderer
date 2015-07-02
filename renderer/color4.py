#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

def create(r, g, b, a=1.0):
    return Color(r, g, b, a)

def average(*values):
    count = 0
    total = Color(0, 0, 0, 0)

    for value in values:
        if value is not None:
            total += value

        count += 1

    if count > 0:
        return total.scale(1 / count, scale_alpha=True)

    return total

class Color(object):

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

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b, self.a + other.a)

    def __sub__(self, other):
        return Color(self.r - other.r, self.g - other.g, self.b - other.b, self.a - other.a)

    def get(self, attr, min_value=0.0, max_value=1.0, format=float):
        value = self.__getattribute__(attr)
        return format(value * (max_value - min_value) + min_value)

    def clone(self):
        return Color(self.r, self.g, self.b, self.a)

    def scale(self, factor, scale_alpha=False):
        color = self.clone()
        color.r *= factor
        color.g *= factor
        color.b *= factor

        if scale_alpha:
            color.a *= factor

        return color

    def values(self):
        return (self.r, self.g, self.b, self.a)
