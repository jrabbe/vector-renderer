#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import vector3

class Camera:

    def __init__(self):
        self.position = vector3.Vector3()
        self.target = vector3.Vector3()
