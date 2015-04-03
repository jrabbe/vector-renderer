#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import vector2 as v2
import vector3 as v3
import color4 as c4
import matrix3 as m3

class Polygon(object):

    def __init__(self, vertex0, vertex1, vertex2, color, scene):

        self.vertex0 = vertex0
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.color = color
        self.scene = scene

    def clamp(self, value, minval=0, maxval=1):
        return max(minval, min(value, minval))

    def interpolate(self, minval, maxval, gradient):
        return minval + (maxval - minval) * self.clamp(gradient)

    def draw_normal(self, point):
        color = c4.Color4(point.world_normal.x, point.world_normal.y, point.world_normal.z, 0.5)
        self.draw_line(point.normal, point.coordinates, color)

    def draw(self):
        """
        Draw this polygon using the scene to project it into the rendered 2D space.
        """

        point0 = self.scene.project(self.vertex0)
        point1 = self.scene.project(self.vertex1)
        point2 = self.scene.project(self.vertex2)

        if not (point0.is_facing_camera() or point1.is_facing_camera() or point2.is_facing_camera()):
            return

        points = [point0, point1, point2]
        points.sort(cmp=lambda x, y: cmp(x.light_normal, y.light_normal))
        midpoint = (points[1].light_normal - points[0].light_normal) / (points[2].light_normal - points[0].light_normal) if points[2].light_normal - points[0].light_normal != 0 else 0

        base = [v2.Vector2(0, 0), v2.Vector2(midpoint, 0.5), v2.Vector2(1, 0)]
        point_coords = map(lambda p: p.coordinates, points)
        point_transformation = m3.find_transformation(base, point_coords)

        self.do_draw(points, self.color, midpoint, point_transformation)

    def do_draw(self, points, color, midpoint, point_transformation):
        """
        Perform the actual drawing, to be implemented by specific subclasses
        """
        raise NotImplementedError

    def draw_line(self, point0, point1, color):
        """
        Draw a line onto the output device
        """
        raise NotImplementedError
