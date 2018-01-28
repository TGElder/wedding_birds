import os
import argparse
import numpy

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data, io
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import rgb2gray, label2rgb
from skimage import img_as_ubyte

parser = argparse.ArgumentParser(description="Extracts pictures from scanned page")
parser.add_argument("input")
parser.add_argument("output_directory")
parser.add_argument("--output_ratio", type=float, default=2.8286)
parser.add_argument("--x_margin", type=float, default=0.05)
parser.add_argument("--y_margin", type=float, default=0.05)
parser.add_argument("--text_width", type=float, default=0.5)
args = parser.parse_args()

output_ratio = args.output_ratio
x_margin = args.x_margin
y_margin = args.y_margin
text_width = args.text_width

if os.path.isdir(args.input):
    files = sorted([os.path.join(args.input, file) for file in os.listdir(args.input)])
else:
    files = [args.input]
    
bird_area_width = 1 - x_margin * 2 - text_width
bird_area_height = (1 - y_margin * 2) / output_ratio
bird_area_ratio = bird_area_width / bird_area_height 
print("Bird area dimensions={}x{}={}".format(bird_area_width, bird_area_height, bird_area_ratio))

for file in files:

    file_name, file_extension = os.path.splitext(os.path.basename(file))
    print("Generating place name for {}", file_name)

    print("Loading image from {}".format(file))
    image = io.imread(file)
    height, width = image.shape
    ratio = width / height

    print("dimensions={}x{}".format(width, height))
    print("ratio={}".format(ratio))
    print("bird_area_ratio={}".format(bird_area_ratio))
    if ratio >= bird_area_ratio:
        bird_area_width = width
    else:
        bird_area_width = height * bird_area_ratio

    print("bird_area_width={}".format(bird_area_width))
    output_width = bird_area_width / (1 - text_width - x_margin * 2)
    output_width = int(output_width)
    output_height = output_width / output_ratio  
    output_height = int(output_height)
    output_text_width = output_width * text_width
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

    output_file = "{}.png".format(file_name)
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    io.imsave(os.path.join(args.output_directory, output_file), output_image)
