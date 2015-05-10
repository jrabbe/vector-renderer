#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

from math3d import vector2

# Local imports
import color4 as c4
import scene as s
import polygon as p
from polygon2d import Polygon2D
from zmap import ZMap

class Meta(object):

    def __init__(self, miny, avgy, maxy, minz, avgz, maxz):
        self.miny = miny
        self.avgy = avgy
        self.maxy = maxy

        self.minz = minz
        self.avgz = avgz
        self.maxz = maxz

    def __str__(self):
        return '[Y={} < {} < {} Z={} < {} < {}]'.format(self.miny, self.avgy, self.maxy, self.minz, self.avgz, self.maxz)

    def __cmp__(self, other):
        # print 'comparing {} to {}'.format(self, other)

        if self.maxz < other.minz:
            # if other is completely in from of self, move self backward
            return -1

        if self.minz > other.maxz:
            # if self is completely in front of other, move self forward
            return 1

        if self.minz >= other.minz and self.maxz <= other.maxz:
            # if they are completely overlapping

            if self.miny > other.maxy:
                # if completely above, move forward
                return 1
            elif self.maxy < other.miny:
                # if completely below move backwards
                return -1

        # TODO: next steps
        # 1. Figure interpolated z values for larger surface to get which one is _actually_ in front
        return cmp(self.avgz, other.avgz)

class Device(object):
    """
    A render device which renders a 3D mesh to a file
    """

    def __init__(self, screen_width, screen_height, name):
        """
        Initialize the device with a size and filename

        screen_width -- the width of the screen
        screen_height -- the height of the screen
        filename -- the name of the file to render
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.name = name

    def polygon(self, vertices, color, scene):
        """
        Get the polygon instance for the device
        """
        return p.Polygon(vertices, color, scene, self)

    def render_primitive(self, camera, primitive):
        print 'Rendering primitive'

        print '- Creating scene'
        scene = s.Scene(self.screen_width, self.screen_height, camera)
        self.begin_render()
        scene.set_rotation_translation(primitive.rotation, primitive.position)

        color = c4.Color(1.0, 0.0, 0.0, 1.0)

        polygons = []
        print '- Projecting triangle strips'
        for triangle_strip in primitive.strips:
            current = Polygon2D()
            for triangle in triangle_strip:
                projected = map(lambda v: scene.simple_project(v), triangle.vertices())
                current += Polygon2D(projected)

            current.generate_zmap()
            polygons.append(current)
            # self.draw_polygon(current.vertices(), color)

        print '- Sorting polygons'
        polygons.sort()

        print '- Drawing to file'
        for p in polygons:
            self.draw_polygon(p.vertices(), color)

        print '- Finishing render'
        self.end_render()

    def render(self, camera, meshes):
        """
        Render the provided meshes with the specified camera.

        camera -- the camera to use for rendering
        meshes -- the meshes to render
        """
        print 'Rendering mesh'
        color = c4.Color(1.0, 0.0, 0.0, 1.0)
        scene = s.Scene(self.screen_width, self.screen_height, camera)
        self.begin_render()

        for mesh in meshes:
            scene.set_rotation_translation(mesh.rotation, mesh.position)
            polygons = []

            for triangle in mesh.triangles:
                polygon = self.polygon([triangle.va, triangle.vb, triangle.vc], color, scene)
                polygons.append(polygon)

            polygons.sort()

            for polygon in polygons:
                polygon.draw()

        self.end_render()

    # --------------------------------------------------------------------------

    def draw_line(self, point0, point1, color=None):
        """
        Draw a line between the provided points using the specified color

        point0 -- the point to start the line
        point1 -- the point to end the line
        color -- the color to stroke the line
        """
        raise NotImplementedError

    def draw_triangle(self, base_points, transformation, start_brightness, end_brightness, base_color=None):
        """
        Draw a triangle with the provided parameters

        """
        raise NotImplementedError

    def draw_polygon(self, points, base_color=None):
        """
        Draw a polygon with the provided points

        """
        raise NotImplementedError

    def begin_render(self):
        """
        Do any device specific initialization at the beginning of rendering, before anything is
        drawn.
        """
        raise NotImplementedError

    def end_render(self):
        """
        Do any device specific finalizing at the end of rendering, after everything has been
        drawn.
        """
        raise NotImplementedError

    def present(self):
        raise NotImplementedError

