#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

class Projection(object):
    """
    A projection of a polygon into rendered 2D space.
    """

    def __init__(self, camera, coordinates, projected_z, normal, brightness, is_facing_camera):
        '''

        '''
        self.camera = camera
        self.coordinates = coordinates
        self.projected_z = projected_z
        self.normal = normal
        self.brightness = brightness
        self.is_facing_camera = is_facing_camera

    def __str__(self):
        return 'P[coordinates={} normal={}]'.format(self.coordinates, self.normal)
