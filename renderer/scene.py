#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

import matrix
import vector2 as v2
import vector3 as v3
import projection as p

class Scene(object):
    """
    The scene for the rendering, that is the camera, light, and projections.
    """

    def __init__(self, width, height, camera):
        self.width = width
        self.height = height
        self.camera = camera
        self.projection = matrix.perspective_fov_lh(0.78, width / height, 0.01, 1.0)
        self.z_buffer = [sys.maxint] * (width * height)
        self.light = v3.Vector3(0, 10, 10)

    def set_mesh(self, mesh):
        """
        Sets the mesh for the scene. Used to get the transformations on the mesh to be applied in the rendering.
        """
        rot = matrix.rotation_yaw_pitch_roll(mesh.rotation.y, mesh.rotation.x, mesh.rotation.z)
        tran = matrix.translation(mesh.position.x, mesh.position.y, mesh.position.z)
        self.world = rot * tran

        self.view = matrix.look_at_lh(self.camera.position, self.camera.target, v3.up())
        self.world_view = self.world * self.view
        self.transformation = self.world_view * self.projection

    def __constrain(self, point):
        """
        Constrains the provided point to the width and height set for the scene.
        This is done by scaling the x and y positions of the point.
        """
        x = int(point.x * self.width + self.width / 2.0)
        y = int(-point.y * self.height + self.height / 2.0)

        return v2.Vector2(x, y)

    def __compute_n_dot_l(self, coords, normal, light):
        """
        Computes the dot product of the light direction and the vertex normal.
        This computed value corresponds to the brightness of the vertex.

        """
        direction = light - coords
        n = v3.normalize(normal)
        d = v3.normalize(direction)

        return max(0, v3.dot(n, d))

    def project(self, vertex):
        """
        Project the vertex into the world and view
        """

        point = v2.to_vector(vertex.coordinates.transform(self.transformation))
        normal = v2.to_vector((vertex.normal + vertex.coordinates).transform(self.transformation))

        world_coords = vertex.coordinates.transform(self.world)
        world_normal = vertex.normal.transform(self.world)

        light_normal = self.__compute_n_dot_l(world_coords, world_normal, self.light)
        if light_normal > 1:
            print '!!! light_normal = ', light_normal

        return p.Projection(self.camera, self.__constrain(point), self.__constrain(normal), world_coords, world_normal, light_normal)
