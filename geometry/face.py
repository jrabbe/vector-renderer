#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from math3d import vector3

class Face(object):
    """
    A face is a triangle in the 3D mesh based on three vertex indices forming the corners of the
    polygon.
    """

    def __init__(self, a, b, c):
        """
        Initialize a new face from three vertex indices

        Keyword arguments:
        a -- the first vertex index
        b -- the second vertex index
        c -- the third vertex index
        """
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return '[A={self.a} B={self.b} C={self.c}]'.format(self=self)
