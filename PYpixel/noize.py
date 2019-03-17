import random
from PIL import Image, ImageDraw

factor = int(input('factor:'))
image = Image.open("228.jpg")
pix = image.load()
draw = ImageDraw.Draw(image)
for i in range(image.size[0]):
    for j in range(image.size[1]):
        rand = random.randint(-factor, factor)
        a = pix[i, j][0] + rand
        b = pix[i, j][1] + rand
        c = pix[i, j][2] + rand
        if (a < 0):
            a = 0
        if (b < 0):
            b = 0
        if (c < 0):
            c = 0
        if (a > 255):
            a = 255
        if (b > 255):
            b = 255
        if (c > 255):
            c = 255
        draw.point((i, j), (a, b, c))

image.save("res.jpg", "JPEG")
del draw


