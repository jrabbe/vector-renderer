#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

class Projection(object):
    """
    A projection of a polygon into rendered 2D space.
    """

    def __init__(self, camera, coordinates, projected_z, normal, world_coordinates, world_normal, light_normal):
        self.camera = camera
        self.coordinates = coordinates
        self.projected_z = projected_z
        self.normal = normal
        self.world_coordinates = world_coordinates
        self.world_normal = world_normal
        self.light_normal = light_normal

    def __str__(self):
        return 'P[coordinates={} normal={}]'.format(self.coordinates, self.normal)

    def is_facing_camera(self):
        """
        Check if this projection is facing the camera or not
        """
        return (self.world_coordinates - self.camera.position).dot(self.world_normal) < 0
