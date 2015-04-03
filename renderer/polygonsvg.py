#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import polygon as p
import matrix3 as m3

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

    def do_draw(self, points, color, midpoint, point_transformation):
        stroke = 'black'
        line_width = 1
        # fill = self.to_svg_color(color)
        # points = map(lambda p: '{},{}'.format(p.x, p.y), points)

        base_points = map(lambda a: '{},{}'.format(a[0], a[1]), [(0,0),(midpoint, 0.5), (1, 0)])
        start_color = self.to_svg_color(color.clone().scale(points[0].light_normal))
        end_color = self.to_svg_color(color.clone().scale(points[1].light_normal))

        grad_id = 'gradient-{}'.format(len(self.output_buffer.get('defs')))
        gradient = """
        <linearGradient id="{}" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="{}"/>
            <stop offset="100%" stop-color="{}"/>
        </linearGradient>
        """.format(grad_id, start_color, end_color)
        self.output_buffer.get('defs').append(gradient)

        fill = 'url(#{})'.format(grad_id)
        transform = 'matrix({}, {}, {}, {}, {}, {})'.format(point_transformation.m[0], point_transformation.m[3], point_transformation.m[1], point_transformation.m[4], point_transformation.m[2], point_transformation.m[5])

        #
        # Making a triangle:
        # 1. Start with a base triangle A-B-C => 0,0-x,0.5-1,0 where x makes B map to the color of "its" texture
        # 1a. The base triangle has a linear gradient from A-C where A is the lightest, C is the darkest,
        #     and B has the position to give the right shade
        # 2. Skew, translate, and rotate to make it fit with the points
        # 3. Success (hopefully)

        #
        # Transformation:
        # 1. A = [[xb1 xb2 xb3][yb1 yb2 yb3][1 1 1]]
        # 2. B = [[xt1 xt2 xt3][yt1 yt2 yt3][1 1 1]]
        # 3. M = B  * Inv(A) = B * (1/det(A) * transpose(A))
        #
        # Result should be 6 values that can be plugged into the "transform" property of an SVG primitive

        triangle = '<polygon points="{points}" fill="{fill}" transform="{transform}"></polygon>'.format(points=' '.join(base_points), stroke=stroke, fill=fill, line_width=line_width, transform=transform)
        self.output_buffer.get('polygons').append(triangle)

    def draw_line(self, point0, point1, color=None):
        dist = len(point0 - point1)

        if dist < 2:
            return

        stroke = self.to_svg_color(color, 'red')
        line = '<line x1="{point0.x}" y1="{point0.y}" x2="{point1.x}" y2="{point1.y}" stroke="{stroke}" stroke-width="{line_width}"></line>'.format(point0=point0, point1=point1, stroke=stroke, line_width=1)
        self.output_buffer.get('polygons').append(line)
