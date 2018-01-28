import os
import argparse

from skimage import io

parser = argparse.ArgumentParser(description="Finds largest image width and height in direcory")
parser.add_argument("input_directory")
args = parser.parse_args()

files = sorted([os.path.join(args.input_directory, file) for file in os.listdir(args.input_directory)])

max_width = 0
max_width_files = []
max_height = 0
max_height_files = []

for file in files:
    if not os.path.isdir(file):
        print("Checking {}".format(file))
        image = io.imread(file)
        height, width = image.shape
        if width == max_width:
            max_width_files.append(file)
        elif width > max_width:
            max_width = width
            max_width_files = [file]

        if height == max_height:
            max_height_files.append(file)
        elif height > max_height:
            max_height = height
            max_height_files = [file]

print("Max width is {} in {}".format(max_width, max_width_files))
print("Max height is {} in {}".format(max_height, max_height_files))
