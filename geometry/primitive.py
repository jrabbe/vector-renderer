#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

def from_triangle_strips(strips):
    return Primitive(strips)

class Primitive(object):

    def __init__(self, strips=[]):
        self.strips = strips
