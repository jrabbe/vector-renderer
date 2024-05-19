#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

def from_values(values):
    result = Matrix()
    # Copy the values
    result.m = values[:]
    return result

def identity():
    return Matrix(identity=True)

def zero():
    return Matrix()

def find_transformation(v1, v2):
    """
    Find the transformation mapping the triangle provided by the three points in v1
    to the triangle specified by the three points in v2. For triangles in 2D this will
    be an affine transformation with homogenous coordinates.
    """
    A = from_values([v1[0].x, v1[0].y, 1, v1[1].x, v1[1].y, 1, v1[2].x, v1[2].y, 1])
    B = from_values([v2[0].x, v2[0].y, 1, v2[1].x, v2[1].y, 1, v2[2].x, v2[2].y, 1])

    return ~A * B

class Matrix(object):
    '''
    Matrix class for a 3 x 3 matrix.

    Note that the matrix is in column major notation

    [0 3 6]
    [1 4 7]
    [2 5 8]
    '''

    def __init__(self, identity=False):
        self.m = [0.0] * 9

        if identity:
            self.m[0] = 1.0
            self.m[4] = 1.0
            self.m[8] = 1.0

    def __str__(self):
        return """
        {0[0]} {0[3]} {0[6]}
        {0[1]} {0[4]} {0[7]}
        {0[2]} {0[5]} {0[8]}
        """.format(self.m)

    def is_identity(self):
        if self.m[0] != 1.0 or self.m[4] != 1.0 or self.m[8] != 1.0:
            return False

        if self.m[1] != 0.0 or self.m[2] != 0.0 or self.m[3] != 0.0 or self.m[5] != 0.0 or self.m[6] != 0.0 or self.m[7] != 0.0:
            return False

        return True

    def determinant(self):
        a = self.m[0] * self.m[4] * self.m[8]
        b = self.m[3] * self.m[7] * self.m[2]
        c = self.m[6] * self.m[1] * self.m[5]
        d = self.m[6] * self.m[4] * self.m[2]
        f = self.m[3] * self.m[1] * self.m[8]
        g = self.m[0] * self.m[7] * self.m[5]

        return (a + b + c) - (d + f + g)

    def as_array(self):
        return self.m

    def __invert__(self):
        a = self.m[0]
        b = self.m[3]
        c = self.m[6]
        d = self.m[1]
        e = self.m[4]
        f = self.m[7]
        g = self.m[2]
        h = self.m[5]
        i = self.m[8]
        A =   e * i - f * h
        B = -(d * i - f * g)
        C =   d * h - e * g
        D = -(b * i - c * h)
        E =   a * i - c * g
        F = -(a * h - b * g)
        G =   b * f - c * e
        H = -(a * f - c * d)
        I =   a * e - b * d

        det = a * A + b * B + c*C

        self.m[0] = A / det
        self.m[1] = B / det
        self.m[2] = C / det
        self.m[3] = D / det
        self.m[4] = E / det
        self.m[5] = F / det
        self.m[6] = G / det
        self.m[7] = H / det
        self.m[8] = I / det

        return self

    def __mul__(self, other):
        result = Matrix()

        result.m[0] = self.m[0] * other.m[0] + self.m[1] * other.m[3] + self.m[2] * other.m[6]
        result.m[1] = self.m[0] * other.m[1] + self.m[1] * other.m[4] + self.m[2] * other.m[7]
        result.m[2] = self.m[0] * other.m[2] + self.m[1] * other.m[5] + self.m[2] * other.m[8]
        result.m[3] = self.m[3] * other.m[0] + self.m[4] * other.m[3] + self.m[5] * other.m[6]
        result.m[4] = self.m[3] * other.m[1] + self.m[4] * other.m[4] + self.m[5] * other.m[7]
        result.m[5] = self.m[3] * other.m[2] + self.m[4] * other.m[5] + self.m[5] * other.m[8]
        result.m[6] = self.m[6] * other.m[0] + self.m[7] * other.m[3] + self.m[8] * other.m[6]
        result.m[7] = self.m[6] * other.m[1] + self.m[7] * other.m[4] + self.m[8] * other.m[7]
        result.m[8] = self.m[6] * other.m[2] + self.m[7] * other.m[5] + self.m[8] * other.m[8]

        return result

    def __eq__(self, other):
        return (self.m[0] == other.m[0] and self.m[1] == other.m[1] and self.m[2] == other.m[2] and
            self.m[3] == other.m[3] and self.m[4] == other.m[4] and self.m[5] == other.m[5] and
            self.m[6] == other.m[6] and self.m[7] == other.m[7] and self.m[8] == other.m[8]);

    def clone(self):
        return from_values(self.m)

    def transpose(self):
        result = Matrix()
        result.m[0] = self.m[0]
        result.m[1] = self.m[3]
        result.m[2] = self.m[7]
        result.m[3] = self.m[6]
        result.m[4] = self.m[4]
        result.m[5] = self.m[7]
        result.m[6] = self.m[3]
        result.m[7] = self.m[5]
        result.m[8] = self.m[8]
        self.m = result.m

        return self

    def scale(self, factor):
        self.m = list(map(lambda v: factor * v, self.m))
        return self

