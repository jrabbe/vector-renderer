#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import math

from math3d import vector3

class ZMap(object):
    '''
    Map of the polygon in 2 dimension where each coordinate is the projected
    z coordinate.
    '''

    def __init__(self, polygon):
        '''

        Arguments:
        polygon -- The 2D polygon to create map for
        '''
        print 'Creating ZMap from {}'.format(polygon)

        self.x = polygon.x
        self.y = polygon.y
        self.width = polygon.width
        self.height = polygon.height
        self.m = [None] * (self.width * self.height)

        # TODO: go through and convert polygon to map setting each z value
        ps = []
        for v in polygon.vertices():
            x = v.x - self.x
            y = v.y - self.y
            self.set(x, y, v.z)
            print '- Setting corner at {}, {} with z = {}'.format(x, y, v.z)

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
            dz = p1.z - p0.z

            print '- Drawing line from {} => {}'.format(p0, p1)

            if dx == 0:
                # vertical
                x = p0.x
                z = p0.z
                for y in xrange(p0.y, p1.y, (-1 if dy  < 0 else 1)):
                    iy = (p1.y - y) / (p1.y - p0.y)
                    self.set(x, y, z + dz * iy)
            else:
                l = math.sqrt(math.pow(p1.x - p0.x, 2) + math.pow(p1.y - p0.y, 2))
                error = 0
                deltaerror = abs(dy / dx)

                y = p0.y
                z = p0.z
                for x in xrange(p0.x, p1.x):
                    dl = math.sqrt(math.pow(p1.x - x, 2) + math.pow(p1.y - y, 2))
                    self.set(x, y, z + dz * (dl/l))
                    error += deltaerror

                    while error >= 0.5:
                        dl = math.sqrt(math.pow(p1.x - x, 2) + math.pow(p1.y - y, 2))
                        self.set(x, y, z + dz * (dl/l))
                        y += -1 if dy < 0 else 1
                        error -= 1

        print '- Filling zmap'

        for y in xrange(self.height):
            startx = None
            startz = None
            inside = False

            for x in xrange(self.width):
                if self.is_set(x, y) and not inside:
                    startx = x
                    startz = self.get(x, y)
                elif not self.is_set(x, y) and startx is not None:
                    inside = True
                elif self.is_set(x, y) and inside:
                    inside = False

                    # paint back from here
                    z = self.get(x, y)
                    dz = (z - startz) / (x - startx)
                    for dx in xrange(x - 1, startx, -1):
                        z = z - dz
                        self.set(dx, y, z)


    def __str__(self):
        result = ''
        for i in xrange(len(self.m)):
            if i > 0 and i % self.width == 0:
                result += '\n'

            value = self.m[i]
            if value is None:
                result += '{:^7}'.format('-')
            else:
                result += '{: 7.4f}'.format((value - 1.0) * 1000)

        return result

    def overlap(self, other):
        """
        Finds the overlap, if any, of the polygon represented by this zmap
        compared to the other that is provided.
        """
        # First do simple rectangular overlap using x, y, width, and height
        if (self.x + self.width < other.x or self.x > other.x + other.width or
            self.y + self.height < other.y or self.y > other.y + other.height):
            return 0

        # iterate from min(x) -> max(x + width) and min(y) -> min(y + width)
        startx = min(self.x, other.x)
        endx = max(self.x + self.width, other.x + other.width)
        starty = min(self.y, other.y)
        endy = max(self.y + self.height, other.y + other.height)

        # print 'iterating from 0,0 -> {},{} (with start = {}, {})'.format(endx, endy, startx, starty)

        result = [None] * (endx * endy)

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
                    # if both are none they are equal
                    value = 0
                elif sz is None:
                    # if sz is None but oz is not, then oz is in front
                    value = -1
                elif oz is None:
                    #if sz is not None, but oz is, then sz is in front
                    value = 1
                else:
                    # if both values are set compare them
                    value = cmp(oz, sz)


                result[x + y * endx] = value

        covered = 0
        free = 0
        for i in xrange(len(result)):
            if result[i] == -1:
                covered += 1
            elif result[i] == -1:
                free += 1

        if free / self.area() > 0.5:
            return 1


        return sum(result)

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
        result = 0
        for i in xrange(len(self.m)):
            if self.m[i] is not None:
                result += 1

        return result

    def __i(self, x, y):
        return x + y * self.width

    def set(self, x, y, z):
        i = self.__i(x, y)
        self.m[i] = z

    def unset(self, x, y):
        i = self.__i(x, y)
        self.m[i] = None

    def get(self, x, y):
        i = self.__i(x, y)
        return self.m[i]

    def is_set(self, x, y):
        return self.get(x, y) is not None

    def valid(self, x, y):
        i = self.__i(x, y)
        return i >= 0 and i < len(self.m)

