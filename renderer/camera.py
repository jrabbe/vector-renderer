#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from math3d import vector3

class Camera:

    def __init__(self):
        self.position = vector3.Vector()
        self.target = vector3.Vector()
