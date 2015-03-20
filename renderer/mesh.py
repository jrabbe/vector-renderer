#!/usr/bin/env python
# encoding: utf-8

import vector3

class Mesh:

    def __init__(self, name, vertex_count, index_count):
        self.name = name
        self.vertices = [None] * vertex_count
        self.indices = [None] * index_count
        self.rotation = vector3.Vector3()
        self.position = vector3.Vector3()
