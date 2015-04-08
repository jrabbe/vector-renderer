#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import device as d

class Device(d.Device):

    def __init__(self, screen_width, screen_height, name):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, name=name)
        self.output_buffer = { 'polygons': [], 'defs': [] }

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

    def draw_triangle(self, base_points, transformation, start_brightness, end_brightness, base_color=None):
        points = map(lambda p: '{},{}'.format(p.x, p.y), base_points)
        start_color = self.to_svg_color(base_color.clone().scale(start_brightness))
        end_color = self.to_svg_color(base_color.clone().scale(end_brightness))

        grad_id = 'gradient-{}'.format(len(self.output_buffer.get('defs')))
        gradient = """
        <linearGradient id="{}" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{}"/>
            <stop offset="100%" stop-color="{}"/>
        </linearGradient>
        """.format(grad_id, start_color, end_color)
        self.output_buffer.get('defs').append(gradient)

        fill = 'url(#{})'.format(grad_id)
        transform = 'matrix({}, {}, {}, {}, {}, {})'.format(transformation.m[0],
            transformation.m[3], transformation.m[1], transformation.m[4],
            transformation.m[2], transformation.m[5])

        triangle = """
        <polygon points="{points}" fill="{fill}" transform="{transform}">
        </polygon>""".format(points=' '.join(points), fill=fill, transform=transform)
        self.output_buffer.get('polygons').append(triangle)

    def draw_line(self, point0, point1, color=None):
        dist = len(point0 - point1)

        if dist < 2:
            return

        stroke = self.to_svg_color(color, 'red')
        line = """
        <line x1="{point0.x}"
              y1="{point0.y}"
              x2="{point1.x}"
              y2="{point1.y}"
              stroke="{stroke}"
              stroke-width="{line_width}"></line>""".format(point0=point0, point1=point1, stroke=stroke, line_width=1)
        self.output_buffer.get('polygons').append(line)

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

