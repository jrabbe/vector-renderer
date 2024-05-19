#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

# Local imports
from .color4 import Color
from .scene import Scene
from .polygon import Polygon

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
        return Polygon(vertices, color, scene, self)

    def render(self, camera, meshes):
        """
        Render the provided meshes with the specified camera.

        camera -- the camera to use for rendering
        meshes -- the meshes to render
        """
        color = Color(1.0, 0.0, 0.0, 1.0)
        scene = Scene(self.screen_width, self.screen_height, camera)
        self.begin_render()

        for mesh in meshes:
            scene.set_mesh(mesh)
            polygons = []

            for triangle in mesh.triangles:

                polygon = self.polygon([triangle.va, triangle.vb, triangle.vc], color, scene)
                polygons.append(polygon)

            # Order the polygons in the scene to allow rendering foreground polygons in from of background polygons.
            polygons.sort()

            for polygon in polygons:
                polygon.draw()

        self.end_render()

    # --------------------------------------------------------------------------

    def draw_line(self, point0, point1, color=None):
        """
        Draw a point at the provided point

        point -- the point to draw to the output device
        """
        raise NotImplementedError

    def draw_triangle(self, base_points, transformation, start_brightness, end_brightness, base_color=None):
        """
        Draw a point at the provided point

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

