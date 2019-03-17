from PIL import Image

first = Image.open("1337.jpg")
second = Image.open("228.jpg")

area = (1000, 1000, 1000, 1000)
first.paste(second, area)

first.show()

