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

parser = argparse.ArgumentParser(description="Extracts largest object from page")
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

# Loading image
print("Loading image")
image = io.imread(args.input)
image = rgb2gray(image)

print("Finding largest object")
# apply threshold
thresh = threshold_otsu(image)
bw = closing(image < thresh, square(10))

# remove artifacts connected to image border
cleared = clear_border(bw)

# label image regions
label_image = label(cleared)
image_label_overlay = label2rgb(label_image, image=image)

sorted_regions = sorted(regionprops(label_image), key=lambda region: region.area, reverse=True)
largest_region = sorted_regions[0]

print("Cropping and saving")
minr, minc, maxr, maxc = largest_region.bbox
cropped = image[minr:maxr, minc:maxc]
thresh = threshold_otsu(image)
thresholded = (cropped > 0.5) * 255
io.imsave(args.output, thresholded)
