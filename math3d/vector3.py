#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import math

def create(x, y, z):
    return Vector(x, y, z)

def normalize(vector):
    result = vector.clone()
    return result.normalize()

def cross(a, b):
    return a.cross(b)

def dot(a, b):
    return a.dot(b)

def transform(vector, transformation):
    vector.transform(transformation)

def distance_squared(a, b):
    return (a - b).lengthSquared()

def distance(a, b):
    """
    Calculates the disctance between the two provided vectors
    """
    return len(a - b)

def zero():
    """
    Creates a zero vector, i.e. a vector with length zero
    """
    return Vector()

def up():
    """
    Creates a new 3D unit vector pointing up along the y axis.
    """
    return Vector(y=1.0)

class Vector(object):

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '[X={self.x:.5f} Y={self.y:.5f} Z={self.z:.5f}]'.format(self=self)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def scale(self, factor):
        return Vector(self.x * factor, self.y * factor, self.z * factor)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        # Note: this is not absolutely reliable for large (> 16-bit) values of x, y, or z
        return hash(self.x) << 32 ^ hash(self.y) << 16 ^ hash(self.z)

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y, self.z * other.z)

    def __div__(self, other):
        return Vector(self.x / other.x, self.y / other.y, self.z / other.z)

    def __truediv__(self, other):
        return self.__div__(other)

    def __len__(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalize(self):
        length = len(self)

        if length == 0:
            return self

        factor = 1.0 / length
        self.x *= factor
        self.y *= factor
        self.z *= factor

        return self

    def clone(self):
        return Vector(self.x, self.y, self.z)

    def cross(self, other):
        """
        Calculates the cross product of this vector against the provided,
        returning a new vector with the result.
        """
        result = Vector()
        result.x = self.y * other.z - self.z * other.y
        result.y = self.z * other.x - self.x * other.z
        result.z = self.x * other.y - self.y * other.x
        return result

    def dot(self, other):
        """
        Calculates the dot product of this vector against the other returning
        the calculated value.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def transform(self, transformation):
        """
        Performs the transformation of the values for this vector with the
        provided transformation matrix, returning a new vector with the
        transformed values.
        """
        x = (self.x * transformation.m[0]) + (self.y * transformation.m[4]) + (self.z * transformation.m[8]) + transformation.m[12]
        y = (self.x * transformation.m[1]) + (self.y * transformation.m[5]) + (self.z * transformation.m[9]) + transformation.m[13]
        z = (self.x * transformation.m[2]) + (self.y * transformation.m[6]) + (self.z * transformation.m[10]) + transformation.m[14]
        w = (self.x * transformation.m[3]) + (self.y * transformation.m[7]) + (self.z * transformation.m[11]) + transformation.m[15]
        return Vector(x / w, y / w, z / w)


