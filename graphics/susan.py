#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import math

def apply(edge_buffer, get=lambda v: 255 * v.length()):
    """
    Calculates the SUSAN for each coordinate in the provided buffer.
    """
    corners = []
    radius = 4
    t = 10

    mask = find_circle_mask(0, 0, radius)
    a = len(mask)

    i = lambda x, y: x + y * self.screen_width
    valid = lambda i: i >= 0 and i < len(edge_buffer)

    R = [None] * (self.screen_width * self.screen_height)
    values = []

    for y in xrange(self.screen_height):
        for x in xrange(self.screen_width):
            c = i(x, y)
            if edge_buffer[c] is None:
                continue

            ic = get(edge_buffer[c])
            n = 0

            for x1, y1 in mask:
                p1 = i(x + x1, y + y1)
                i1 = get(edge_buffer[p1]) if valid(p1) and edge_buffer[p1] is not None else 0
                c1 = math.pow(math.e, -math.pow(((i1 - ic) / t), 6))
                n += c1

            values.append(n)
            R[c] = n

    # Calculate the geometric threshold: 1/2 max(n) for corners
    maxn = max(values)
    minn = min(values)
    g = 0.5 * max(values)

    # Constrain to the geometric threshold
    values = []
    for iR in xrange(len(R)):
        n = R[iR]
        if n is None:
            continue

        R[iR] = g - n if n < g else None
        if R[iR] is not None:
            values.append(R[iR])

    # normalize the output to the range 0.0-1.0
    maxr = max(values)
    minr = min(values)
    norm = lambda v: (v - minr) / (maxr - minr)
    for iR in xrange(len(R)):
        if R[iR] is None:
            continue

        R[iR] = norm(R[iR])

    print 'SUSAN in the range = {}-{} => g = {} => new range = {}-{}'.format(minn, maxn, g, min(values), max(values))
    return R

def find_circle_coords(x0, y0, radius):
    """
    Calculates coordinates for a Breshenham circle with the provided radius
    around the specified center.

    Arguments
    - x0 : x coordinate of center
    - y0 : y coordinate of center
    - radius : the radius of the circle
    """
    x = radius
    y = 0

    # Decision criterion divided by 2 evaluated at x=r, y=0
    decisionOver2 = 1 - x

    coords = []

    while x >= y:

        coords.append(( x + x0,  y + y0))
        coords.append(( y + x0,  x + y0))
        coords.append((-x + x0,  y + y0))
        coords.append((-y + x0,  x + y0))
        coords.append((-x + x0, -y + y0))
        coords.append((-y + x0, -x + y0))
        coords.append(( x + x0, -y + y0))
        coords.append(( y + x0, -x + y0))
        y += 1

        if decisionOver2 <= 0:
            # Change in decision criterion for y -> y+1
            decisionOver2 += 2 * y + 1
        else:
            x -= 1
            # Change for y -> y+1, x -> x-1
            decisionOver2 += 2 * (y - x) + 1

    return coords

def find_circle_mask(x0, y0, radius):
    """
    Finds the coordinates of a filled Breshenham circle with the provided radius
    around the specified center.

    Arguments
    - x0 : x coordinate of center
    - y0 : y coordinate of center
    - radius : the radius of the circle
    """
    coords = find_circle_coords(x0, y0, radius)

    q = [(x0, y0)]
    while len(q) > 0:
        x, y = q.pop(0)
        coords.append((x, y))

        if (x - 1, y) not in coords:
            q.append((x - 1, y))
        if (x + 1, y) not in coords:
            q.append((x + 1, y))
        if (x, y - 1) not in coords:
            q.append((x, y - 1))
        if (x, y + 1) not in coords:
            q.append((x, y + 1))

    return coords

