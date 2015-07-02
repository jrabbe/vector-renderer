#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import math

def apply(source, w, h, r):
    """
    Applies Gaussian blur to the provided source buffer. The buffer is expected
    to be an array containing values in the range 0.0-1.0 for each coordinate
    in the width * height (w * h)

    Algorithm from http://blog.ivank.net/fastest-gaussian-blur.html

    Arguments
    - source : the source buffer
    - w : the width of the source buffer
    - h : the height of the source buffer
    - r : the radius of the blur
    """
    i = lambda x, y: x + y * w
    sigma = r
    n = 3

    wIdeal = math.sqrt((12 * sigma * sigma / n)+1)
    wl = math.floor(wIdeal)
    if  wl % 2 == 0:
        wl -= 1

    wu = wl + 2

    mIdeal = (12 * sigma * sigma - n * wl * wl - 4 * n * wl - 3 * n) / (-4 * wl - 4)
    m = round(mIdeal)

    boxes = []
    for idx in xrange(n):
        boxes.append(wl if i < m else wu);

    print '-- blurring for radius = {}, have boxes = {}'.format(r, boxes)

    i1 = self.box_blur(source, w, h, int(round((boxes[0] - 1) / 2)))
    i2 = self.box_blur(i1, w, h, int(round((boxes[1] - 1) / 2)))
    i3 = self.box_blur(i2, w, h, int(round((boxes[2] - 1) / 2)))

    return i3

def box_blur(self, source, w, h, r):
    intermediary = self.box_blur_H(source, w, h, r)
    result = self.box_blur_T(intermediary, w, h, r)
    return result

def box_blur_H(self, source, w, h, r):
    result = [1] * (w * h)
    iarr = 1 / ( r + r + 1)
    for i in xrange(h):
        ti = i * w
        li = ti
        ri = ti + r
        fv = source[ti]
        lv = source[ti + w - 1]
        val = (r + 1) * fv

        for j in xrange(r):
            val += source[ti + j]

        for j in xrange(r + 1):
            val += source[ri] - fv
            result[ti] = (val * iarr)
            ri += 1
            ti += 1

        for j in xrange(r + 1, w - r):
            val += source[ri] - source[li]
            result[ti] = (val * iarr)
            li += 1
            ri += 1
            ti += 1

        for j in xrange(w - r, w):
            val += lv - source[li]
            result[ti] = (val * iarr)
            li += 1
            ti += 1

    return result

def box_blur_T(self, source, w, h, r):
    result = [1] * (w * h)
    iarr = 1 / (r + r + 1)
    for i in xrange(w):
        ti = i
        li = ti
        ri = ti + r * w
        fv = source[ti]
        lv = source[ti + w * (h - 1)]
        val = (r + 1) * fv

        for j in xrange(r):
            val += source[ti + j * w]

        for j in xrange(r + 1):
            val += source[ri] - fv
            result[ti] = (val * iarr)
            ri += w
            ti += w

        for j in xrange(r + 1, h - r):
            val += source[ri] - source[li]
            result[ti] = (val * iarr)
            li += w
            ri += w
            ti += w

        for j in xrange(h - r, h):
            val += lv - source[li]
            result[ti] = (val * iarr)
            li += w
            ti += w

    return result
