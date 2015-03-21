#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import struct

class Filebuffer(object):

    def __init__(self, filepath, chunksize=8192):
        self.__intformat = struct.Struct('<i')
        self.__floatformat = struct.Struct('<f')

        self.__buffer = bytearray()
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    for b in chunk:
                        self.__buffer.append(b)
                else:
                    break

        self.__offset = 0
        self.__size = len(self.__buffer)

        print 'read ', self.__size, ' bytes from ', filepath

    def getinteger(self):
        return self.getforformat(self.__intformat)

    def getfloat(self):
        return self.getforformat(self.__floatformat)

    def getforformat(self, fmt):
        fmtsize = fmt.size
        remainingsize = self.__size - self.__offset

        if fmtsize > remainingsize:
            raise BufferError('trying to read ' + fmtsize + ' bytes, but there are only ' + (remainingsize) + ' left')

        result, = fmt.unpack_from(self.__buffer, self.__offset)
        self.__offset += fmtsize

        return result
