#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

# Local imports
import vector2 as v2
import vector3 as v3
import matrix
import color4 as c4
import scene as s

# http://en.wikipedia.org/wiki/Back-face_culling
# Possibly doing the dot product for each vertex normal and the camera->vertex vector, and
# discarding each triangle where all dot products are >= 0 => ∀[(Vi-C) · Ni ≥ 0]
#
# Pseudo code to calculate face normal based on vertex points and normals
#
# Vec3 CalcNormalOfFace( Vec3 pPositions[3], Vec3 pNormals[3] )
# {
#     Vec3 p0 = pPositions[1] - pPositions[0];
#     Vec3 p1 = pPositions[2] - pPositions[0];
#     Vec3 faceNormal = crossProduct( p0, p1 );

#     Vec3 vertexNormal = pNormals[0]; // or you can average 3 normals.
#     float dot = dotProduct( faceNormal, vertexNormal );

#     return ( dot < 0.0f ) ? -faceNormal : faceNormal;
# }

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

    def draw_line(self, point0, point1, color=None):
        """
        Draw a point at the provided point

        point -- the point to draw to the output device
        """
        raise NotImplementedError

    def draw_triangle(self, point0, point1, point2, color=None):
        """
        Draw a point at the provided point

        point -- the point to draw to the output device
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

    def polygon(self, vertex0, vertex1, vertex2, color, scene):
        """
        Get the polygon instance for the device
        """
        raise NotImplementedError


    def render(self, camera, meshes):
        """
        Render the provided meshes with the specified camera.

        camera -- the camera to use for rendering
        meshes -- the meshes to render
        """

        scene = s.Scene(self.screen_width, self.screen_height, camera)
        self.begin_render()

        for mesh in meshes:
            scene.set_mesh(mesh)

            for face in mesh.faces:
                vertex0 = mesh.vertices[face.a]
                vertex1 = mesh.vertices[face.b]
                vertex2 = mesh.vertices[face.c]

                color = c4.Color4(0.0, 1.0, 1.0, 1.0)

                poly = self.polygon(vertex0, vertex1, vertex2, color, scene)
                poly.draw()

        self.end_render()

    def present(self):
        raise NotImplementedError

