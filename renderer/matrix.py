#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import math

def from_values(values):
    result = Matrix()
    # Copy the values
    result.m = values[:]
    return result

def rotation_x (angle):
    result = Matrix()
    s = math.sin(angle)
    c = math.cos(angle)
    result.m[0] = 1.0
    result.m[15] = 1.0
    result.m[5] = c
    result.m[10] = c
    result.m[9] = -s
    result.m[6] = s
    return result

def rotation_y(angle):
    result = Matrix()
    s = math.sin(angle)
    c = math.cos(angle)
    result.m[5] = 1.0
    result.m[15] = 1.0
    result.m[0] = c
    result.m[2] = -s
    result.m[8] = s
    result.m[10] = c
    return result

def rotation_z(angle):
    result = Matrix()
    s = math.sin(angle)
    c = math.cos(angle)
    result.m[10] = 1.0
    result.m[15] = 1.0
    result.m[0] = c
    result.m[1] = s
    result.m[4] = -s
    result.m[5] = c
    return result

def rotation_yaw_pitch_roll(yaw, pitch, roll):
    return rotation_z(roll) * rotation_x(pitch) * rotation_y(yaw);

def scaling(x, y, z):
    result = Matrix(identity=True)
    result.m[0] = x
    result.m[5] = y
    result.m[10] = z
    return result

def translation(x, y, z):
    result = Matrix(identity=True)
    result.m[12] = x
    result.m[13] = y
    result.m[14] = z
    return result

def look_at_lh(eye, target, up):
    z_axis = (target - eye).normalize()
    x_axis = up.cross(z_axis).normalize()
    y_axis = z_axis.cross(x_axis).normalize()

    ex = -x_axis.dot(eye)
    ey = -y_axis.dot(eye)
    ez = -z_axis.dot(eye)

    return from_values([x_axis.x, y_axis.x, z_axis.x, 0, x_axis.y, y_axis.y, z_axis.y, 0, x_axis.z, y_axis.z, z_axis.z, 0, ex, ey, ez, 1])

def perspective_lh(width, height, z_near, z_far):
    matrix = Matrix()
    matrix.m[0] = (2.0 * z_near) / width
    matrix.m[1] = matrix.m[2] = matrix.m[3] = 0.0
    matrix.m[5] = (2.0 * z_near) / height
    matrix.m[4] = matrix.m[6] = matrix.m[7] = 0.0
    matrix.m[10] = -z_far / (z_near - z_far)
    matrix.m[8] = matrix.m[9] = 0.0
    matrix.m[11] = 1.0
    matrix.m[12] = matrix.m[13] = matrix.m[15] = 0.0
    matrix.m[14] = (z_near * z_far) / (z_near - z_far)
    return matrix

def perspective_fov_lh(fov, aspect, z_near, z_far):
    result = Matrix()
    tan = 1.0 / (math.tan(fov * 0.5))
    result.m[0] = tan / aspect
    result.m[1] = result.m[2] = result.m[3] = 0.0
    result.m[5] = tan
    result.m[4] = result.m[6] = result.m[7] = 0.0
    result.m[8] = result.m[9] = 0.0
    result.m[10] = -z_far / (z_near - z_far)
    result.m[11] = 1.0
    result.m[12] = result.m[13] = result.m[15] = 0.0
    result.m[14] = (z_near * z_far) / (z_near - z_far)
    return result

def identity():
    return Matrix(identity=True)

def zero():
    return Matrix()

class Matrix(object):

    def __init__(self, identity=False):
        self.m = [0.0] * 16

        if identity:
            self.m[0] = 1.0
            self.m[5] = 1.0
            self.m[10] = 1.0
            self.m[15] = 1.0

    def __str__(self):
        return """
        {0[0]} {0[1]} {0[2]} {0[3]}
        {0[4]} {0[5]} {0[6]} {0[7]}
        {0[8]} {0[9]} {0[10]} {0[11]}
        {0[12]} {0[13]} {0[14]} {0[15]}
        """.format(self.m)

    def is_identity(self):
        if self.m[0] != 1.0 or self.m[5] != 1.0 or self.m[10] != 1.0 or self.m[15] != 1.0:
            return False

        if self.m[1] != 0.0 or self.m[2] != 0.0 or self.m[3] != 0.0 or self.m[4] != 0.0 or self.m[6] != 0.0 or self.m[7] != 0.0 or self.m[8] != 0.0 or self.m[9] != 0.0 or self.m[11] != 0.0 or self.m[12] != 0.0 or self.m[13] != 0.0 or self.m[14] != 0.0:
            return False

        return True

    def determinant(self):
        temp1 = (self.m[10] * self.m[15]) - (self.m[11] * self.m[14])
        temp2 = (self.m[9] * self.m[15]) - (self.m[11] * self.m[13])
        temp3 = (self.m[9] * self.m[14]) - (self.m[10] * self.m[13])
        temp4 = (self.m[8] * self.m[15]) - (self.m[11] * self.m[12])
        temp5 = (self.m[8] * self.m[14]) - (self.m[10] * self.m[12])
        temp6 = (self.m[8] * self.m[13]) - (self.m[9] * self.m[12])
        return ((((self.m[0] * (((self.m[5] * temp1) - (self.m[6] * temp2)) + (self.m[7] * temp3))) - (self.m[1] * (((self.m[4] * temp1) - (self.m[6] * temp4)) + (self.m[7] * temp5)))) + (self.m[2] * (((self.m[4] * temp2) - (self.m[5] * temp4)) + (self.m[7] * temp6)))) - (self.m[3] * (((self.m[4] * temp3) - (self.m[5] * temp5)) + (self.m[6] * temp6))))

    def to_array(self):
        return self.m

    def __invert__(self):
        l1 = self.m[0]
        l2 = self.m[1]
        l3 = self.m[2]
        l4 = self.m[3]
        l5 = self.m[4]
        l6 = self.m[5]
        l7 = self.m[6]
        l8 = self.m[7]
        l9 = self.m[8]
        l10 = self.m[9]
        l11 = self.m[10]
        l12 = self.m[11]
        l13 = self.m[12]
        l14 = self.m[13]
        l15 = self.m[14]
        l16 = self.m[15]
        l17 = (l11 * l16) - (l12 * l15)
        l18 = (l10 * l16) - (l12 * l14)
        l19 = (l10 * l15) - (l11 * l14)
        l20 = (l9 * l16) - (l12 * l13)
        l21 = (l9 * l15) - (l11 * l13)
        l22 = (l9 * l14) - (l10 * l13)
        l23 = ((l6 * l17) - (l7 * l18)) + (l8 * l19)
        l24 = -(((l5 * l17) - (l7 * l20)) + (l8 * l21))
        l25 = ((l5 * l18) - (l6 * l20)) + (l8 * l22)
        l26 = -(((l5 * l19) - (l6 * l21)) + (l7 * l22))
        l27 = 1.0 / ((((l1 * l23) + (l2 * l24)) + (l3 * l25)) + (l4 * l26))
        l28 = (l7 * l16) - (l8 * l15)
        l29 = (l6 * l16) - (l8 * l14)
        l30 = (l6 * l15) - (l7 * l14)
        l31 = (l5 * l16) - (l8 * l13)
        l32 = (l5 * l15) - (l7 * l13)
        l33 = (l5 * l14) - (l6 * l13)
        l34 = (l7 * l12) - (l8 * l11)
        l35 = (l6 * l12) - (l8 * l10)
        l36 = (l6 * l11) - (l7 * l10)
        l37 = (l5 * l12) - (l8 * l9)
        l38 = (l5 * l11) - (l7 * l9)
        l39 = (l5 * l10) - (l6 * l9)
        self.m[0] = l23 * l27
        self.m[4] = l24 * l27
        self.m[8] = l25 * l27
        self.m[12] = l26 * l27
        self.m[1] = -(((l2 * l17) - (l3 * l18)) + (l4 * l19)) * l27
        self.m[5] = (((l1 * l17) - (l3 * l20)) + (l4 * l21)) * l27
        self.m[9] = -(((l1 * l18) - (l2 * l20)) + (l4 * l22)) * l27
        self.m[13] = (((l1 * l19) - (l2 * l21)) + (l3 * l22)) * l27
        self.m[2] = (((l2 * l28) - (l3 * l29)) + (l4 * l30)) * l27
        self.m[6] = -(((l1 * l28) - (l3 * l31)) + (l4 * l32)) * l27
        self.m[10] = (((l1 * l29) - (l2 * l31)) + (l4 * l33)) * l27
        self.m[14] = -(((l1 * l30) - (l2 * l32)) + (l3 * l33)) * l27
        self.m[3] = -(((l2 * l34) - (l3 * l35)) + (l4 * l36)) * l27
        self.m[7] = (((l1 * l34) - (l3 * l37)) + (l4 * l38)) * l27
        self.m[11] = -(((l1 * l35) - (l2 * l37)) + (l4 * l39)) * l27
        self.m[15] = (((l1 * l36) - (l2 * l38)) + (l3 * l39)) * l27

    def __mul__(self, other):
        result = Matrix()

        result.m[0] = self.m[0] * other.m[0] + self.m[1] * other.m[4] + self.m[2] * other.m[8] + self.m[3] * other.m[12]
        result.m[1] = self.m[0] * other.m[1] + self.m[1] * other.m[5] + self.m[2] * other.m[9] + self.m[3] * other.m[13]
        result.m[2] = self.m[0] * other.m[2] + self.m[1] * other.m[6] + self.m[2] * other.m[10] + self.m[3] * other.m[14]
        result.m[3] = self.m[0] * other.m[3] + self.m[1] * other.m[7] + self.m[2] * other.m[11] + self.m[3] * other.m[15]
        result.m[4] = self.m[4] * other.m[0] + self.m[5] * other.m[4] + self.m[6] * other.m[8] + self.m[7] * other.m[12]
        result.m[5] = self.m[4] * other.m[1] + self.m[5] * other.m[5] + self.m[6] * other.m[9] + self.m[7] * other.m[13]
        result.m[6] = self.m[4] * other.m[2] + self.m[5] * other.m[6] + self.m[6] * other.m[10] + self.m[7] * other.m[14]
        result.m[7] = self.m[4] * other.m[3] + self.m[5] * other.m[7] + self.m[6] * other.m[11] + self.m[7] * other.m[15]
        result.m[8] = self.m[8] * other.m[0] + self.m[9] * other.m[4] + self.m[10] * other.m[8] + self.m[11] * other.m[12]
        result.m[9] = self.m[8] * other.m[1] + self.m[9] * other.m[5] + self.m[10] * other.m[9] + self.m[11] * other.m[13]
        result.m[10] = self.m[8] * other.m[2] + self.m[9] * other.m[6] + self.m[10] * other.m[10] + self.m[11] * other.m[14]
        result.m[11] = self.m[8] * other.m[3] + self.m[9] * other.m[7] + self.m[10] * other.m[11] + self.m[11] * other.m[15]
        result.m[12] = self.m[12] * other.m[0] + self.m[13] * other.m[4] + self.m[14] * other.m[8] + self.m[15] * other.m[12]
        result.m[13] = self.m[12] * other.m[1] + self.m[13] * other.m[5] + self.m[14] * other.m[9] + self.m[15] * other.m[13]
        result.m[14] = self.m[12] * other.m[2] + self.m[13] * other.m[6] + self.m[14] * other.m[10] + self.m[15] * other.m[14]
        result.m[15] = self.m[12] * other.m[3] + self.m[13] * other.m[7] + self.m[14] * other.m[11] + self.m[15] * other.m[15]

        return result

    def __eq__(self, other):
        return (self.m[0] == other.m[0] and self.m[1] == other.m[1] and self.m[2] == other.m[2] and
            self.m[3] == other.m[3] and self.m[4] == other.m[4] and self.m[5] == other.m[5] and
            self.m[6] == other.m[6] and self.m[7] == other.m[7] and self.m[8] == other.m[8] and
            self.m[9] == other.m[9] and self.m[10] == other.m[10] and self.m[11] == other.m[11] and
            self.m[12] == other.m[12] and self.m[13] == other.m[13] and self.m[14] == other.m[14] and
            self.m[15] == other.m[15]);


    def clone(self):
        return from_values(self.m)

    def transpose(self):
        result = Matrix()
        result.m[0] = self.m[0]
        result.m[1] = self.m[4]
        result.m[2] = self.m[8]
        result.m[3] = self.m[12]
        result.m[4] = self.m[1]
        result.m[5] = self.m[5]
        result.m[6] = self.m[9]
        result.m[7] = self.m[13]
        result.m[8] = self.m[2]
        result.m[9] = self.m[6]
        result.m[10] = self.m[10]
        result.m[11] = self.m[14]
        result.m[12] = self.m[3]
        result.m[13] = self.m[7]
        result.m[14] = self.m[11]
        result.m[15] = self.m[15]
        return result

