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
parser.add_argument("--margin_w_pc", type=float, default=0.05)
parser.add_argument("--margin_h_pc", type=float, default=0.05)
parser.add_argument("--text_area_w_pc", type=float, default=0.45)
args = parser.parse_args()

output_ratio = args.output_ratio
margin_w_pc = args.margin_w_pc
margin_h_pc = args.margin_h_pc
text_area_w_pc = args.text_area_w_pc

# Handles single file or directory
if os.path.isdir(args.input):
    files = sorted([os.path.join(args.input, file) for file in os.listdir(args.input)])
else:
    files = [args.input]
    
bird_area_w_pc = 1 - margin_w_pc * 2 - text_area_w_pc
bird_area_h_pcw = (1 - margin_h_pc * 2) / output_ratio
bird_area_ratio = bird_area_w_pc / bird_area_h_pcw 

for file in files:
    file_name, file_extension = os.path.splitext(os.path.basename(file))

    print("Generating place name for {}".format(file_name))

    # Should flip images with ! in name
    if "!" in file_name:
        flip = True
        file_name = file_name.replace("!", "")
    else:
        flip = False

    print("  Loading image from {}".format(file))
    bird = io.imread(file)
    bird_h, bird_w = bird.shape
    if flip:
        print("  Flipping image")
        bird = numpy.fliplr(bird)

    # Calculate actual size of elements
    bird_ratio = (bird_w*1.0) / (bird_h*1.0)

    if bird_ratio >= bird_area_ratio:
        bird_area_w = bird_w
        bird_area_h = bird_w / bird_area_ratio
    else:
        bird_area_w = bird_h * bird_area_ratio
        bird_area_h = bird_h

    output_w = int(bird_area_w / (1 - text_area_w_pc - margin_w_pc * 2))
    output_h = int(output_w / output_ratio)
    text_area_w = int(output_w * text_area_w_pc)
    margin_w = int(output_w * margin_w_pc)
    margin_h = (output_h * margin_h_pc)

    bird_x_centering = int((output_w - margin_w * 2 - bird_w - text_area_w) / 1)
    bird_y_centering = int((output_h - margin_h * 2 - bird_h) / 2)

    output_image = numpy.ones(shape = (output_h, output_w))
    output_image = img_as_ubyte(output_image)

    # Inserting bird image into output image
    bird_fy = margin_h + bird_y_centering
    bird_fx = margin_w + bird_x_centering + text_area_w 
    bird_ty = bird_fy + bird_h
    bird_tx = bird_fx + bird_w
    output_image[bird_fy:bird_ty, bird_fx:bird_tx] = bird

    # Rendering text and inserting into output image
    name = ''.join([i for i in file_name if not i.isdigit()])
    text_desired_h = int(bird_area_h / 4)
    text_image = text_renderer.get_text_image(name, text_desired_h)
    (text_h, text_w) = text_image.shape
    text_fy = (output_h - text_desired_h) / 2
    text_fx = (output_w - text_w - bird_w - margin_w) / 2
    text_ty = text_fy + text_h
    text_tx = text_fx + text_w
    output_image[text_fy:text_ty, text_fx:text_tx] = text_image

    # Saving
    output_file = "{}.png".format(file_name)
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)
    io.imsave(os.path.join(args.output_directory, output_file), output_image)
