#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

import vector2 as v2
import color4 as c4
import matrix3 as m3

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

        self.average_z = reduce(lambda acc, pt: acc + pt.projected_z, self.points, 0) / 3
        self.average_y = reduce(lambda acc, pt: acc + pt.world_y, self.points, 0) / 3

    def __cmp__(self, other):
        if self.average_y > other.average_y:
            any_in_front = reduce(lambda acc, pt: acc or (pt.projected_z > other.average_z), self.points, False)
            if any_in_front:
                return 1

        return cmp(self.average_z, other.average_z)

    def __find_midpoint(self, ln0, ln1, ln2):
        return (ln1 - ln0) / (ln2 - ln0) if ln2 - ln0 != 0 else 0

    def __find_base(self, points):
        points.sort(cmp=lambda a, b: cmp(a.brightness, b.brightness))
        midpoint = self.__find_midpoint(points[0].brightness, points[1].brightness, points[2].brightness)
        return [v2.Vector(0, 0), v2.Vector(midpoint, 0.5), v2.Vector(1, 0)]

    def draw(self):
        """
        Draw this polygon using the scene to project it into the rendered 2D space.
        """

        is_facing_camera = reduce(lambda acc, pt: acc or pt.is_facing_camera, self.points, False)
        if not is_facing_camera:
            return

        base = self.__find_base(self.points)
        point_coords = map(lambda p: p.coordinates, self.points)
        point_transformation = m3.find_transformation(base, point_coords)

        self.device.draw_triangle(base, point_transformation, self.points[0].brightness, self.points[2].brightness, self.color)
