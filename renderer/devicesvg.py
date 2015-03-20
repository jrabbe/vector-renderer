#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import device as d

class Device(d.Device):

    def __init__(self, screen_width, screen_height, filename):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, filename=filename)
        self.output_buffer = []

        self.output_buffer.append('<svg viewBox="0 0 ' + str(self.screen_width) + ' ' + str(self.screen_height) + '" xmlns="http://www.w3.org/2000/svg">\n')
        self.output_buffer.append('<g>\n')

    def draw_point(self, point):
        # clipping what is visible inside "screen"
        if point.x >= 0 and point.y >= 0 and point.x < self.screen_width and point.y < self.screen_height:
            self.output_buffer.append('<circle cx="' + str(point.x) + '" cy="' + str(point.y) + '" r="1" fill="black" stroke="none" />\n')

    def draw_line(self, point1, point2):
        dist = len(point1 - point2)

        if dist < 2:
            return

        self.output_buffer.append(''.join(['<line x1="', str(point1.x), '" y1="', str(point1.y), '" x2="', str(point2.x), '" y2="', str(point2.y), '" stroke="red" />\n']))

    def draw_triangle(self, point0, point1, point2):
        points = []
        points.append(str(point0.x) + ',' + str(point0.y))
        points.append(str(point1.x) + ',' + str(point1.y))
        points.append(str(point2.x) + ',' + str(point2.y))

        self.output_buffer.append('<polygon points="' + ' '.join(points) + '" stroke="black" fill="none" />')

    def begin_render(self):
        pass

    def end_render(self):
        pass

    def present(self):
        self.output_buffer.append('</g>\n')
        self.output_buffer.append('</svg>\n')

        with open(self.filename, 'w') as f:
            f.writelines(self.output_buffer)

