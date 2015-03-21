#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import plotdevice as pd
import device as d

class Device(d.Device):

    def __init__(self, screen_width, screen_height, name, options={}):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, name=name)

        fps = options.get('fps', 30)

        pd.size(screen_width, screen_height)
        self.canvas = pd.export(name + '.gif', fps=fps, loop=-1)

    def draw_line(self, point0, point1, color=None):
        pd.pen(0.1)
        if color is not None:
            c = pd.color(color.r, color.g, color.b, color.a)
            pd.stroke(c)

        pd.line(point0.x, point0.y, point1.x, point1.y)

    def draw_triangle(self, point0, point1, point2, color=None):
        pd.pen(0.1, join=pd.BEVEL)
        pd.stroke(0)

        if color is not None:
            c = pd.color(color.r, color.g, color.b, color.a)
            pd.fill(c)

        points = [(point0.x, point0.y), (point1.x, point1.y), (point2.x, point2.y)]
        pd.bezier(points, close=True)

    def begin_render(self):
        pd.clear(all)

    def end_render(self):
        self.canvas.add()

    def present(self):
        self.canvas.finish()
