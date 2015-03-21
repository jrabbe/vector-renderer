#!/usr/bin/env python
# encoding: utf-8

import sys
from renderer import *

if __name__ == '__main__':

    filename = 'cube.gif'
    frames = 600
    duration = 10
    fps = frames / duration

    print 'rendering %d frames at %d fps to %s' % (frames, fps, filename)
    sys.stdout.flush()

    cam = camera.Camera()
    g = geometryreader.GeometryReader()
    m = g.read('./files/cube.g')

    cam.position = vector3.Vector3(0, 0, 10)
    cam.target = vector3.Vector3(0, 0, 0)

    dev = deviceplot.Device(160, 100, filename, {fps: fps})

    print '[',

    for i in xrange(frames):
        sys.stdout.flush()
        sys.stdout.write('.')

        m.rotation.x += 0.0104
        m.rotation.y += 0.0104
        dev.render(cam, [m])

    print '] DONE'

    dev.present()
