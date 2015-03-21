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

    m.vertices[0] = vector3.Vector3(-1, -1, -1)
    m.vertices[1] = vector3.Vector3( 1, -1, -1)
    m.vertices[2] = vector3.Vector3(-1,  1, -1)
    m.vertices[3] = vector3.Vector3(-1, -1,  1)
    m.vertices[4] = vector3.Vector3( 1,  1, -1)
    m.vertices[5] = vector3.Vector3(-1,  1,  1)
    m.vertices[6] = vector3.Vector3( 1, -1,  1)
    m.vertices[7] = vector3.Vector3( 1,  1,  1)

    m.indices[0] = 0
    m.indices[1] = 1
    m.indices[2] = 2

    m.indices[3] = 0
    m.indices[4] = 1
    m.indices[5] = 3

    m.indices[6] = 0
    m.indices[7] = 2
    m.indices[8] = 3

    m.indices[9] = 1
    m.indices[10] = 2
    m.indices[11] = 4

    m.indices[12] = 1
    m.indices[13] = 3
    m.indices[14] = 6

    m.indices[15] = 1
    m.indices[16] = 4
    m.indices[17] = 6

    m.indices[18] = 2
    m.indices[19] = 3
    m.indices[20] = 5

    m.indices[21] = 2
    m.indices[22] = 4
    m.indices[23] = 5

    m.indices[24] = 3
    m.indices[25] = 5
    m.indices[26] = 6

    m.indices[27] = 4
    m.indices[28] = 5
    m.indices[29] = 7

    m.indices[30] = 4
    m.indices[31] = 6
    m.indices[32] = 7

    m.indices[33] = 5
    m.indices[34] = 6
    m.indices[35] = 7

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
