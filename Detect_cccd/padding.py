from PIL import Image

def padding_image(image):
    width, height = image.size
    right = int(width / 15)
    left = int(width / 15)
    top = int(height / 15)
    bottom = int(height / 15)
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(image.mode, (new_width, new_height), (0, 0, 0))
    result.paste(image, (left, top))
    return result