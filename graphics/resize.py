#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

def apply(buf, original_width, original_height, width, heigth):
    x_ratio = original_width / width
    y_ratio = original_height / heigth

    output = [None] * (width * heigth)

    if int(round(x_ratio / 2)) == 1 and int(round(y_ratio / 2)) == 1:
        # No resizing necessary/possiblel
        return buf

    i = lambda x, y: x + y * width
    original_i = lambda x, y: x + y * original_width
    original_valid = lambda i: i >= 0 and i < len(buf)

    for y in xrange(height):
        for x in xrange(width):

            v = (0, 0, 0, 0)

            original_x = int(round(x * x_ratio))
            x_offset = int(round(x_ratio / 2))
            original_y = int(round(y * y_ratio))
            y_offset = int(round(y_ratio / 2))
            for dy in xrange(-y_offset, y_offset):
                for dx in xrange(-x_offset, x_offset):

                    oi = original_i(original_x + dx, original_y + dy)
                    if not original_valid(oi):
                        continue

                    percent_x = 1 - (dx / x_offset)
                    percent_y = 1 - (dy / y_offset)
                    percent = percent_x * percent_y

                    ov = buf[oi]
                    if ov is None:

                    elif len(ov) == 3:
                        ov = (*ov, 255)





