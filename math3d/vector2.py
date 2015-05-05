#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import math

def create(x, y):
    return Vector(x, y)

def normalize(vector):
    """
    Returns a normalized copy of the provided vector.
    """
    return vector.clone().normalize()

def transform(vector, transformation):
    """
    Transforms the provided vector with the specified transformation.
    """
    return vector.transform(transformation)

def distance(a, b):
    """
    Finds the distance between the two vectors a and b.
    """
    return (a - b).length()

def distance_squared(a, b):
    return (a - b).length_squared()

def to_vector2(vector):
    """
    Creates a Vector2 from the provided vector. This is done by taking the x and y coordinates
    of the provided vector.
    """
    return Vector(vector.x, vector.y)

class Vector(object):

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return '[X={self.x:.5f} Y={self.y:.5f}]'.format(self=self)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def scale(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) << 32 ^ hash(self.y)

    def __len__(self):
        return self.length()

    def length(self):
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

        return self

    def clone(self):
        return Vector(self.x, self.y)

    def transform(self, transformation):
        """
        Performs the transformation of the values for this vector with the
        provided transformation matrix, returning a new vector with the
        transformed values.
        """
        x = (self.x * transformation.m[0]) + (self.y * transformation.m[3]) + transformation.m[6]
        y = (self.x * transformation.m[1]) + (self.y * transformation.m[4]) + transformation.m[7]
        w = (self.x * transformation.m[2]) + (self.y * transformation.m[5]) + transformation.m[8]
        return Vector(x / w, y / w)
