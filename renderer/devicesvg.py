#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import device as d
import polygonsvg as p

class Device(d.Device):

    def __init__(self, screen_width, screen_height, name):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, name=name)
        self.output_buffer = { 'polygons': [], 'defs': [] }

    def to_svg_color(self, color, default='black'):
        if color is None:
            svg_color = default
        else:
            svg_color = 'rgba({}, {}, {}, {})'.format(color.get('r', 0, 255, int),
                color.get('g', 0, 255, int),
                color.get('b', 0, 255, int),
                color.get('a', 0.0, 1.0, float))
        return svg_color

    def polygon(self, vertex0, vertex1, vertex2, color, scene):
        return p.Polygon(vertex0, vertex1, vertex2, color, scene, self.output_buffer)

    def begin_render(self):
        pass

    def end_render(self):
        pass

    def present(self):
        output = []
        svg = '<svg viewBox="0 0 {screen_width} {screen_height}" xmlns="http://www.w3.org/2000/svg">'.format(screen_width=self.screen_width, screen_height=self.screen_height)
        output.append(svg)
        output.append('<defs>')
        output.extend(self.output_buffer.get('defs'))
        output.append('</defs>')
        output.append('<g>')
        output.extend(self.output_buffer.get('polygons'))
        output.append('</g>')
        output.append('</svg>')

        with open(self.name + '.svg', 'w') as f:
            f.writelines(map(lambda l: l + '\n', output))

