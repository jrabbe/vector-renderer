

class Color4:

    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __str__(self):
        return '{R=' + self.r + ' G=' + self.g + ' B=' + self.b + ' A=' + self.a + '}'
