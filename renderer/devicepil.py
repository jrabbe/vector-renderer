#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from PIL import Image, ImageDraw

import device as d
import vector2

class Device(d.Device):

    def __init__(self, screen_width, screen_height, name):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, name=name)

        self.image = Image.new('RGBA', (screen_width, screen_height))

    def begin_render(self):
        self.draw = ImageDraw.Draw(self.image)

    def end_render(self):
        del self.draw

    def present(self):
        with open(self.name + '.png', 'w') as f:
            self.image.save(f, 'PNG')

    def __pil_color(self, color=None):
        if color is None:
            return (255, 0, 0, 255)

        return (255 * color.r, 255 * color.g, 255 * color.b, 255* color.a)

    def draw_triangle(self, base_points, transformation, start_brightness, end_brightness, base_color=None):
        base_points = map(lambda p: p.apply_affine(transformation), base_points)
        for i in xrange(len(base_points)):
            a = base_points[i]
            b = base_points[(i + 1) % len(base_points)]
            self.draw_line(a, b, base_color)

    def draw_line(self, point0, point1, color=None):
        x0 = int(round(point0.x))
        y0 = int(round(point0.y))
        x1 = int(round(point1.x))
        y1 = int(round(point1.y))
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.draw_point(x0, y0, color);

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err;
            if e2 > -dy:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += sy

    def draw_point(x, y, color=None):
        pc = self.__pil_color(color)
        xy = [(x, y)]
        self.draw.point(xy, pc)
