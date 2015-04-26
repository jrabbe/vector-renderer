#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

from PIL import Image, ImageDraw

import device as d
import vector2
import vector3

class Device(d.Device):

    def __init__(self, screen_width, screen_height, name):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, name=name)

        self.image = Image.new('RGBA', (screen_width, screen_height))
        self.depthbuffer = [sys.maxint] * (screen_width * screen_height)

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

        r = int(round(255 * color.r))
        g = int(round(255 * color.g))
        b = int(round(255 * color.b))
        a = int(round(255 * color.a))

        return (r, g, b, a)

    def draw_triangle(self, base_points, z_values, transformation, start_brightness, end_brightness, base_color=None):
        base_points = map(lambda p: p.apply_affine(transformation), base_points)

        p0, p1, p2 = map(lambda tp: vector3.Vector3(tp[0].x, tp[0].y, tp[1]), zip(base_points, z_values))

        if p0.y > p1.y:
            p1, p0 = p0, p1

        if p1.y > p2.y:
            p2, p1 = p1, p2

        if p0.y > p1.y:
            p1, p0 = p0, p1

        dP0P1 = 0
        if p1.y - p0.y > 0:
            dP0P1 = (p1.x - p0.x) / (p1.y - p0.y)

        dP0P2 = 0
        if p2.y - p0.y > 0:
            dP0P2 = (p2.x - p0.x) / (p2.y - p0.y)

        y0 = int(round(p0.y))
        y2 = int(round(p2.y))

        if dP0P1 > dP0P2:
            for y in xrange(y0, y2):
                if y < p1.y:
                    self.process_scanline(y, p0, p2, p0, p1, base_color)
                else:
                    self.process_scanline(y, p0, p2, p1, p2, base_color)
        else:
            for y in xrange(y0, y2):
                if y < p1.y:
                    self.process_scanline(y, p0, p1, p0, p2, base_color)
                else:
                    self.process_scanline(y, p1, p2, p0, p2, base_color)


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
            self.draw_point(x0, y0, 0, color);

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err;
            if e2 > -dy:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += sy

    def draw_point(self, x, y, z, color=None):
        index = x + y * self.screen_width

        if self.depthbuffer[index] < z:
            return

        self.depthbuffer[index] = z

        pc = self.__pil_color(color)
        xy = [(x, y)]
        self.draw.point(xy, pc)

    def clamp(self, value, minimum=0.0, maximum=1.0):
        return max(minimum, min(value, maximum))

    def interpolate(self, minimum, maximum, gradient):
        return minimum + (maximum - minimum) * self.clamp(gradient)

    def process_scanline(self, y, pa, pb, pc, pd, color):
        gradient1 = (y - pa.y) / (pb.y - pa.y) if pa.y != pb.y else 1
        gradient2 = (y - pc.y) / (pd.y - pc.y) if pc.y != pd.y else 1

        sx = int(round(self.interpolate(pa.x, pb.x, gradient1)))
        ex = int(round(self.interpolate(pc.x, pd.x, gradient2)))

        z1 = self.interpolate(pa.z, pb.z, gradient1)
        z2 = self.interpolate(pc.z, pb.z, gradient2)

        for x in xrange(sx, ex):
            gradient = (x - sx) / (ex - sx)
            z = self.interpolate(z1, z2, gradient)
            self.draw_point(x, y, z, color)




