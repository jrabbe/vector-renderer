#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys

from math3d import matrix4 as m4
from math3d import vector2 as v2
from math3d import vector3 as v3

import projection as p

class Scene(object):
    """
    The scene for the rendering, that is the camera, light, and projections.
    """

    def __init__(self, width, height, camera):
        self.width = width
        self.height = height
        self.camera = camera
        self.projection = m4.perspective_fov_lh(0.78, width / height, 0.01, 1.0)
        self.z_buffer = [sys.maxint] * (width * height)
        self.light = v3.Vector(0, 10, 10)

    def set_rotation_translation(self, rotation, translation):
        rot = m4.rotation_yaw_pitch_roll(rotation.y, rotation.x, rotation.z)
        tran = m4.translation(translation.x, translation.y, translation.z)
        self.__initialize(rot, tran)

    def __initialize(self, rot, tran):
        self.world = rot * tran

        self.view = m4.look_at_lh(self.camera.position, self.camera.target, v3.up())
        self.world_view = self.world * self.view
        self.transformation = self.world_view * self.projection

    def __constrain(self, point, z=None):
        """
        Constrains the provided point to the width and height set for the scene.
        This is done by scaling the x and y positions of the point.
        """
        x = int(point.x * self.width + self.width / 2.0)
        y = int(-point.y * self.height + self.height / 2.0)

        if z is None:
            return v2.Vector(x, y)
        else:
            return v3.Vector(x, y, z)

    def __compute_brightness(self, coords, normal, light):
        """
        Computes the brightness as the dot product of the light direction and
        the vertex normal.
        The light is an omnidirectional light with a position in the world
        coordinates, and no falloff from a brightness of 1.
        """
        direction = light - coords
        return max(0, v3.dot(v3.normalize(normal), v3.normalize(direction)))

    def __is_facing_camera(self, coords, normal, camera):
        direction = coords - camera
        return v3.dot(v3.normalize(normal), v3.normalize(direction)) < 0

    def project(self, vertex):
        """
        Project the vertex into the world and view
        """

        point = vertex.coordinates.transform(self.transformation)
        normal = (vertex.normal + vertex.coordinates).transform(self.transformation)

        world_coords = vertex.coordinates.transform(self.world)
        world_normal = vertex.normal.transform(self.world)

        view_coords = vertex.coordinates.transform(self.world_view)

        is_facing_camera = self.__is_facing_camera(world_coords, world_normal, self.camera.position)
        brightness = self.__compute_brightness(world_coords, world_normal, self.light)
        if brightness > 1:
            # It can never be brighter than brightest
            brightness = 1

        proj = p.Projection(self.camera, self.__constrain(point), world_coords.z, self.__constrain(normal), brightness, is_facing_camera)
        proj.world = world_coords
        proj.view = view_coords
        proj.world_y = world_coords.y
        return proj

    def simple_project(self, vertex):
        point = vertex.coordinates.transform(self.transformation)
        return self.__constrain(point, point.z)
