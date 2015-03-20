#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import vector2
import vector3
import matrix

class Device:

    def __init__(self, screen_width, screen_height, filename):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.filename = filename
        self.output_buffer = []

    def draw_point(self, point):
        raise NotImplementedError

    def draw_line(self, point0, point1):
        raise NotImplementedError

    def draw_triangle(self, point0, point1, point2):
        raise NotImplementedError

    def begin_render(self):
        raise NotImplementedError

    def end_render(self):
        raise NotImplementedError

    def project(self, vertices, matrix):
        point = vertices.transform(matrix)

        x = int(point.x * self.screen_width + self.screen_width / 2.0)
        y = int(-point.y * self.screen_height + self.screen_height / 2.0)

        return vector2.Vector2(x, y)

    def render(self, camera, meshes):
        view_matrix = matrix.look_at_lh(camera.position, camera.target, vector3.up())
        projection_matrix = matrix.perspective_fov_lh(0.78, self.screen_width / self.screen_height, 0.01, 1.0)

        self.begin_render()

        for i in range(len(meshes)):
            mesh = meshes[i]
            rot = matrix.rotation_yaw_pitch_roll(mesh.rotation.y, mesh.rotation.x, mesh.rotation.z)
            tran = matrix.translation(mesh.position.x, mesh.position.y, mesh.position.z)
            world_matrix = rot * tran

            transformation_matrix = world_matrix * view_matrix * projection_matrix

            for vi in range(len(mesh.vertices)):
                point = self.project(mesh.vertices[vi], transformation_matrix)
                self.draw_point(point)

        self.end_render()

    def present(self):
        raise NotImplementedError

