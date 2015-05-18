#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

class CoordinateMatrix(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.m = [None] * (width * height)

    def __add__(self, other):
        nx = min(self.x, other.x)
        ny = min(self.y, other.y)
        width = max(self.x - nx + self.width, other.x - nx + other.width)
        height = max(self.y - ny + self.height, other.y - ny + other.height)

        m = CoordinateMatrix(nx, ny, width, height)
        for y in xrange(self.height):
            for x in xrange(self.width):
                cx = x + self.x
                cy = y + self.y
                z = self.get(x, y, offset=False)
                if z is not None:
                    m.set(cx, cy, z)

        for y in xrange(other.height):
            for x in xrange(other.width):
                cx = x + other.x
                cy = y + other.y
                z = other.get(x, y, offset=False)
                if z is not None:
                    m.set(cx, cy, z)

        return m

    def clone(self):
        m = CoordinateMatrix(self.x, self.y, self.width, self.height)
        m.m = self.m[:]
        return m

    def __str__(self):
        result = ''
        for y in xrange(self.height):
            for x in xrange(self.width):
                value = self.m[self.__i(x, y)]
                if value is None:
                    result += '{:^7}'.format('-')
                else:
                    result += '{: 7.4f}'.format((value - 1.0) * 1000)

            result += '\n'

        return result

    def average(self):
        count = 0
        total = 0
        for i in xrange(len(self.m)):
            if self.m[i] is not None:
                total += self.m[i]
                count += 1

        return total / count

    def bounds(self):
        values = []
        for i in xrange(len(self.m)):
            if self.m[i] is not None:
                values.append(self.m[i])

        return (min(values), max(values))

    def valid(self, x, y, offset=True):
        if offset:
            x = x - self.x
            y = y - self.y

        i = self.__i(x, y)
        return i >= 0 and i < len(self.m)

    def set_count(self):
        result = 0
        for i in xrange(len(self.m)):
            if self.m[i] is not None:
                result +=1

        return result

    def __i(self, x, y):
        return x + y * self.width

    def set(self, x, y, value, offset=True):
        if offset:
            x = x - self.x
            y = y - self.y

        self.m[self.__i(x, y)] = value

    def get(self, x, y, offset=True):
        if offset:
            x = x - self.x
            y = y - self.y

        return self.m[self.__i(x, y)]

