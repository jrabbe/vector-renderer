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

    def __init__(self, name, indices, vertices, normals, textures=None):
        """
        Initialize a mesh from its vertices, vertex normals, vertex textures, and indices.

        Keyword arguments:
        name -- the name of the mesh
        indices -- the indices of the vertices that make up each face.
        vertices -- the vertices for the 3D mesh
        normals -- the vertex normals for the 3D mesh
        textures -- the textures for each vertex of the 3D mesh (default: None)
        """
        self.name = name
        self.textures_enabled = textures is not None

        self.faces = []
        for i in xrange(0, len(indices), 3):
            a = indices[i + 0]
            b = indices[i + 1]
            c = indices[i + 2]

            self.faces.append(Face(a, b, c))

        self.vertices = vertices
        self.normals = normals
        self.textures = textures

        self.rotation = vector3.Vector3()
        self.position = vector3.Vector3()

    def face_normal(self, face):
        """
        Calculate the face normal for the provided face. The normal is calculated as the average
        of the three vertex normals for the face

        face -- the face to calculate the normal for.
        """
        if face not in self.faces:
            return None

        normal_a = self.normals[face.a]
        normal_b = self.normals[face.b]
        normal_c = self.normals[face.c]

        return (normal_a + normal_b + normal_c).scale(1/3).normalize()
