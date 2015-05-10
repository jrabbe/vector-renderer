#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import plotdevice as pd

import device as d

class Device(d.Device):

    def __init__(self, screen_width, screen_height, name, options={}):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, name=name)

        fps = options.get('fps', 30)
        self.animated = options.get('animated', True)

        pd.size(screen_width, screen_height)
        if self.animated:
            self.canvas = pd.export(name + '.gif', fps=fps, loop=-1)
        else:
            self.canvas = pd.export(name + '.png')

    def begin_render(self):
        pd.clear(all)

    def end_render(self):
        self.canvas.add()

    def present(self):
        self.canvas.finish()

    def __pd_color(self, color):
        return pd.color(color.r, color.g, color.b, color.a)

    def draw_line(self, point0, point1, color=None):
        pd.pen(0.1)
        if color is not None:
            c = self.__pd_color(color)
            pd.stroke(c)

        pd.line(point0.x, point0.y, point1.x, point1.y)

    def draw_triangle(self, base_points, transformation, start_brightness, end_brightness, base_color=None):
        pd.pen(0.1, join=pd.BEVEL)
        pd.stroke(0)

        if base_color is not None:
            cs = self.__pd_color(base_color.scaled(start_brightness))
            ce = self.__pd_color(base_color.scaled(end_brightness))
            pd.fill(cs, ce)

        base_points = map(lambda p: p.transform(transformation), base_points)
        points = map(lambda p: (p.x, p.y), base_points)
        pd.bezier(points, close=True)

    def draw_polygon(self, points, base_color=None):
        """
        Draw a polygon with the provided points

        """
        raise NotImplementedError
