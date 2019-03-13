import sys
from wwdb import *


class Filters:

    def __init__(self, image):
        self.image = image
        self.size_x, self.size_y = self.image.size
        self.matrix = self.image.load()

    def negative(self):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.matrix[x, y] = tuple(map(lambda cl: 255 - cl, self.matrix[x, y]))

    def full_monochrome(self, power=350):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.matrix[x, y] = (255, 255, 255) if sum(self.matrix[x, y]) > power else (0, 0, 0)

    def monochrome(self):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                med = sum(self.matrix[x, y]) // 3
                self.matrix[x, y] = med, med, med

    def sepia(self, koeff=30):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.matrix[x, y] = tuple(map(lambda cl, i: cl + koeff * i, self.matrix[x, y], range(2, -1, -1)))

    def anagliph(self, delta=10):
        self.matrix = self.image.load()
        for x in range(self.size_x - delta - 1, -1, -1):
            for y in range(self.size_y):
                r, g, b = self.matrix[x, y]
                r1, g1, b1 = self.matrix[x + delta, y]
                self.matrix[x + delta, y] = r, g1, b1

    def bright(self, koeff):
        self.matrix = self.image.load()
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.matrix[x, y] = tuple(
                    map(lambda cl: 255 if cl + koeff > 255 else 0 if cl + koeff < 0 else cl + koeff, self.matrix[x, y]))

    def mosaic(self, lup=(0, 0), rdwn=None, power=30):
        if not rdwn:
            rdwn = (self.size_x, self.size_y)
        for i in range(lup[1], rdwn[1], power * 2):
            self.move_fragment((lup[0], i), (rdwn[0], i + power), (-1) ** i * power)
        for i in range(lup[0], rdwn[0], power * 2):
            self.move_fragment((i + power, lup[1] - power), (i + power * 2, rdwn[1] - power), delta_y=(-1) ** i * power)


class Shaping:

    def __init__(self, image):
        self.image = image
        self.size_x, self.size_y = self.image.size
        self.sub_image = None

    def resize(self, x, y=None):
        if y:
            self.image = self.image.resize((x, y))
            self.size_x, self.size_y = x, y
        else:
            self.image = self.image.resize(x)
            self.size_x, self.size_y = x

    def crop(self, lup, rdwn):
        self.image = self.image.crop(lup + rdwn)
        self.size_x, self.size_y = self.image.size

    def move_fragment(self, lup, rdwn, delta_x=0, delta_y=0):
        self.sub_image = Processing(self.image)
        self.sub_image.crop(lup, rdwn)
        self.sub_image.paste_image((lup[0] + delta_x, lup[1] + delta_y), self)

    def paste_image(self, pos, screen=None):
        if screen:
            screen.image.paste(self.image, pos)
        else:
            sys.exit("I don't know name of screen you mean(((")

    def rotate(self, angle):
        self.image = self.image.rotate(angle)


class Processing(Filters, Shaping):

    def __init__(self, image):
        super().__init__(image)


user = DBUWorking('Alexandro')
print(user.sign_up('rewq'))
if user.access:
    print('yes')
else:
    print('(((')
