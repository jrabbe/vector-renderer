#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import polygon as p

class Polygon(p.Polygon):

    def __init__ (self, vertex0, vertex1, vertex2, color, scene, pd):
        p.Polygon.__init__(self, vertex0, vertex1, vertex2, color, scene)
        self.pd = pd

    def do_draw(self, points, color):
        self.pd.pen(0.1, join=self.pd.BEVEL)
        self.pd.stroke(0)

        if color is not None:
            c = self.pd.color(color.r, color.g, color.b, color.a)
            self.pd.fill(c)

        points = map(lambda p: (p.x, p.y), points)
        self.pd.bezier(points, close=True)

    def draw_line(self, point0, point1, color=None):
        self.pd.pen(0.1)
        if color is not None:
            c = self.pd.color(color.r, color.g, color.b, color.a)
            self.pd.stroke(c)

        self.pd.line(point0.x, point0.y, point1.x, point1.y)

