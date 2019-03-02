from PIL import Image


class Processing:

    def __init__(self, image):
        if type(image) == str:
            self.image = Image.open(image)
        else:
            self.image = image

    def resize(self, x, y=None):
        if y:
            self.image.resize((x, y))
        else:
            self.image.resize(x)

    # def negative(self):
