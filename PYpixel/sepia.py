from PIL import Image, ImageDraw


image = Image.open("228.jpg")
pix = image.load()
draw = ImageDraw.Draw(image)

depth = int(input('depth:'))
for i in range(image.size[0]):
    for j in range(image.size[1]):
        a = pix[i, j][0]
        b = pix[i, j][1]
        c = pix[i, j][2]
        S = (a + b + c) // 3
        a = S + depth * 2
        b = S + depth
        c = S
        if (a > 255):
            a = 255
        if (b > 255):
            b = 255
        if (c > 255):
            c = 255
        draw.point((i, j), (a, b, c))

image.save("res.jpg", "JPEG")
del draw
