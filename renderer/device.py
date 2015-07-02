#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import math
import sys
import time

from PIL import Image, ImageDraw

from math3d import vector2
from math3d import vector3

from graphics import sobel
from graphics import fxaa
from graphics import antialias

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
        self.times = []

        self.zbuffer = [None] * (self.screen_width * self.screen_height)

    def polygon(self, vertices, color, scene):
        """
        Get the polygon instance for the device
        """
        return p.Polygon(vertices, color, scene, self)

    def render_primitive(self, camera, primitive):
        print 'Rendering primitive'
        # self.begin_render()

        print '- Creating scene'
        scene = s.Scene(self.screen_width, self.screen_height, camera)
        scene.set_rotation_translation(primitive.rotation, primitive.position)

        self.times.append(('scene', time.clock()))

        color = c4.Color(0.0, 1.0, 1.0, 1.0)

        print '- Projecting triangle strips'
        self.polygons = []
        self.normals = []
        self.brightness = []
        ys = []
        for strip in primitive.strips:
            current = Polygon2D(None)
            normal = vector3.zero()
            brightness = 0
            count = 0
            for triangle in strip:
                # if scene.is_backface(triangle.center(), triangle.normal()):
                #     continue

                count +=1
                projected = map(lambda v: scene.simple_project(v), triangle.vertices())
                current += Polygon2D(projected)
                normal += scene.to_world(triangle.surface_normal())
                brightness += sum(map(lambda v: scene.brightness(v.coordinates, v.normal), triangle.vertices())) / 3

            # if current.empty():
            #     continue

            ys.append(current.y)
            ys.append(current.y + current.height)
            self.polygons.append(current)
            self.normals.append(normal.scale(1/count))
            self.brightness.append(brightness / count)

        miny = min(ys)
        maxy = max(ys)
        print '- Mesh y coordinate goes from {} to {}'.format(miny, maxy)
        self.times.append(('project', time.clock()))

        print '- Populating depth buffer'
        mindepth, maxdepth, depth_buffer = self.generate_depth_buffer()
        print '- Depth buffer goes from {}-{}'.format(mindepth, maxdepth)
        self.times.append(('depth', time.clock()))

        print '- Detecting edges'
        G = sobel.apply(self.normal_buffer, self.screen_width, self.screen_height, sobel.abs_luminance)
        Gd = sobel.apply(depth_buffer, self.screen_width, self.screen_height, sobel.identity)
        GG = map(lambda g, gd: g if gd is None or (g is not None and g.length() > gd.length()) else gd, G, Gd)
        self.times.append(('edges', time.clock()))

        if self.debug:
            print '- outputting debug images'
            self.draw_image('depth', depth_buffer, lambda v: (int(round(255 * (maxdepth - v) / (maxdepth - mindepth))),) * 3)
            clamp_color = lambda c: min(255, max(c, 0))
            norval = lambda n: clamp_color(int(round(128 * (1 - n) + 128)))
            self.draw_image('normal', self.normal_buffer, lambda v: (norval(v.x), norval(v.y), norval(v.z)))
            self.draw_image('brightness', self.light_normal_buffer, lambda v: (int(round(255 * v)),) * 3)

            self.draw_image('sobel', GG, lambda v: (int(round(255 * (1 - v.length()))),) * 3)
            # self.draw_image('SUSAN', R, lambda v: (int(round(255 * (1 - v))),) * 3)
            self.times.append(('debug', time.clock()))


        cl = lambda b, v: b * v
        im = map(lambda b: (cl(b, color.r), cl(b, color.g), cl(b, color.b), 1.0) if b is not None else None, self.light_normal_buffer)
        raw_im = map(lambda b, g: (1 - g.length(),) * 3 + (1.0,) if g is not None else b, im, GG)
        raw_im = map(lambda b: (0.0,) * 4 if b is None else b, raw_im)
        im = map(lambda (r, g, b, a): c4.create(r, g, b, a), raw_im)
        c_im = map(lambda (r, g, b, a): c4.create(r, g, b, a), raw_im)
        self.times.append(('img buffer', time.clock()))

        if self.debug:
            width = self.screen_width
            height = self.screen_height
            print '- outputting debug from fxaa'
            print '-- passthrough'
            fxaa_passthrough = fxaa.apply(im, width, height, debug_passthrough=True)
            self.draw_image('fxaa_passthrough', fxaa_passthrough, lambda d: d.scale(255, scale_alpha=True).values())

            print '-- horzvert'
            fxaa_horzvert = fxaa.apply(im, width, height, debug_horzvert=True)
            self.draw_image('fxaa_horzvert', fxaa_horzvert, lambda d: d.scale(255, scale_alpha=True).values())

            print '-- pair'
            fxaa_pair = fxaa.apply(im, width, height, debug_pair=True)
            self.draw_image('fxaa_pair', fxaa_pair, lambda d: d.scale(255, scale_alpha=True).values())

            print '-- negpos'
            fxaa_negpos = fxaa.apply(im, width, height, debug_negpos=True)
            self.draw_image('fxaa_negpos', fxaa_negpos, lambda d: d.scale(255, scale_alpha=True).values())

            print '-- offset'
            fxaa_offset = fxaa.apply(im, width, height, debug_offset=True)
            self.draw_image('fxaa_offset', fxaa_offset, lambda d: d.scale(255, scale_alpha=True).values())
            self.times.append(('fxaa debug', time.clock()))

        print '- fxaa'
        im = fxaa.apply(im, self.screen_width, self.screen_height)
        self.times.append(('fxaa', time.clock()))

        print '- Drawing final image'
        self.draw_image('image', im, lambda d: d.scale(255, scale_alpha=True).values())
        self.times.append(('image', time.clock()))
        # print '-- rendering image output'
        # image = Image.new('RGBA', (self.screen_width, self.screen_height))
        # draw = ImageDraw.Draw(image)
        # for y in xrange(self.screen_height):
        #     for x in xrange(self.screen_width):
        #         i = x + y * self.screen_width
        #         xy = [(x, y)]

        #         b = self.light_normal_buffer[i]
        #         g = GG[i]
        #         if b is not None:
        #             c = lambda v: int(round(255 * b * v))
        #             pc = (c(color.r), c(color.g), c(color.b), 255)

        #             if g is not None:
        #                 gl = g.length()
        #                 c = int(round(255 * (1 - gl)))
        #                 pc = (c, c, c, 255)

        #             draw.point(xy, pc)
        # del draw
        # filename = self.name + '.png'
        # with open(filename, 'w') as f:
        #     image.save(f, 'PNG')

        # print '- Culling obscured polygons starting with {}'.format(len(self.polygons))
        # obscured = []
        # for p in self.polygons:
        #     if self.is_completely_obscured(p, depth_buffer):
        #         obscured.append(p)

        # self.polygons = filter(lambda p: p not in obscured, self.polygons)

        # print '- After culling have {} polygons'.format(len(self.polygons))

        # for p in self.polygons:
        #     v = lambda p: p.zmap.comparison_values(lambda z: (maxdepth - z) / (maxdepth - mindepth), lambda y: 1 - (maxy - y) / (maxy - miny))
        #     print '- comparison value for {} = {}'.format(p, v(p))

        # print '- Sorting polygons'
        # self.polygons.sort(key=lambda p: p.zmap.comparison_values(lambda z: (maxdepth - z) / (maxdepth - mindepth), lambda y: 1 - (maxy - y) / (maxy - miny)))

        # print '- Drawing to file'
        # for p in self.polygons:
        #     self.draw_polygon(p.vertices(), color)

        # print '- Finishing render'
        # self.end_render()

        return self.times

    def draw_image(self, postfix, buf, filler):
        print '-- rendering {} output'.format(postfix)
        image = Image.new('RGBA', (self.screen_width, self.screen_height))
        draw = ImageDraw.Draw(image)
        inted = lambda (r, g, b, a): (int(round(r)), int(round(g)), int(round(b)), int(round(a)))
        for y in xrange(self.screen_height):
            for x in xrange(self.screen_width):
                i = x + y * self.screen_width
                xy = [(x, y)]

                v = buf[i]

                if v is not None:
                    pc = filler(v)
                    if len(pc) == 3:
                        pc += (255,)

                    draw.point(xy, inted(pc))
        del draw
        filename = self.name + '-{}.png'.format(postfix)
        with open(filename, 'w') as f:
            image.save(f, 'PNG')

    def generate_depth_buffer(self):
        depth_buffer = [None] * (self.screen_width * self.screen_height)
        normal_buffer = [None] * (self.screen_width * self.screen_height)
        light_normal_buffer = [None] * (self.screen_width * self.screen_height)

        i = lambda x, y: x + y * self.screen_width
        valid = lambda i, buf: i >= 0 and i < len(buf)
        mins = []
        maxs = []
        for pidx in xrange(len(self.polygons)):
            p = self.polygons[pidx]
            n = self.normals[pidx]
            b = self.brightness[pidx]
            if p.minz is not None:
                mins.append(p.minz)
            if p.maxz is not None:
                maxs.append(p.maxz)

            pmap = p.zmap
            for y in xrange(pmap.height):
                for x in xrange(pmap.width):
                    idx = i(x + pmap.x, y + pmap.y)

                    z = pmap.get(x, y)
                    if z is not None and valid(idx, depth_buffer) and (depth_buffer[idx] is None or z < depth_buffer[idx]):
                        depth_buffer[idx] = z
                        normal_buffer[idx] = n
                        light_normal_buffer[idx] = b

        self.normal_buffer = normal_buffer
        self.light_normal_buffer = light_normal_buffer

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

