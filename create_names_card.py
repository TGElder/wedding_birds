import numpy

from skimage import data
from skimage import img_as_ubyte

import text_renderer

def create_names_card(guest_file_name, width, height):
    guest_file = open(guest_file_name, "r")
    guests = guest_file.readlines()
    guests.sort(key=sortable_name)

    output_image = numpy.ones(shape = (height, width))
    output_image = img_as_ubyte(output_image)

    increment = int(height / ((len(guests) * 2) + 1))

    y = increment

    for guest in guests:
        text_desired_h = int(height / 21)
        text_image = text_renderer.get_text_image(guest, text_desired_h)
        (text_h, text_w) = text_image.shape
        centering = (width - text_w) / 2

        text_fx = centering
        text_ty = y + text_h
        text_tx = text_fx + text_w
        output_image[y:text_ty, text_fx:text_tx] = text_image

        y += increment * 2

    return output_image

def sortable_name(name):
    first, last = name.split(" ")
    return last + ", " + first