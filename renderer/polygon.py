#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import vector3 as v3
import color4 as c4

class Polygon(object):

    def __init__(self, vertex0, vertex1, vertex2, color, scene):

        self.vertex0 = vertex0
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.color = color
        self.scene = scene

        self.order()

    def order(self):
        if self.vertex0.coordinates.y > self.vertex1.coordinates.y:
            self.vertex0, self.vertex1 = v3.swap(self.vertex0, self.vertex1)

        if self.vertex1.coordinates.y > self.vertex2.coordinates.y:
            self.vertex1, self.vertex2 = v3.swap(self.vertex1, self.vertex2)

        if self.vertex0.coordinates.y > self.vertex1.coordinates.y:
            self.vertex0, self.vertex1 = v3.swap(self.vertex0, self.vertex1)

    def clamp(self, value, minval=0, maxval=1):
        return max(minval, min(value, minval))

    def interpolate(self, minval, maxval, gradient):
        return minval + (maxval - minval) * self.clamp(gradient)

    def is_backface(self, vertex):
        return not self.scene.is_facing_camera(vertex)

    def draw_normal(self, point):
        color = c4.Color4(point.world_normal.x, point.world_normal.y, point.world_normal.z, 0.5)
        self.draw_line(point.normal, point.coordinates, color)

    def draw(self):
        """
        Draw this polygon with the provided world matrix and transformation
        """

        point0 = self.scene.project(self.vertex0)
        point1 = self.scene.project(self.vertex1)
        point2 = self.scene.project(self.vertex2)

        if not (point0.is_facing_camera() or point1.is_facing_camera() or point2.is_facing_camera()):
            return

        self.do_draw([point0.coordinates, point1.coordinates, point2.coordinates], self.color)
        self.draw_normal(point0)
        self.draw_normal(point1)
        self.draw_normal(point2)

    def do_draw(self, points, color):
        """
        Perform the actual drawing, to be implemented by specific subclasses
        """
        raise NotImplementedError

    def draw_line(self, point0, point1, color):
        """
        Draw a line onto the output device
        """
        raise NotImplementedError
