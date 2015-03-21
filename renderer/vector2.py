#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import math

def normalize(vector):
    return vector.clone().normalize()

def transform(vector, transformation):
    return vector.transform(transformation)

def distance(a, b):
    return len(a - b)

def distance_squared(a, b):
    return (a - b).length_squared()

class Vector2(object):

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return '{X=' + str(self.x) + ' Y=' + str(self.y) + '}'

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def scale(self, factor):
        return Vector2(self.x * factor, self.y * factor)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __len__(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return (self.x * self.x + self.y * self.y)

    def normalize(self):
        length = len(self)

        if length == 0:
            return

        num = 1.0 / length
        self.x *= num
        self.y *= num

    def clone(self):
        return Vector2(self.x, self.y)

    def transform(self, transformation):
        x = (self.x * transformation.m[0]) + (self.y * transformation.m[4])
        y = (self.x * transformation.m[1]) + (self.y * transformation.m[5])
        return Vector2(x, y)
