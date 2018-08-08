import cairo
import pango
import pangocairo
import sys
import numpy as np

def render_text(text, height, out_file):
    surf = cairo.ImageSurface(cairo.FORMAT_A1, height * 16, height * 2)
    context = cairo.Context(surf)

    context.rectangle(0,0,height * 16,height * 2)

    context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

    pangocairo_context = pangocairo.CairoContext(context)
    pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

    layout = pangocairo_context.create_layout()
    font = pango.FontDescription("Book Antiqua")
    font.set_size(1024 * height)
    layout.set_font_description(font)

    layout.set_text(text)
    pangocairo_context.update_layout(layout)
    pangocairo_context.show_layout(layout)

    with open(out_file, "wb") as image_file:
        surf.write_to_png(image_file)

def bounding_box(image):
    (rows, columns) = image.nonzero()
    return (min(rows), max(rows), min(columns), max(columns))

def get_text_image(text, height):
    render_text(text, height, "text_temp.png")

    from skimage import data, io
        
    image = io.imread("text_temp.png")

    (minr, maxr, minc, maxc) = bounding_box(image)

    #inverting
    image = 255 - image
    cropped = image[minr:maxr, minc:maxc]

    return cropped
