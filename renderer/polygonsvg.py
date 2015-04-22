#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import polygon as p

class Polygon(p.Polygon):

    def __init__ (self, vertex0, vertex1, vertex2, color, scene, output_buffer):
        p.Polygon.__init__(self, vertex0, vertex1, vertex2, color, scene)
        self.output_buffer = output_buffer

    def to_svg_color(self, color, default='black'):
        if color is None:
            svg_color = default
        else:
            svg_color = 'rgba({}, {}, {}, {})'.format(
                color.get('r', 0, 255, int),
                color.get('g', 0, 255, int),
                color.get('b', 0, 255, int),
                color.get('a', 0.0, 1.0, float))

        return svg_color

    def do_draw(self, points, color):
        stroke = 'black'
        line_width = 1
        fill = self.to_svg_color(color)
        points = map(lambda p: '{},{}'.format(p.x, p.y), points)

        triangle = '<polygon points="{points}" stroke="{stroke}" fill="{fill}" stroke-linejoin="bevel" stroke-width="{line_width}"></polygon>'.format(points=' '.join(points), stroke=stroke, fill=fill, line_width=line_width)
        self.output_buffer.append(triangle)

    def draw_line(self, point0, point1, color=None):
        dist = len(point0 - point1)

        if dist < 2:
            return

        stroke = self.to_svg_color(color, 'red')
        line = '<line x1="{point0.x}" y1="{point0.y}" x2="{point1.x}" y2="{point1.y}" stroke="{stroke}" stroke-width="{line_width}"></line>'.format(point0=point0, point1=point1, stroke=stroke, line_width=1)
        self.output_buffer.append(line)
