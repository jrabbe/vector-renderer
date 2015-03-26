#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import vector3 as v3
import color4 as c4

class Polygon(object):

    def __init__(self, vertex0, vertex1, vertex2, color):

        self.vertex0 = vertex0
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.color = color

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

    def is_backface(self, vertex, world_matrix, camera):
        world_coordinates = (vertex.coordinates).transform(world_matrix)
        world_normal = (vertex.normal + vertex.coordinates).transform(world_matrix)
        return (world_coordinates - camera.position).dot(world_normal) >= 0

    def draw_normal(self, vertex, transformation, project):
        coords = project(vertex.coordinates, transformation)
        nc = vertex.normal + vertex.coordinates
        normal = project(nc, transformation)
        self.draw_line(normal, coords, c4.Color4(nc.x, nc.y, nc.z, 0.5))

    def draw(self, world_matrix, transformation, project, camera):
        """
        Draw this polygon with the provided world matrix and transformation
        """
        if self.is_backface(self.vertex0, world_matrix, camera) and self.is_backface(self.vertex1, world_matrix, camera) and self.is_backface(self.vertex2, world_matrix, camera):
            return

        point0 = project(self.vertex0.coordinates, transformation)
        point1 = project(self.vertex1.coordinates, transformation)
        point2 = project(self.vertex2.coordinates, transformation)

        self.do_draw([point0, point1, point2], self.color)
        self.draw_normal(self.vertex0, transformation, project)
        self.draw_normal(self.vertex1, transformation, project)
        self.draw_normal(self.vertex2, transformation, project)

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
