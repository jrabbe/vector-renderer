#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import plotdevice as pd

import device as d

class Device(d.Device):

    def __init__(self, screen_width, screen_height, filename, options={}):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, filename=filename)

        fps = options.get('fps', 30)

        pd.size(screen_width, screen_height)
        self.canvas = pd.export(filename, fps=fps, loop=-1)

    def draw_point(self, point):
        # clipping what is visible inside "screen"
        if point.x >= 0 and point.y >= 0 and point.x < self.screen_width and point.y < self.screen_height:
            pd.oval(point.x, point.y, 1, 1, stroke=None, fill='red')

    def draw_line(self, point0, point1):
        dist = len(point0 - point1)

        if dist < 2:
            return

        pd.stroke(0.5)
        pd.line(point0.x, point0.y, point1.x, point1.y)

    def draw_triangle(self, point0, point1, point2):
        points = [(point0.x, point0.y), (point1.x, point1.y), (point2.x, point2.y)]
        pd.bezier(points, stroke=0.5, fill=None, close=True)

    def begin_render(self):
        pd.clear(all)

    def end_render(self):
        self.canvas.add()

    def present(self):
        self.canvas.finish()
