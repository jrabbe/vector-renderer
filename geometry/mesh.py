#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from math3d import vector3

import face

def cube():
    vertices = [
        vertex.Vertex(vector3.Vector(-1, -1, -1),vector3.Vector(-1, -1, -1)),
        vertex.Vertex(vector3.Vector( 1, -1, -1),vector3.Vector( 1, -1, -1)),
        vertex.Vertex(vector3.Vector(-1,  1, -1),vector3.Vector(-1,  1, -1)),
        vertex.Vertex(vector3.Vector(-1, -1,  1),vector3.Vector(-1, -1,  1)),
        vertex.Vertex(vector3.Vector( 1,  1, -1),vector3.Vector( 1,  1, -1)),
        vertex.Vertex(vector3.Vector(-1,  1,  1),vector3.Vector(-1,  1,  1)),
        vertex.Vertex(vector3.Vector( 1, -1,  1),vector3.Vector( 1, -1,  1)),
        vertex.Vertex(vector3.Vector( 1,  1,  1),vector3.Vector( 1,  1,  1)),
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

    return Mesh('cube', indices, vertices, False)

class Mesh(object):

    def __init__(self, name, indices, vertices, textures_enabled):
        """
        Initialize a mesh from its vertices and indices.

        Keyword arguments:
        name -- the name of the mesh
        indices -- the indices of the vertices that make up each face.
        vertices -- the vertices for the 3D mesh
        """
        self.name = name

        self.faces = []
        for i in xrange(0, len(indices), 3):
            a = indices[i + 0]
            b = indices[i + 1]
            c = indices[i + 2]

            self.faces.append(face.Face(a, b, c))

        self.vertices = vertices
        self.textures_enabled = textures_enabled

        self.rotation = vector3.zero()
        self.position = vector3.zero()

    def merge(self, other):
        highest_index = len(self.vertices)

        other_faces = map(lambda f: Face(f.a + highest_index, f.b + highest_index, f.c + highest_index),other.faces)
        self.faces += other_faces
        self.vertices += other.vertices[:]
