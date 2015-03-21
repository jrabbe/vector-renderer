#!/usr/bin/env python
# encoding: utf-8

import vector3

class Mesh:

    def __init__(self, name, vertex_count, index_count, textures_enabled):
        self.name = name
        self.__vertex_count = vertex_count
        self.__index_count = index_count
        self.textures_enabled = textures_enabled

        self.vertices = [None] * vertex_count
        self.normals = [None] * vertex_count
        self.textures = [None] * vertex_count
        self.indices = [None] * index_count

        self.rotation = vector3.Vector3()
        self.position = vector3.Vector3()
