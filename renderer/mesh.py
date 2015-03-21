#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import vector3

class Face(object):
    """
    A face is a triangle in the 3D mesh based on three vertex indices forming the corners of the
    polygon.
    """

    def __init__(self, a, b, c):
        """
        Initialize a new face from three vertex indices

        Keyword arguments:
        a -- the first vertex index
        b -- the second vertex index
        c -- the third vertex index
        """
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return '{A=' + str(self.a) + ' B=' + str(self.b) + ' C=' + str(self.c) + '}'


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

            self.faces.append(Face(a, b, c))

        print 'Created mesh ', name, ' with ', len(self.faces), ' faces'

        self.vertices = vertices
        self.textures_enabled = textures_enabled

        self.rotation = vector3.zero()
        self.position = vector3.zero()

    def merge(self, other):
        highest_index = len(self.vertices)
        print 'highest old index = ', highest_index

        other_faces = map(lambda f: Face(f.a + highest_index, f.b + highest_index, f.c + highest_index),other.faces)
        self.faces += other_faces
        self.vertices += other.vertices[:]

    def face_normal(self, face):
        """
        Calculate the face normal for the provided face. The normal is calculated as the average
        of the three vertex normals for the face

        face -- the face to calculate the normal for.
        """
        if face not in self.faces:
            return None

        normal_a = self.vertices[face.a].coordinates + self.vertices[face.a].normal
        normal_b = self.vertices[face.b].coordinates + self.vertices[face.b].normal
        normal_c = self.vertices[face.c].coordinates + self.vertices[face.c].normal

        return (normal_a + normal_b + normal_c).scale(1/3).normalize()
