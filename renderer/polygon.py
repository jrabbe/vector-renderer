#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
import functools

from math3d import vector2 as v2
from math3d import matrix3 as m3

from .color4 import Color

class Polygon(object):

    def __init__(self, vertices, color, scene, device):

        self.color = color
        self.scene = scene
        self.device = device

        self.points = []
        for vertex in vertices:
            projection = self.scene.project(vertex);
            self.points.append(projection)

        self.vertices = vertices

        self.average_z = functools.reduce(lambda acc, pt: acc + pt.projected_z, self.points, 0) / 3
        self.average_y = functools.reduce(lambda acc, pt: acc + pt.world_y, self.points, 0) / 3

    # Was used as a crude way to compare y & z values of two polygons. Will implement correct clipping.
    def __lt__(self, other):
        return self.__cmp(other) < 0

    def __gt__(self, other):
        return self.__cmp(other) > 0

    def __le__(self, other):
        return self.__cmp(other) <= 0

    def __ge__(self, other):
        return self.__cmp(other) >= 0

    def __eq__(self, other):
        return self.__cmp(other) == 0

    def __ne__(self, other):
        return self.__cmp(other) != 0
    
    def __cmp(self, other):
        if self.average_y > other.average_y:
            any_in_front = functools.reduce(lambda acc, pt: acc or (pt.projected_z > other.average_z), self.points, False)
            if any_in_front:
                return 1

        if self.average_z > other.average_z:
            return 1
        elif self.average_z < other.average_z:
            return -1
        else:
            return 0

    def __find_midpoint(self, ln0, ln1, ln2):
        return (ln1 - ln0) / (ln2 - ln0) if ln2 - ln0 != 0 else 0

    def __find_base(self, points):
        points.sort(key=lambda a: a.brightness)
        midpoint = self.__find_midpoint(points[0].brightness, points[1].brightness, points[2].brightness)
        return [v2.Vector(0, 0), v2.Vector(midpoint, 0.5), v2.Vector(1, 0)]

    def draw(self):
        """
        Draw this polygon using the scene to project it into the rendered 2D space.
        """

        is_facing_camera = functools.reduce(lambda acc, pt: acc or pt.is_facing_camera, self.points, False)
        if not is_facing_camera:
            return

        base = self.__find_base(self.points)
        point_coords = list(map(lambda p: p.coordinates, self.points))
        point_transformation = m3.find_transformation(base, point_coords)

        self.device.draw_triangle(base, point_transformation, self.points[0].brightness, self.points[2].brightness, self.color)
