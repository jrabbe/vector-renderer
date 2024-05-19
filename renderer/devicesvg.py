#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import xml.etree.ElementTree as ET

from .device import Device

class Device(Device):

    def __init__(self, screen_width, screen_height, name):
        super().__init__(screen_width=screen_width, screen_height=screen_height, name=name)
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        self.output_buffer = {
            'polygons': ET.Element('g'),
            'defs': ET.Element('defs')
        }

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

        start_color = self.to_svg_color(base_color.scaled(start_brightness))
        end_color = self.to_svg_color(base_color.scaled(end_brightness))

        grad_id = 'gradient-{}'.format(len(self.output_buffer.get('defs')))
        attributes = {
            'id': grad_id,
            'x1': '0%',
            'y1': '0%',
            'x2': '100%',
            'y2': '0%'
        }

        gradient = ET.Element('linearGradient', attrib=attributes)
        ET.SubElement(gradient, 'stop', attrib={'offset': '0%', 'stop-color': start_color})
        ET.SubElement(gradient, 'stop', attrib={'offset': '100%', 'stop-color': end_color})
        self.output_buffer.get('defs').append(gradient)

        attributes = {
            'points': ' '.join(points),
            'fill': 'url(#{})'.format(grad_id),
            'transform': 'matrix({}, {}, {}, {}, {}, {})'.format(
                transformation.m[0], transformation.m[1], transformation.m[3],
                transformation.m[4], transformation.m[6], transformation.m[7])
        }

        triangle = ET.Element('polygon', attrib=attributes)
        self.output_buffer.get('polygons').append(triangle)

    def draw_line(self, point0, point1, color=None):
        dist = len(point0 - point1)

        if dist < 2:
            return

        attributes = {
            'x1': point0.x,
            'y1': point0.y,
            'x2': point1.x,
            'y2': point1.y,
            'stroke': self.to_svg_color(color, 'red'),
            'stroke-width': 1
        }
        line = ET.element('line', attrib=attributes)
        self.output_buffer.get('polygons').append(line)

    def begin_render(self):
        pass

    def end_render(self):
        pass

    def present(self):
        viewBox = '0 0 {} {}'.format(self.screen_width, self.screen_height)
        # TODO: add default namespace for svg element: http://www.w3.org/2000/svg
        svg = ET.Element('{http://www.w3.org/2000/svg}svg', attrib={'viewBox': viewBox})
        svg.append(self.output_buffer.get('defs'))
        svg.append(self.output_buffer.get('polygons'))

        tree = ET.ElementTree(svg)


        # TODO: Figure out how to add '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
        with open(self.name + '.svg', 'w') as f:
            tree.write(f, encoding='unicode')

