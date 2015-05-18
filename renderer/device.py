#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

from PIL import Image, ImageDraw

from math3d import vector2
from math3d import vector3

# Local imports
import color4 as c4
import scene as s
import polygon as p
from polygon2d import Polygon2D

class Device(object):
    """
    A render device which renders a 3D mesh to a file
    """

    def __init__(self, screen_width, screen_height, name, debug):
        """
        Initialize the device with a size and filename

        screen_width -- the width of the screen
        screen_height -- the height of the screen
        name -- the name of the file to render
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.name = name
        self.debug = debug

        self.zbuffer = [None] * (self.screen_width * self.screen_height)

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

        print '- Projecting triangle strips'
        self.polygons = []
        ys = []
        for strip in primitive.strips:
            current = Polygon2D(None)
            for triangle in strip:
                # if scene.is_backface(triangle.center(), triangle.normal()):
                #     continue

                projected = map(lambda v: scene.simple_project(v), triangle.vertices())
                current += Polygon2D(projected)

            # if current.empty():
            #     continue

            ys.append(current.y)
            ys.append(current.y + current.height)
            self.polygons.append(current)

        miny = min(ys)
        maxy = max(ys)
        print '- Mesh y coordinate goes from {} to {}'.format(miny, maxy)

        print '- Populating depth buffer'
        mindepth, maxdepth, depth_buffer = self.generate_depth_buffer()
        print '- Depth buffer goes from {}-{}'.format(mindepth, maxdepth)

        if self.debug:
            image = Image.new('RGBA', (self.screen_width, self.screen_height))
            draw = ImageDraw.Draw(image)
            for y in xrange(self.screen_height):
                for x in xrange(self.screen_width):
                    i = x + y * self.screen_width
                    xy = [(x, y)]

                    # Set "color"
                    c = 0
                    if depth_buffer[i] is not None:
                        c = int(round(255 * ((maxdepth - depth_buffer[i]) / (maxdepth - mindepth))))
                    pc = (c, c, c, 255)

                    draw.point(xy, pc)
            del draw
            depth_filename = self.name + '-depth.png'
            with open(depth_filename, 'w') as f:
                image.save(f, 'PNG')

        print '- Culling obscured polygons starting with {}'.format(len(self.polygons))
        obscured = []
        for p in self.polygons:
            if self.is_completely_obscured(p, depth_buffer):
                obscured.append(p)

        self.polygons = filter(lambda p: p not in obscured, self.polygons)

        print '- After culling have {} polygons'.format(len(self.polygons))

        print '- Sorting polygons'
        self.polygons.sort(key=lambda p: p.zmap.comparison_values(lambda z: (maxdepth - z) / (maxdepth - mindepth), lambda y: 1 - (maxy - y) / (maxy - miny)))

        print '- Drawing to file'
        for p in self.polygons:
            self.draw_polygon(p.vertices(), color)

        print '- Finishing render'
        self.end_render()

    def generate_depth_buffer(self):
        depth_buffer = [None] * (self.screen_width * self.screen_height)
        mins = []
        maxs = []
        for p in self.polygons:
            if p.minz is not None:
                mins.append(p.minz)
            if p.maxz is not None:
                maxs.append(p.maxz)

            pmap = p.zmap
            for y in xrange(pmap.height):
                for x in xrange(pmap.width):
                    i = (x + pmap.x) + (y + pmap.y) * self.screen_width
                    z = pmap.get(x, y)
                    if z is not None and (depth_buffer[i] is None or z < depth_buffer[i]):
                        depth_buffer[i] = z

            # can be parallelized as long as the set if larger/smaller is atomic
        return (min(mins), max(maxs), depth_buffer)

    def is_completely_obscured(self, polygon, depth_buffer):
        area = polygon.zmap.area()
        covered = 0
        for y in xrange(polygon.height):
            for x in xrange(polygon.width):
                gx = x + polygon.x
                gy = y + polygon.y
                z = polygon.zmap.get(x, y)
                if z is not None and z > depth_buffer[gx + gy * self.screen_width]:
                    covered += 1

        return area == covered

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

