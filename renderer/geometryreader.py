
import struct

import mesh as m
import vector3 as v3
import vector2 as v2

class GeometryReader:

    def __init__(self):
        self.__intformat = struct.Struct('<i')
        self.__floatformat = struct.Struct('<f')
        self.__TEXTURE_COORDINATES_INCLUDED = 0x1

    def read(self, filename, chunksize=8192):
        self.__buffer = bytearray()
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    for b in chunk:
                        self.__buffer.append(b)
                else:
                    break

        self.__offset = 0
        self.__size = len(self.__buffer)

        # Discarding first integer
        self.getinteger()

        vertexcount = self.getinteger()
        indexcount = self.getinteger()

        options = self.getinteger()
        textures_enabled = ((options & self.__TEXTURE_COORDINATES_INCLUDED) == self.__TEXTURE_COORDINATES_INCLUDED)

        mesh = m.Mesh('brick', vertexcount, indexcount, textures_enabled)

        # Get vertices
        for i in xrange(vertexcount):
            mesh.vertices[i] = v3.Vector3(self.getfloat(), self.getfloat(), self.getfloat())

        # Get normals
        for i in xrange(vertexcount):
            mesh.normals[i] = v3.Vector3(self.getfloat(), self.getfloat(), self.getfloat())

        # Conditionally get textures
        if textures_enabled:
            for i in xrange(vertexcount):
                mesh.textures[i] = v2.Vector2(self.getfloat(), self.getfloat())

        for i in xrange(indexcount):
            mesh.indices[i] = self.getinteger()

        return mesh

    def getinteger(self):
        return self.getforformat(self.__intformat)

    def getfloat(self):
        return self.getforformat(self.__floatformat)

    def getforformat(self, fmt):
        fmtsize = fmt.size
        remainingsize = self.__size - self.__offset

        if fmtsize > remainingsize:
            raise BufferError('trying to read ' + fmtsize + ' bytes, but there are only ' + (remainingsize) + ' left')

        res, = fmt.unpack_from(self.__buffer, self.__offset)
        self.__offset += fmtsize

        return res
