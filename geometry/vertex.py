#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from math3d import vector3

class Vertex:
    """
    Describes a vertex as its coordinates, normal, and texture.
    """

    def __init__(self, coordinates=vector3.zero(), normal=vector3.zero(), texture=None):
        self.coordinates = coordinates
        self.normal = normal
        self.texture = texture

    def __str__(self):
        return '[coordinates={self.coordinates} normal={self.normal} texture={self.texture}]'.format(self=self)
