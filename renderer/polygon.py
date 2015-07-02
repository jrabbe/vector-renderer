#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

from math3d import vector2 as v2
from math3d import matrix3 as m3

import color4 as c4

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
        self.max_y = max(map(lambda pt: pt.world_y, self.points))

    def __cmp__(self, other):
        if self.max_y > other.max_y:
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

        point_coords = map(lambda p: p.coordinates, self.points)
        avg_brightness = sum(map(lambda p: p.brightness, self.points)) / len(self.points)

        self.device.draw_polygon(point_coords, self.color.scaled(avg_brightness), self.points)
