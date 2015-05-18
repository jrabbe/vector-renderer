#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import math
from PIL import Image, ImageDraw

from math3d import vector3
from math3d.coordinatematrix import CoordinateMatrix

def drawimage(name, width, height, buf):
    image = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(image)
    for y in xrange(height):
        for x in xrange(width):
                i = x + y * width
                xy = [(x, y)]
                c = 0
                if buf[i] is not None:
                    c = int(round(255 * buf[i]))
                pc = (c, c, c, 255)
                draw.point(xy, pc)

    del draw
    with open('files/output/depth/' + name + '.png', 'w') as f:
        image.save(f, 'PNG')


def from_triangle(vertices):
    minx = min(map(lambda v: v.x, vertices))
    width = max(map(lambda p: p.x, vertices)) - minx + 1
    miny = min(map(lambda p: p.y, vertices))
    height = max(map(lambda p: p.y, vertices)) - miny + 1

    ps = []
    m = CoordinateMatrix(minx, miny, width, height)
    v1, v2, v3 = vertices

    if v1.y > v2.y:
        v1, v2 = v2, v1

    if v2.y > v3.y:
        v2, v3 = v3, v2

    if v1.y > v2.y:
        v1, v2 = v2, v1

    d12 = (v2.x - v1.x) / (v2.y - v1.y) if v2.y - v1.y > 0 else 0
    d13 = (v3.x - v1.x) / (v3.y - v1.y) if v3.y - v1.y > 0 else 0

    if d12 > d13:
        for y in xrange(v1.y, v3.y):
            if y < v2.y:
                line = process_scanline(m, y, v1, v3, v1, v2)
            else:
                process_scanline(m, y, v1, v3, v2, v3)
    else:
        for y in xrange(v1.y, v3.y):
            if y < v2.y:
                process_scanline(m, y, v1, v2, v1, v3)
            else:
                process_scanline(m, y, v2, v3, v1, v3)

    return ZMap(m)

def process_scanline(m, y, va, vb, vc, vd):
    gradient1 = (y - va.y) / (vb.y - va.y) if va.y != vb.y else 0
    gradient2 = (y - vc.y) / (vd.y - vc.y) if vc.y != vd.y else 0

    interpolate = lambda mini, maxi, grad: mini + (maxi - mini) * max(0, min(grad, 1))

    sx = int(interpolate(va.x, vb.x, gradient1))
    ex = int(interpolate(vc.x, vd.x, gradient2))

    z1 = interpolate(va.z, vb.z, gradient1)
    z2 = interpolate(vc.z, vd.z, gradient2)

    for x in xrange(sx, ex):
        gradient = (x - sx) / (ex - sx)
        z = interpolate(z1, z2, gradient)
        m.set(x, y, z)

def from_polygon(polygon, mindepth=None, maxdepth=None):
    '''

    Arguments:
    polygon -- The 2D polygon to create map for
    '''
    # print 'Creating ZMap from {}'.format(polygon)

    sx = polygon.x
    sy = polygon.y
    width = polygon.width
    height = polygon.height
    m = CoordinateMatrix(sx, sy, width, height)
    interpolate = lambda z: (z - mindepth) / (maxdepth - mindepth)

    # TODO: go through and convert polygon to map setting each z value
    ps = []
    for v in polygon.vertices():
        x = v.x - sx
        y = v.y - sy
        z = interpolate(v.z)
        m.set(x, y, z, offset=False)
        # print '- Setting corner at {}, {} with z = {}'.format(x, y, v.z)

        drawimage('{}-points'.format(polygon), width, height, m)

        ps.append(vector3.Vector(x, y, v.z))

    # Draw the lines
    for a in xrange(len(ps)):
        p0 = ps[a]
        p1 = ps[(a + 1) % len(ps)]

        # Ensure 0 & 1 are ordered by x
        if p0.x > p1.x:
            p0, p1 = p1, p0

        dx = p1.x - p0.x
        dy = p1.y - p0.y
        dz = interpolate(p1.z) - interpolate(p0.z)

        # print '- Drawing line from {} => {}'.format(p0, p1)

        if dx == 0:
            # vertical
            x = p0.x
            z = interpolate(p0.z)
            for y in xrange(p0.y, p1.y, (-1 if dy  < 0 else 1)):
                iy = (p1.y - y) / (p1.y - p0.y)
                m.set(x, y, z + dz * iy, offset=False)
        else:
            l = math.sqrt(math.pow(p1.x - p0.x, 2) + math.pow(p1.y - p0.y, 2))
            error = 0
            deltaerror = abs(dy / dx)

            y = p0.y
            z = interpolate(p0.z)
            for x in xrange(p0.x, p1.x):
                dl = math.sqrt(math.pow(p1.x - x, 2) + math.pow(p1.y - y, 2))
                m.set(x, y, z + dz * (dl/l) * (-1 if dz < 0 else 1), offset=False)
                error += deltaerror

                while error >= 0.5:
                    dl = math.sqrt(math.pow(p1.x - x, 2) + math.pow(p1.y - y, 2))
                    m.set(x, y, z + dz * (dl/l) * (-1 if dz < 0 else 1), offset=False)
                    y += -1 if dy < 0 else 1
                    error -= 1

    drawimage('{}-line'.format(polygon), width, height, m)

    # print '- Filling zmap'

    for y in xrange(height):
        startx = None
        startz = None
        inside = False

        for x in xrange(self.width):
            if m.get(x, y, offset=False) is not None and not inside:
                startx = x
                startz = m[__i(x, y)]
            elif m.get(x, y, offset=False) is None and startx is not None:
                inside = True
            elif m.get(x, y, offset=False) is not None and inside:
                inside = False

                # paint back from here
                z = m.get(x, y, offset=False)
                dz = (z - startz) / (x - startx)
                for dx in xrange(x - 1, startx, -1):
                    z = z - dz
                    m[__i(dx, y)] = z
                    m.set(dx, y, z, offset=False)

    drawimage('{}-filled'.format(polygon), width, height, m)
    return ZMap(m)

class ZMap(object):
    '''
    Map of the polygon in 2 dimension where each coordinate is the projected
    z coordinate.
    '''

    def __init__(self, m):
        self.m = m
        self.x = m.x
        self.y = m.y
        self.width = m.width
        self.height = m.height

    def __str__(self):
        result = ''
        for y in xrange(self.height):
            for x in xrange(self.width):
                value = self.m.get(x, y, offset=False)
                if value is None:
                    result += '{:^7}'.format('-')
                else:
                    result += '{: 7.4f}'.format((value - 1.0) * 1000)

            result += '\n'

        return result

    def __add__(self, other):
        return ZMap(self.m + other.m)

    def clone(self):
        return ZMap(self.m.clone())

    def comparison_values(self, depthpart, ypart):
        count = 0
        total = 0
        for y in xrange(self.height):
            for x in xrange(self.width):
                z = self.get(x, y)
                if z is not None:
                    count += 1
                    total += ypart(y + self.y) + depthpart(z)

        return total / count

    def detailed_overlap(self, other):
        area = self.area()

        # First do simple rectangular overlap using x, y, width, and height
        if (self.x + self.width < other.x or self.x > other.x + other.width or
            self.y + self.height < other.y or self.y > other.y + other.height):
            return (area, 0, area)

        # iterate from min(x) -> max(x + width) and min(y) -> min(y + width)
        startx = min(self.x, other.x)
        endx = max(self.x + self.width, other.x + other.width)
        starty = min(self.y, other.y)
        endy = max(self.y + self.height, other.y + other.height)

        # print 'iterating from 0,0 -> {},{} (with start = {}, {})'.format(endx, endy, startx, starty)

        result = [None] * (endx * endy)
        free = 0
        covered = 0

        for y in xrange(endy):
            for x in xrange(endx):
                sz = None
                oz = None

                # print 'checking {}, {}'.format(x, y)

                if self.in_bounds(x, y):
                    sx = x - self.x
                    sy = y - self.y
                    # print 'getting self for {}, {}'.format(sx, sy)
                    sz = self.get(sx, sy)

                if other.in_bounds(x, y):
                    ox = x - other.x
                    oy = y - other.y
                    # print 'getting other for {}, {}'.format(ox, oy)
                    oz = other.get(ox, oy)

                value = None
                if sz is None and oz is None:
                    continue

                if sz is None:
                    # if sz is None but oz is not, then oz is in front
                    value = 'o'
                elif oz is None:
                    #if sz is not None, but oz is, then sz is in front
                    value = 's'
                    free += 1
                else:
                    # if both values are set compare them
                    if cmp(oz, sz) >= 0:
                        # oz is larger
                        value = 'so'
                        free += 1
                    else:
                        value = 'os'
                        covered +=1

                result[x + y * endx] = value

        return (free, covered, area)

    def overlap(self, other):
        """
        Finds the overlap, if any, of the polygon represented by this zmap
        compared to the other that is provided.
        """
        # First do simple rectangular overlap using x, y, width, and height
        if (self.x + self.width < other.x or self.x > other.x + other.width or
            self.y + self.height < other.y or self.y > other.y + other.height):

            mins, maxs = self.m.bounds()
            mino, maxo = other.m.bounds()

            if mins > mino:
                return -1
            elif maxs < maxo:
                return 1
            else:
                return 0

        free, covered, area = self.detailed_overlap(other)
        return free - covered

    def in_bounds(self, x, y):
        return (x >= self.x and x < self.x + self.width and
                y >= self.y and y < self.y + self.height)

    def global_to_local(self, x, y):
        """
        Converts the provided x and y coordinates from global to local
        coordinates. Note that there is no error checking done, so the returned
        coordinates may be outside the bounds of the zmap.
        """
        return (x - self.x, y - self.y)

    def boundingarea(self):
        """
        The rectangle area that is guaranteed to surround the polygon making up
        this zmap.
        """
        return self.width * self.height

    def area(self):
        """
        The true area of the polygon making up this zmap
        """
        return self.m.set_count()

    def is_set(self, x, y):
        return self.get(x, y) is not None

    def set(self, x, y, z):
        self.m.set(x, y, z, offset=False)

    def unset(self, x, y):
        self.m.set(x, y, None, offset=False)

    def get(self, x, y):
        return self.m.get(x, y, offset=False)

    def valid(self, x, y):
        return self.m.valid(x, y, offset=False)

