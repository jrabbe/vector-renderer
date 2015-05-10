#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from math3d import vector3

from triangle import Triangle
from trianglestrip import TriangleStrip
import primitive
from vertex import Vertex

def cube():
    """
    Creates a cube around 0,0,0 with each side having a length of 2 (from -1 to 1)
    """
    vertices = [
        Vertex(vector3.Vector(-1, -1, -1),vector3.Vector(-1, -1, -1)),
        Vertex(vector3.Vector( 1, -1, -1),vector3.Vector( 1, -1, -1)),
        Vertex(vector3.Vector(-1,  1, -1),vector3.Vector(-1,  1, -1)),
        Vertex(vector3.Vector(-1, -1,  1),vector3.Vector(-1, -1,  1)),
        Vertex(vector3.Vector( 1,  1, -1),vector3.Vector( 1,  1, -1)),
        Vertex(vector3.Vector(-1,  1,  1),vector3.Vector(-1,  1,  1)),
        Vertex(vector3.Vector( 1, -1,  1),vector3.Vector( 1, -1,  1)),
        Vertex(vector3.Vector( 1,  1,  1),vector3.Vector( 1,  1,  1)),
    ]

    indices = [
        0,1,2,
        0,1,3,
        0,2,3,
        1,2,4,
        1,3,6,
        1,4,6,
        2,3,5,
        2,4,5,
        3,5,6,
        4,5,7,
        4,6,7,
        5,6,7
    ]

    m = Mesh('cube', indices, vertices, False)
    m.finish()
    return m

class Mesh(object):

    def __init__(self, name, indices, vertices, textures_enabled):
        """
        Initialize a mesh from its vertices and indices.

        Arguments:
        name -- the name of the mesh
        indices -- the indices of the vertices that make up each face.
        vertices -- the vertices for the 3D mesh
        textures_enabled -- whether the mesh uses textures
        """
        print 'Creating mesh for {}'.format(name)

        self.name = name

        self.triangles = []
        for i in xrange(0, len(indices), 3):
            a = indices[i + 0]
            b = indices[i + 1]
            c = indices[i + 2]

            self.triangles.append(Triangle(a, b, c))

        self.vertices = vertices
        self.textures_enabled = textures_enabled

        self.rotation = vector3.zero()
        self.position = vector3.zero()

    def merge(self, other):
        highest_index = len(self.vertices)

        other_triangles = map(lambda t: Triangle(t.a + highest_index, t.b + highest_index, t.c + highest_index), other.triangles)
        self.triangles += other_triangles
        self.vertices += other.vertices[:]

    def finish(self):
        print '- Created mesh with {} vertices and {} triangle triangles'.format(len(self.vertices), len(self.triangles))

        print 'Finishing up mesh:'
        self.__assign_vertices()
        self.__find_neighbors()
        self.__combine()

    def __assign_vertices(self):
        print '- Setting vertices for triangles'

        for triangle in self.triangles:
            va = self.vertices[triangle.a]
            vb = self.vertices[triangle.b]
            vc = self.vertices[triangle.c]
            triangle.set_vertices(va, vb, vc)

    def __find_neighbors(self):
        print '- Finding neighbors for triangles'

        for triangle in self.triangles:
            self.__find_neighbors_of(triangle)

    def __find_neighbors_of(self, original):
        for triangle in self.triangles:
            if triangle == original:
                continue

            indices = triangle.indices()
            if original.a in indices and original.b in indices:
                original.ab = triangle
            elif original.b in indices and original.c in indices:
                original.bc = triangle
            elif original.c in indices and original.a in indices:
                original.ca = triangle

            if original.ab is not None and original.bc is not None and original.ca is not None:
                break

    def __combine(self):
        print '- Combining triangles into triangle strips'
        strips = []
        visited = []

        for triangle in self.triangles:
            if triangle not in visited:
                queue = [triangle]
                current = TriangleStrip(triangle)

                while len(queue) > 0:
                    triangle = queue.pop(0)
                    visited.append(triangle)

                    for other in triangle.neighbors():
                        if triangle.can_be_combined_with(other):
                            current.append(other)

                            if other not in visited:
                                queue.append(other)

                strips.append(current)

        self.primitive = primitive.from_triangle_strips(strips)
        self.primitive.rotation = self.rotation
        self.primitive.position = self.position
