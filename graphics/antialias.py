#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from renderer import color4

def apply(buf, width, height):
    out = [None] * (width * height)

    for y in xrange(height):
        for x in xrange(width):
            out[x + y * width] = handle_pixel(buf, x, y, width)

    return out

def handle_pixel(buf, x, y, width):
    c_ne = get_pixel(buf, x - 1, y - 1, width)
    c_n = get_pixel(buf, x, y - 1, width)
    c_nw = get_pixel(buf, x + 1, y - 1, width)
    c_e = get_pixel(buf, x - 1, y, width)
    c_m = get_pixel(buf, x, y, width)
    c_w = get_pixel(buf, x + 1, y, width)
    c_se = get_pixel(buf, x - 1, y + 1, width)
    c_s = get_pixel(buf, x, y + 1, width)
    c_sw = get_pixel(buf, x + 1, y + 1, width)

    c_avg = color4.average(c_ne, c_n, c_nw, c_e, c_m, c_w, c_se, c_s, c_sw)

    return c_avg

def get_pixel(buf, x, y, width):
    i = x + y * width
    if i < 0 or i >= len(buf):
        return None

    return buf[i]
