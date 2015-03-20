#!/usr/bin/env python
# encoding: utf-8

import math

class Vector2(object):

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __len__(self):
        return math.sqrt(self.length_squared())

    def __str__(self):
        return '{X=' + str(self.x) + ' Y=' + str(self.y) + '}'

    def length_squared(self):
        return (self.x * self.x + self.y * self.y)
