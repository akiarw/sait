from PIL import Image, ImageEnhance

def add_watermark(image, watermark, opacity=1, wm_interval=0):

    assert opacity >= 0 and opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image.size, (0,0,0,0))
    for y in range(0, image.size[1], watermark.size[1]+wm_interval):
        for x in range(0, image.size[0], watermark.size[0]+wm_interval):
            layer.paste(watermark, (x, y))
    return Image.composite(layer,  image,  layer)

if __name__ == "__main__":
    img = Image.open("1337.jpg")
    watermark = Image.open("watermark.png")


    result = add_watermark(img, watermark)
result.save('res.png')


