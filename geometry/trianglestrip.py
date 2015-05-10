#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

class TriangleStrip(object):

    def __init__(self, triangle=None):
        self.triangles = []

        if triangle is not None:
            self.triangles.append(triangle)

    def append(self, triangle):
        if triangle not in self.triangles:
            self.triangles.append(triangle)

    def __iter__(self):
        for t in self.triangles:
            yield t
