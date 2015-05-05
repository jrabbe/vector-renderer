#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import os
import os.path as path
import sys

import argparse
import sys
import time

from renderer import *
from geometry import *
from math3d import *

def prepare_output(output):
    output = path.abspath(output)
    print 'Outputting rendered file(s) to ', output
    if not path.exists(output):
        print 'Output directory does not exist, creating.'
        os.mkdir(output)
    elif not path.isdir(output):
        print 'Output location is not a directory, exiting.'
        sys.exit(1)

    return output

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Renders the mesh corresponding to the part id from the location of primitives.')
    parser.add_argument('part', type=str, nargs='+', help='The id of the parts to read and render', metavar='PART')
    parser.add_argument('-p', '--primitives', type=str, nargs='?', default='.',
        help='The path to the directory containing the primitives (default: %(default)s)')
    parser.add_argument('--fps', type=int, nargs='?', default=30,
        help='The number of frames per second for an animation when using the \'gif\' device (default: %(default)s)')
    parser.add_argument('-d', '--device', choices=['svg', 'gif', 'png'], type=str, default='gif',
        help='The output device to use (default: %(default)s)')
    parser.add_argument('-o', '--output', type=str, default='',
        help='The output directory to use for outputting the rendered file. Will be created if it does not exist (default: the current directory)')

    args = parser.parse_args()
    output = prepare_output(args.output)

    print 'Preparing to render {} parts'.format(len(args.part))

    print 'Creating camera'
    cam = camera.Camera()
    cam.position = vector3.Vector(0, 0, 10)
    cam.target = vector3.Vector(0, 0, 0)

    for part in args.part:

        print 'Reading geometry for ', part

        start_time = time.clock()

        g = reader.GeometryReader(args.primitives)
        m = g.read(part)

        filename = '/'.join([output, m.name])

        if args.device == 'gif':
            frames = 600
            fps = args.fps
            dev = deviceplot.Device(320, 200, filename, {fps: fps})
            print 'Rendering {} frames at {} fps ['.format(frames, fps),

            for i in xrange(frames):
                sys.stdout.flush()
                sys.stdout.write('.')
                m.rotation.x += 0.0104
                m.rotation.y += 0.0104
                dev.render(cam, [m])

            print '] DONE'
        else:
            m.rotation.x = 0.3
            m.rotation.y = -0.4
            width = 1600
            height = 1000

            if args.device == 'svg':
                dev = devicesvg.Device(width, height, filename)
            elif args.device == 'png':
                dev = deviceplot.Device(width, height, filename, {'animated': False})
            else:
                sys.stderr.write('Undefined engine ' + args.engine + ' specified\n')
                sys.exit(1)

            print 'Rendering mesh'

            dev.render(cam, [m])

        dev.present()

        end_time = time.clock()
        print 'Finished rendering part {} in {} seconds'.format(part, end_time - start_time)
