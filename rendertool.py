#!/usr/bin/env python
# encoding: utf-8

import sys

from renderer import *

if __name__ == '__main__':

    filename = 'cube.gif'
    frames = 600
    duration = 10
    fps = frames/duration

    print 'rendering %d frames as %d fps to %s' % (frames, fps, filename)
    sys.stdout.flush()

    cam = camera.Camera()
    m = mesh.Mesh('cube', 8, 36)

    m.vertices[0] = vector3.Vector3(-1, 1, 1)
    m.vertices[1] = vector3.Vector3(1, 1, 1)
    m.vertices[2] = vector3.Vector3(-1, -1, 1)
    m.vertices[3] = vector3.Vector3(-1, -1, -1)
    m.vertices[4] = vector3.Vector3(-1, 1, -1)
    m.vertices[5] = vector3.Vector3(1, 1, -1)
    m.vertices[6] = vector3.Vector3(1, -1, 1)
    m.vertices[7] = vector3.Vector3(1, -1, -1)

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
