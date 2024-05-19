#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import os

from math3d import vector3 as v3
from math3d import vector2 as v2

from .mesh import Mesh
from .vertex import Vertex
from .filebuffer import Filebuffer

class GeometryReader:

    def __init__(self, primitive_path):
        """
        Initialize the
        """
        self.__TEXTURE_COORDINATES_INCLUDED = 0x1
        self.primitive_path = primitive_path

    def read(self, part):
        print('Reading geometry for {}'.format(part))

        self.__buffer = bytearray()
        filepath = os.path.join(self.primitive_path, part + '.g')

        print('- reading base geometry from ', filepath)

        mesh = self.read_single_geometry(filepath, part)

        sub_part_index = 1
        while os.path.exists(filepath + str(sub_part_index)):
            print('- reading sub part from with index ', sub_part_index)

            sub_mesh = self.read_single_geometry(filepath + str(sub_part_index), part)
            mesh.merge(sub_mesh)
            sub_part_index += 1

        mesh.finish()

        return mesh

    def read_single_geometry(self, filepath, name):
        buf = Filebuffer(filepath)

        # Discarding first integer
        buf.getinteger()

        vertexcount = buf.getinteger()
        indexcount = buf.getinteger()

        options = buf.getinteger()
        textures_enabled = ((options & self.__TEXTURE_COORDINATES_INCLUDED) == self.__TEXTURE_COORDINATES_INCLUDED)

        coordinates = []
        normals = []
        textures = [None] * vertexcount

        indices = []

        # Get vertices
        for i in range(vertexcount):
            coordinates.append(v3.Vector(buf.getfloat(), buf.getfloat(), buf.getfloat()))

        # Get normals
        for i in range(vertexcount):
            normals.append(v3.Vector(buf.getfloat(), buf.getfloat(), buf.getfloat()))

        # Conditionally get textures
        if textures_enabled:
            textures = []
            for i in range(vertexcount):
                textures.append(v2.Vector(buf.getfloat(), buf.getfloat()))

        for i in range(indexcount):
            indices.append(buf.getinteger())

        vertices = list(map(lambda c, n, t: Vertex(c, n, t), coordinates, normals, textures))

        return Mesh(name, indices, vertices, textures_enabled)
