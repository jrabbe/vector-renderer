#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import math
import matrix

class Quaternion(object):

    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def rotation_yaw_pitch_roll(self, yaw, pitch, roll):
        halfRoll = roll * 0.5
        halfPitch = pitch * 0.5
        halfYaw = yaw * 0.5
        sinRoll = math.sin(halfRoll)
        cosRoll = math.cos(halfRoll)
        sinPitch = math.sin(halfPitch)
        cosPitch = math.cos(halfPitch)
        sinYaw = math.sin(halfYaw)
        cosYaw = math.cos(halfYaw)

        result = Quaternion()
        result.x = (cosYaw * sinPitch * cosRoll) + (sinYaw * cosPitch * sinRoll)
        result.y = (sinYaw * cosPitch * cosRoll) - (cosYaw * sinPitch * sinRoll)
        result.z = (cosYaw * cosPitch * sinRoll) - (sinYaw * sinPitch * cosRoll)
        result.w = (cosYaw * cosPitch * cosRoll) + (sinYaw * sinPitch * sinRoll)

        return result

    def to_rotation_matrix(self):
        xx = self.x * self.x
        yy = self.y * self.y
        zz = self.z * self.z
        xy = self.x * self.y
        zw = self.z * self.w
        zx = self.z * self.x
        yw = self.y * self.w
        yz = self.y * self.z
        xw = self.x * self.w

        values = []
        values.append(1.0 - (2.0 * (yy + zz)))
        values.append(2.0 * (xy + zw))
        values.append(2.0 * (zx - yw))
        values.append(0)
        values.append(2.0 * (xy - zw))
        values.append(1.0 - (2.0 * (zz + xx)))
        values.append(2.0 * (yz + xw))
        values.append(0)
        values.append(2.0 * (zx + yw))
        values.append(2.0 * (yz - xw))
        values.append(1.0 - (2.0 * (yy + xx)))
        values.append(0)
        values.append(0)
        values.append(0)
        values.append(0)
        values.append(1.0)

        return matrix.Matrix.from_values(values)

