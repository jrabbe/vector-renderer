#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import vector3 as v3

class Vertex:
    """
    Describes a vertex as its coordinates, normal, and texture.
    """

    def __init__(self, coordinates=v3.zero(), normal=v3.zero(), texture=None):
        self.coordinates = coordinates
        self.normal = normal
        self.texture = texture

    def __str__(self):
        return '[coordinates={} normal={} texture={}]'.format(self.coordinates, self.normal, self.texture)
