#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from math3d import vector2

operators = {
    'sobel': ([-1, -2, -1, 0, 0, 0, 1, 2, 1], [-1, 0, 1, -2, 0, 2, -1, 0, 1]),
    'scharr': ([3, 10, 3, 0, 0, 0, -3, -10, -3],[3, 0, -3, 10, 0, -10, 3, 0, -3]),
    'prewitt': ([-1, -1, -1, 0, 0, 0, 1, 1, 1], [-1, 0, 1, -1, 0, 1, -1, 0, 1])
}

# luminance abs     : gs = lambda normal: 0.21 * abs(normal.x) + 0.72 * abs(normal.y) + 0.07 * abs(normal.z)
# lightness abs     : gs = lambda normal: (max(abs(normal.x), abs(normal.y), abs(normal.z)) + min(abs(normal.x), abs(normal.y), abs(normal.z))) / 2
# average abs       : gs = lambda normal: (abs(normal.x) + abs(normal.y) + abs(normal.z)) / 3
# luminance 1-minus : gs = lambda normal: 0.21 * (1 - normal.x) / 2 + 0.72 * (1 - normal.y) / 2 + 0.07 * (1 - normal.z) / 2
# lightness 1-minus : gs = lambda normal: (max((1 - normal.x) / 2, (1 - normal.y) / 2, (1 - normal.z) / 2) + min((1 - normal.x) / 2, (1 - normal.y) / 2, (1 - normal.z) / 2)) / 2
# average 1-minus   : gs = lambda normal: ((1 - normal.x) / 2 + (1 - normal.y) / 2 + (1 - normal.z) / 2) / 3

def identity(val):
    return val

def abs_luminance(normal):
    return 0.21 * abs(normal.x) + 0.72 * abs(normal.y) + 0.07 * abs(normal.z)

def abs_lightness(normal):
    return (max(abs(normal.x), abs(normal.y), abs(normal.z)) + min(abs(normal.x), abs(normal.y), abs(normal.z))) / 2

def abs_average(normal):
    return (abs(normal.x) + abs(normal.y) + abs(normal.z)) / 3

def minus_luminance(normal):
    return 0.21 * (1 - normal.x) / 2 + 0.72 * (1 - normal.y) / 2 + 0.07 * (1 - normal.z) / 2

def minus_lightness(normal):
    return (max((1 - normal.x) / 2, (1 - normal.y) / 2, (1 - normal.z) / 2) + min((1 - normal.x) / 2, (1 - normal.y) / 2, (1 - normal.z) / 2)) / 2

def minus_average():
    return ((1 - normal.x) / 2 + (1 - normal.y) / 2 + (1 - normal.z) / 2) / 3

def apply(buf, w, h, gs=None, operator='sobel'):
    """
    Finds the edges of the image in the provided buffer with the specified width (w)
    and height (h). The buffer is expected to contain a 3D vector with x, y, and z
    coordinates, but the gs argument can be used to specify a getter function for
    other types of values.

    The default getter uses luminance (0.21 * R + 0.72 * G + 0.07 * B) to calculate
    the greyscale value for finding the edges. This can also be changed by providing
    a different getter. Other alternatives is lightness ((max(R, G, B) + min(R, G, B)) / 2)
    and average ((R + G + B) / 3)

    Arguments
    - buf : the image buffer
    - w : width of the image buffer
    - h : heigth of the image buffer
    - gs : getter function
    - operator : the operator to use, can be 'sobel', 'scharr', or 'prewitt'.
    """
    G = [None] * (w * h)

    i = lambda x, y: x + y * w
    if gs is None:
        gs = lambda normal: 0.21 * abs(normal.x) + 0.72 * abs(normal.y) + 0.07 * abs(normal.z)

    gvx, gvy = operators[operator]

    for y in xrange(h):
        for x in xrange(w):
            ixy = i(x, y)

            if buf[ixy] is None:
                continue

            i1 = i(x-1, y-1)
            i2 = i(x-1, y)
            i3 = i(x-1, y+1)
            i4 = i(x, y-1)
            i5 = i(x, y)
            i6 = i(x, y+1)
            i7 = i(x+1, y-1)
            i8 = i(x+1, y)
            i9 = i(x+1, y+1)

            v = []
            v.append(gs(buf[i1]) if (i1 >= 0 and i1 < len(buf)) and buf[i1] is not None else 0)
            v.append(gs(buf[i2]) if (i2 >= 0 and i2 < len(buf)) and buf[i2] is not None else 0)
            v.append(gs(buf[i3]) if (i3 >= 0 and i3 < len(buf)) and buf[i3] is not None else 0)
            v.append(gs(buf[i4]) if (i4 >= 0 and i4 < len(buf)) and buf[i4] is not None else 0)
            v.append(gs(buf[i5]) if (i5 >= 0 and i5 < len(buf)) and buf[i5] is not None else 0)
            v.append(gs(buf[i6]) if (i6 >= 0 and i6 < len(buf)) and buf[i6] is not None else 0)
            v.append(gs(buf[i7]) if (i7 >= 0 and i7 < len(buf)) and buf[i7] is not None else 0)
            v.append(gs(buf[i8]) if (i8 >= 0 and i8 < len(buf)) and buf[i8] is not None else 0)
            v.append(gs(buf[i9]) if (i9 >= 0 and i9 < len(buf)) and buf[i9] is not None else 0)

            sgx = sum(map(lambda (a, b): a * b, zip(v, gvx)))
            sgy = sum(map(lambda (a, b): a * b, zip(v, gvy)))

            if sgx != 0 or sgy != 0:
                G[ixy] = vector2.create(sgx, sgy).normalize()

    return G
