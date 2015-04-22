#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import os
import os.path as path
import sys

import argparse
import sys

from renderer import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Renders something')
    parser.add_argument('part', type=str, help='The id of the part to read and render', metavar='PART')
    parser.add_argument('-p', '--primitives', type=str, nargs='?', default='.',
        help='The path to the directory containing the primitives (default: %(default)s)')
    parser.add_argument('--fps', type=int, nargs='?', default=30,
        help='The number of frames per second for an animation when using the \'gif\' engine (default: %(default)s)')
    parser.add_argument('-e', '--engine', choices=['svg', 'gif'], type=str, default='gif',
        help='The engine to use (default: %(default)s)')
    parser.add_argument('-o', '--output', type=str, default='',
        help='The output directory to use for outputting the rendered file. Will be created if it does not exist (default: the current directory)')

    args = parser.parse_args()

    output = args.output
    output = path.abspath(output)
    print 'Outputting rendered file(s) to ', output
    if not path.exists(output):
        print 'Output directory does not exist, creating.'
        os.mkdir(output)
    elif not path.isdir(output):
        print 'Output location is not a directory, exiting.'
        sys.exit(1)



    print 'Reading geometry for ', args.part
    g = geometryreader.GeometryReader(args.primitives)
    mesh = g.read(args.part)

    print 'Creating camera'
    cam = camera.Camera()
    cam.position = vector3.Vector3(0, 0, 10)
    cam.target = vector3.Vector3(0, 0, 0)

    if args.engine == 'svg':
        dev = devicesvg.Device(1600, 1000, '/'.join([output, mesh.name]))
        mesh.rotation.x += 0.3
        mesh.rotation.y -= 0.4
        dev.render(cam, [mesh])
    else:
        frames = 600
        fps = args.fps
        dev = deviceplot.Device(320, 200, '/'.join([output, mesh.name]), {fps: fps})
        print 'Rendering {} frames at {} fps ['.format(frames, fps),

        for i in xrange(frames):
            sys.stdout.flush()
            sys.stdout.write('.')
            mesh.rotation.x += 0.0104
            mesh.rotation.y += 0.0104
            dev.render(cam, [mesh])

        print '] DONE'

    dev.present()
