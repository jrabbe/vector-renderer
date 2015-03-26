#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import plotdevice as pd
import polygonplot as p
import device as d

class Device(d.Device):

    def __init__(self, screen_width, screen_height, name, options={}):
        d.Device.__init__(self, screen_width=screen_width, screen_height=screen_height, name=name)

        fps = options.get('fps', 30)

        pd.size(screen_width, screen_height)
        self.canvas = pd.export(name + '.gif', fps=fps, loop=-1)

    def polygon(self, vertex0, vertex1, vertex2, color):
        return p.Polygon(vertex0, vertex1, vertex2, color, pd)

    def begin_render(self):
        pd.clear(all)

    def end_render(self):
        self.canvas.add()

    def present(self):
        self.canvas.finish()
