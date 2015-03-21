#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import device as d

class Device(d.Device):

    def __init__(self, screen_width, screen_height, name):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, name=name)
        self.output_buffer = []

        svg = '<svg viewBox="0 0 {screen_width} {screen_height}" xmlns="http://www.w3.org/2000/svg">'.format(screen_width=screen_width, screen_height=screen_height)
        self.output_buffer.append(svg + '\n')
        self.output_buffer.append('<g>\n')

    def draw_line(self, point1, point2, color=None):
        dist = len(point1 - point2)

        if dist < 2:
            return

        stroke = self.to_svg_color(color, 'red')
        line = '<line x1="{point1.x}" y1="{point1.y}" x2="{point2.x}" y2="{point2.y}" stroke="{stroke}" stroke-width="{line_width}"></line>'.format(point1=point1, point2=point2, stroke=stroke, line_width=0.1)
        self.output_buffer.append(line + '\n')

    def to_svg_color(self, color, default='black'):
        if color is None:
            svg_color = default
        else:
            svg_color = 'rgba({}, {}, {}, {})'.format(color.get('r', 0, 255, int),
                color.get('g', 0, 255, int),
                color.get('b', 0, 255, int),
                color.get('a', 0.0, 1.0, float))
            return svg_color

    def draw_triangle(self, point0, point1, point2, color=None):
        points = []
        points.append(str(point0.x) + ',' + str(point0.y))
        points.append(str(point1.x) + ',' + str(point1.y))
        points.append(str(point2.x) + ',' + str(point2.y))
        fill = self.to_svg_color(color)

        triangle = '<polygon points="{points}" stroke="{stroke}" fill="{fill}" stroke-linejoin="bevel" stroke-width="{line_width}"></polygon>'.format(points=' '.join(points), stroke='black', fill=fill, line_width=0.1)
        self.output_buffer.append(triangle + '\n')

    def begin_render(self):
        pass

    def end_render(self):
        pass

    def present(self):
        self.output_buffer.append('</g>\n')
        self.output_buffer.append('</svg>\n')

        with open(self.name + '.svg', 'w') as f:
            f.writelines(self.output_buffer)

