#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import math

from math3d import vector3

class Triangle(object):
    """
    A triangle in the 3D mesh based on three vertex indices forming the corners
    of the polygon.
    """

    def __init__(self, a, b, c):
        """
        Initialize a new face from three vertex indices

        Arguments:
        a -- the first vertex index
        b -- the second vertex index
        c -- the third vertex index
        """
        self.a = a
        self.b = b
        self.c = c

        self.ab = None
        self.bc = None
        self.ca = None

        self.va = None
        self.vb = None
        self.vc = None

    def __str__(self):
        return '[A={self.a} B={self.b} C={self.c}]'.format(self=self)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c

    def indices(self):
        return [self.a, self.b, self.c]

    def set_vertices(self, va, vb, vc):
        self.va = va
        self.vb = vb
        self.vc = vc

    def vertices(self):
        return [self.va, self.vb, self.vc]

    def center(self):
        return self.va.coordinates.scale(1/3) + self.vb.coordinates.scale(1/3) + self.vc.coordinates.scale(1/3)

    def normal(self):
        return (self.va.normal + self.vb.normal + self.vc.normal).scale(1/3).normalize()

    def neighbors(self):
        return [x for x in [self.ab, self.bc, self.ca] if x is not None]

    def share_edge(self, other):
        indices = other.indices()
        return (self != other and
                ((self.a in indices and self.b in indices) or
                 (self.b in indices and self.c in indices) or
                 (self.c in indices and self.a in indices)))

    def __get_unique_vertices(self, other):
        result = indices()[:]
        for i in other.incides():
            if i not in result:
                result.append(i)

        return result

    def __coplaner(self, A, B, C, D):
        # (C - A)•[(B-A)x(D-C)] = 0
        return ((C - A).dot((B - A).cross(D - C)) == 0)

    def sine_of_angle(self, other):
        a = self.surface_normal()
        b = other.surface_normal()

        return a.cross(b).length()

    def angle(self, other):
        # atan2(len(cross(a,b)),dot(a,b))
        a = self.surface_normal()
        b = other.surface_normal()

        return math.atan2(a.cross(b).length(), a.dot(b))

    def surface_normal(self):
        return (self.va.normal + self.vb.normal + self.vc.normal).scale(1/3).normalize()
        # a = self.va.coordinates
        # b = self.vb.coordinates
        # c = self.vc.coordinates

        # u = b - a
        # v = c - a

        # return u.cross(v).normalize()

    def can_be_combined_with(self, other):
        if self == other:
            return False

        s = self.sine_of_angle(other)

        # Note: can be tuned to the exact angle that should mark the difference between two polygons.
        # A value of 0.2 seems to be the most effective.
        return s < 0.2
        # return False
