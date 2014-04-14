# Claire Jaja
# 4/14/14
# This module provides a function for automatically resizing images
# to the max allowed width

from PIL import Image
from django.conf import settings

def autoresize_image(image_path):
    image = Image.open(image_path)
    width = image.size[0]
    if width > settings.IMAGE_MAX_WIDTH:
        height = image.size[1]
        reduce_factor = settings.IMAGE_MAX_WIDTH / float(width)
        reduced_width = int(width * reduce_factor)
        reduced_height = int(height * reduce_factor)
        image = image.resize((reduced_width, reduced_height), Image.ANTIALIAS)
        image.save(image_path)
