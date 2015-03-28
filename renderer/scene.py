#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

import matrix
import vector2 as v2
import vector3 as v3

class Projection(object):
    """
    """

    def __init__(self, camera, coordinates, normal, world_coordinates, world_normal):
        self.camera = camera
        self.coordinates = coordinates
        self.normal = normal
        self.world_coordinates = world_coordinates
        self.world_normal = world_normal

    def is_facing_camera(self):
        """
        """
        return (self.world_coordinates - self.camera.position).dot(self.world_normal) < 0


class Scene(object):
    """
    """

    def __init__(self, width, height, camera):
        self.width = width
        self.height = height
        self.camera = camera
        self.projection = matrix.perspective_fov_lh(0.78, width / height, 0.01, 1.0)
        self.z_buffer = [sys.maxint] * (width * height)

    def set_mesh(self, mesh):
        """
        """
        rot = matrix.rotation_yaw_pitch_roll(mesh.rotation.y, mesh.rotation.x, mesh.rotation.z)
        tran = matrix.translation(mesh.position.x, mesh.position.y, mesh.position.z)
        self.world = rot * tran

        self.view = matrix.look_at_lh(self.camera.position, self.camera.target, v3.up())
        self.world_view = self.world * self.view
        self.transformation = self.world_view * self.projection

    def __constrain(self, point):
        """
        """
        x = int(point.x * self.width + self.width / 2.0)
        y = int(-point.y * self.height + self.height / 2.0)

        return v3.Vector3(x, y, point.z)


    def project(self, vertex):
        """
        Project the vertex into the world and view
        """

        point = vertex.coordinates.transform(self.transformation)
        normal = (vertex.normal + vertex.coordinates).transform(self.transformation)

        world_coords = vertex.coordinates.transform(self.world)
        world_normal = vertex.normal.transform(self.world)

        return Projection(self.camera, self.__constrain(point), self.__constrain(normal), world_coords, world_normal)
