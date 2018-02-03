import os
import argparse
import numpy

from skimage import data, io
from skimage import img_as_ubyte

import text_renderer

parser = argparse.ArgumentParser(description="Extracts pictures from scanned page")
parser.add_argument("input")
parser.add_argument("output_directory")
parser.add_argument("--output_ratio", type=float, default=2.8286)
parser.add_argument("--x_margin", type=float, default=0.05)
parser.add_argument("--y_margin", type=float, default=0.05)
parser.add_argument("--text_area_width", type=float, default=0.5)
args = parser.parse_args()

output_ratio = args.output_ratio
x_margin = args.x_margin
y_margin = args.y_margin
text_area_width = args.text_area_width

if os.path.isdir(args.input):
    files = sorted([os.path.join(args.input, file) for file in os.listdir(args.input)])
else:
    files = [args.input]
    
bird_area_width = 1 - x_margin * 2 - text_area_width
bird_area_height = (1 - y_margin * 2) / output_ratio
bird_area_ratio = bird_area_width / bird_area_height 
print("bird_area_ratio={}".format(bird_area_ratio))

for file in files:

    file_name, file_extension = os.path.splitext(os.path.basename(file))
    if "!" in file_name:
        flip = True
        file_name = file_name.replace("!", "")
    else:
        flip = False
    print("Generating place name for {}".format(file_name))

    print("Loading image from {}".format(file))
    image = io.imread(file)
    height, width = image.shape
    if flip:
        print("Flipping image")
        image = numpy.fliplr(image)

    print("Image dimensions = {}x{}".format(width, height))
    ratio = (width*1.0) / (height*1.0)
    print(ratio)

    if ratio >= bird_area_ratio:
        bird_area_width = width
        bird_area_height = width / bird_area_ratio
    else:
        bird_area_width = height * bird_area_ratio
        bird_area_height = height

    print("bird_area_dimensions={}x{}".format(bird_area_width, bird_area_height))
    output_width = bird_area_width / (1 - text_area_width - x_margin * 2)
    output_width = int(output_width)
    output_height = output_width / output_ratio  
    output_height = int(output_height)
    output_text_width = output_width * text_area_width
    output_text_width = int(output_text_width)
    print("output_dimensions={}x{}".format(output_width, output_height))
    margin_width = output_width * x_margin
    margin_width = int(margin_width)
    margin_height = output_height * y_margin
    margin_height = int(margin_height)

    bird_x_centering = int((output_width - output_text_width - margin_width * 2 - width) / 1)
    bird_y_centering = int((output_height - margin_height * 2 - height) / 2)

    output_image = numpy.ones(shape = (output_height, output_width))
    output_image = img_as_ubyte(output_image)

    minr = margin_height + bird_y_centering
    maxr = margin_height + bird_y_centering + height
    minc = margin_width + output_text_width + bird_x_centering
    maxc = margin_width + output_text_width + bird_x_centering + width
    print("{}:{} {}:{}".format(minr, maxr, minc, maxc))

    output_image[minr:maxr, minc:maxc] = image

    text_desired_height = int(bird_area_height / 4)
    print("Desired text height = {}".format(text_desired_height))
    text_image = text_renderer.get_text_image(file_name, text_desired_height)
    (text_height, text_width) = text_image.shape
    text_ystart = (output_height - text_desired_height) / 2
    text_xstart = (output_width - width - margin_width - text_width) / 2

    output_image[text_ystart:text_ystart + text_height, text_xstart:text_xstart + text_width] = text_image

    output_file = "{}.png".format(file_name)
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    io.imsave(os.path.join(args.output_directory, output_file), output_image)
