#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

from math3d import vector2

from segment import Segment
from zmap import ZMap

def empty():
    return Polygon2D([])

def from_vertices(vertices):
    return Polygon2D(vertices)

class Polygon2D(object):

    def __init__(self, vertices=None):
        self.segments = []
        self.x = None
        self.y = None
        self.width = None
        self.heigth = None
        self.zmap = None

        if vertices is not None:
            for i in xrange(len(vertices)):
                self.segments.append(Segment(vertices[i], vertices[(i + 1) % len(vertices)]))

            self.x = min(map(lambda p: p.x, vertices))
            self.width = max(map(lambda p: p.x, vertices)) - self.x + 1
            self.y = min(map(lambda p: p.y, vertices))
            self.height = max(map(lambda p: p.y, vertices)) - self.y + 1

    def __find_size(self):
        vertices = reduce(lambda acc, s: acc + s.vertices(), self.segments, [])

        self.x = min(map(lambda p: p.x, vertices))
        self.width = max(map(lambda p: p.x, vertices)) - self.x + 1
        self.y = min(map(lambda p: p.y, vertices))
        self.height = max(map(lambda p: p.y, vertices)) - self.y + 1

    def __cmp__(self, other):
        return self.zmap.overlap(other.zmap)

    def __str__(self):
        return 'Polygon2D[x={} y={} width={} height={}]'.format(self.x, self.y, self.width, self.height)

    def __add__(self, other):
        """
        Creates a new polygon containing the vertices of self and other

        arguments:
        other -- The other polygon (may also be a list of vertices)
        """
        result = Polygon2D()
        result += self
        result += other
        return result

    def __iadd__(self, other):
        """
        Adds the distinct vertices of other to self. Will remove segments that
        are present in both

        arguments:
        other -- The other polygon
        """
        for segment in other:
            if segment in self.segments:
                self.segments.remove(segment)
            else:
                self.segments.append(segment)

        self.__find_size()

        return self

    def __iter__(self):
        for segment in self.segments:
            yield segment

    def generate_zmap(self):
        self.zmap = ZMap(self)
        # print self.zmap

    def center(self):
        return vector2.Vector(self.x + self.width / 2, self.y + self.height / 2)

    def __point_sort(self, cx, cy, a, b):
        # print '({} - {}) * ({} - {}) - ({} - {}) * ({} - {}) = {} * {} - {} * {} = {} - {} = {} ~= {}'.format(
        #         a.x, cx, b.y, cy, b.x, cx, a.y, cy,
        #         (a.x - cx), (b.y - cy), (b.x - cx), (a.y - cy),
        #         (a.x - cx) * (b.y - cy), (b.x - cx) * (a.y - cy),
        #         (a.x - cx) * (b.y - cy) - (b.x - cx) * (a.y - cy),
        #         int(round((a.x - cx) * (b.y - cy) - (b.x - cx) * (a.y - cy)))
        #     )

        return int(round((a.x - cx) * (b.y - cy) - (b.x - cx) * (a.y - cy)))

    def vertices(self):
        """
        An ordered list of the vertices in this polygon. Ordered in either clockwise or counter-clockwise order
        """
        vertex_set = set()
        for segment in self:
            vertex_set |= set(segment.vertices())

        vertex_list = list(vertex_set)
        center = self.center()
        vertex_list.sort(key=lambda p: p.x)
        vertex_list.sort(lambda a, b: self.__point_sort(center.x, center.y, a, b))

        return vertex_list
