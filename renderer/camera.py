#!/usr/bin/env python
# encoding: utf-8

import vector3

class Camera:

    def __init__(self):
        self.position = vector3.Vector3()
        self.target = vector3.Vector3()
