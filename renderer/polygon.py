#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

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

        self.projection0 = self.scene.project(self.vertex0)
        self.projection1 = self.scene.project(self.vertex1)
        self.projection2 = self.scene.project(self.vertex2)

        self.points = [self.projection0, self.projection1, self.projection2]
        self.average_z = reduce(lambda acc, pt: acc + pt.world_coordinates.z, self.points, 0) / 3

    def clamp(self, value, minval=0, maxval=1):
        return max(minval, min(value, minval))

    def interpolate(self, minval, maxval, gradient):
        return minval + (maxval - minval) * self.clamp(gradient)

    def __find_midpoint(self, ln0, ln1, ln2):
        return (ln1 - ln0) / (ln2 - ln0) if ln2 - ln0 != 0 else 0

    def draw_normal(self, point):
        color = c4.Color4(point.world_normal.x, point.world_normal.y, point.world_normal.z, 0.5)
        self.draw_line(point.normal, point.coordinates, color)

    def __find_base(self, points):
        points.sort(cmp=lambda x, y: cmp(x.light_normal, y.light_normal))
        midpoint = self.__find_midpoint(points[0].light_normal, points[1].light_normal, points[2].light_normal)
        return [v2.Vector2(0, 0), v2.Vector2(midpoint, 0.5), v2.Vector2(1, 0)]

    def draw(self):
        """
        Draw this polygon using the scene to project it into the rendered 2D space.
        """

        is_facing_camera = reduce(lambda acc, pt: acc or pt.is_facing_camera(), self.points, False)
        if not is_facing_camera:
            return

        base = self.__find_base(self.points)
        point_coords = map(lambda p: p.coordinates, self.points)
        point_transformation = m3.find_transformation(base, point_coords)

        self.do_draw(self.points, base, self.color, point_transformation)

    def do_draw(self, points, base, color, point_transformation):
        """
        Perform the actual drawing, to be implemented by specific subclasses
        """
        raise NotImplementedError

    def draw_line(self, point0, point1, color):
        """
        Draw a line onto the output device
        """
        raise NotImplementedError
