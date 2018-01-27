import os
import argparse

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data, io
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import rgb2gray, label2rgb

parser = argparse.ArgumentParser(description="Extracts pictures from scanned page")
parser.add_argument("input")
parser.add_argument("output_directory")
parser.add_argument("--minimum_object_size_pc", type=float, default=0.005)
parser.add_argument("--threshold", type=float, default=0.5)
args = parser.parse_args()

if os.path.isdir(args.input):
    files = sorted([os.path.join(args.input, file) for file in os.listdir(args.input)])
else:
    files = [args.input]
    
for file in files:
    print("Loading image from {}".format(file))
    image = io.imread(file)
    image = rgb2gray(image)
    image_area = image.size

    print("Finding objects")
    thresh = threshold_otsu(image)
    bw = closing(image < thresh, square(10))

    cleared = clear_border(bw)

    label_image = label(cleared)
    image_label_overlay = label2rgb(label_image, image=image)

    output_regions = [region for region in regionprops(label_image) if region.area/image_area >= args.minimum_object_size_pc]
    print("Found {} objects to output".format(len(output_regions)))
    output_count = 0
    for output_region in output_regions:
        output_count += 1
        print("Cropping and saving object {}".format(output_count))
        minr, minc, maxr, maxc = output_region.bbox
        cropped = image[minr:maxr, minc:maxc]
        thresholded = (cropped > args.threshold) * 255
        file_name, file_extension = os.path.splitext(os.path.basename(file))
        output_file = "{}-{}.png".format(file_name, str(output_count))
        if not os.path.exists(args.output_directory):
            os.makedirs(args.output_directory)
        io.imsave(os.path.join(args.output_directory, output_file), thresholded)
