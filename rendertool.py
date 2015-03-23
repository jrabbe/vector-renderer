#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import argparse
import sys

from renderer import *

def render(dev, cam, mesh):
    dev.render(cam, [mesh])
    mesh.rotation.x += 0.0104
    mesh.rotation.y += 0.0104

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Renders something')
    parser.add_argument('part', type=str, help='The id of the part to read and render', metavar='PART')
    parser.add_argument('-p', '--primitives', type=str, nargs='?', default='.',
        help='The path to the directory containing the primitives (default: %(default)s)')
    parser.add_argument('--fps', type=int, nargs='?', default=30,
        help='The number of frames per second for an animation when using the \'gif\' engine (default: %(default)s)')
    parser.add_argument('-e', '--engine', choices=['svg', 'gif'], type=str, default='gif',
        help='The engine to use (default: %(default)s)')

    args = parser.parse_args()

    print 'Reading geometry for ', args.part
    g = geometryreader.GeometryReader(args.primitives)
    mesh = g.read(args.part)

    print 'Creating camera'
    cam = camera.Camera()
    cam.position = vector3.Vector3(0, 0, 10)
    cam.target = vector3.Vector3(0, 0, 0)

    if args.engine == 'svg':
        dev = devicesvg.Device(1600, 1000, mesh.name)
        mesh.rotation.x += 0.2
        mesh.rotation.y -= 0.4
        render(dev, cam, mesh)
    else:
        frames = 600
        fps = args.fps
        dev = deviceplot.Device(320, 200, mesh.name, {fps: fps})
        print '[',

        for i in xrange(frames):
            sys.stdout.flush()
            sys.stdout.write('.')
            render(dev, cam, mesh)

        print '] DONE'

    dev.present()
