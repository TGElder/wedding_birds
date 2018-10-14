import os
import argparse
import numpy

from skimage import data, io
from skimage import img_as_ubyte

import text_renderer
import create_names_card

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output_directory")
parser.add_argument("--output_ratio", type=float, default=0.709)
parser.add_argument("--margin_w_pc", type=float, default=0.02)
parser.add_argument("--margin_h_pc", type=float, default=0.02)
parser.add_argument("--text_area_h_pc", type=float, default=0.25)
parser.add_argument("--add_names", type=bool, default=True)
parser.add_argument("--guide_w", type=float, default=0.01)
args = parser.parse_args()

output_ratio = args.output_ratio
margin_w_pc = args.margin_w_pc
margin_h_pc = args.margin_h_pc
text_area_h_pc = args.text_area_h_pc
add_names = args.add_names

# Handles single file or directory
if os.path.isdir(args.input):
    files = sorted([os.path.join(args.input, file) for file in os.listdir(args.input)])
else:
    files = [args.input]
    
scene_area_w_pch = (1 - margin_w_pc * 2) * output_ratio
scene_area_h_pc = (1 - margin_h_pc * 2) - text_area_h_pc
scene_area_ratio = scene_area_w_pch / scene_area_h_pc

for file in files:
    file_name, file_extension = os.path.splitext(os.path.basename(file))

    if file_extension == ".png":

        print("Generating scene card for {}".format(file_name))

        # Image on right if ! in name
        if "!" in file_name:
            flip = True
            file_name = file_name.replace("!", "")
        else:
            flip = False

        print("  Loading image from {}".format(file))
        scene = io.imread(file)
        scene_h, scene_w = scene.shape

        # Calculate actual size of elements
        scene_ratio = (scene_w*1.0) / (scene_h*1.0)

        if scene_ratio >= scene_area_ratio:
            scene_area_w = scene_w
            scene_area_h = scene_w / scene_area_ratio
        else:
            scene_area_w = scene_h * scene_area_ratio
            scene_area_h = scene_h

        output_h = int(scene_area_h / (1 - text_area_h_pc - margin_h_pc * 2))
        output_w = int(output_h * output_ratio)
        text_area_h = int(output_h * text_area_h_pc)
        margin_w = int(output_w * margin_w_pc)
        margin_h = int(output_h * margin_h_pc)


        scene_x_centering = int((output_w - margin_w * 2 - scene_w) / 2)
        scene_y_centering = int((output_h - margin_h * 2 - scene_h - text_area_h) / 2)

        scene_image = numpy.ones(shape = (output_h, output_w))
        scene_image = img_as_ubyte(scene_image)

        # Inserting scene image into output image
        scene_fy = margin_h + scene_y_centering + text_area_h
        scene_fx = margin_w + scene_x_centering
        scene_ty = scene_fy + scene_h
        scene_tx = scene_fx + scene_w
        scene_image[scene_fy:scene_ty, scene_fx:scene_tx] = scene

        # Rendering text and inserting into output image
        name = ''.join([i for i in file_name if not i.isdigit()])
        text_desired_h = int(text_area_h / 2)
        text_image = text_renderer.get_text_image(name, text_desired_h)
        (text_h, text_w) = text_image.shape

        text_x_centering = int((output_w - margin_w * 2 - text_w) / 2)
        text_y_centering = int((text_area_h - text_desired_h) / 2)

        text_fy = margin_h + text_y_centering
        text_fx = margin_w + text_x_centering
        text_ty = text_fy + text_h
        text_tx = text_fx + text_w
        scene_image[text_fy:text_ty, text_fx:text_tx] = text_image

        if add_names:
            name_image = create_names_card.create_names_card(os.path.join(args.input, file_name) + ".txt", output_w, output_h)

            output_image = numpy.ones(shape = (output_h, output_w * 2))
            output_image = img_as_ubyte(output_image)

            if flip:
                left_image = name_image
                right_image = scene_image
            else:
                left_image = scene_image
                right_image = name_image
        
            output_image[0 : output_h, 0 : output_w] = left_image
            output_image[0 : output_h, output_w : output_w * 2] = right_image
            
        else:
            output_image = scene_image

        # Adding guides
        guide_px = (int)( output_w * 2 * args.guide_w)
        output_image[0 : guide_px, 0 : 2] = 0
        output_image[0 : 2, 0 : guide_px] = 0
        output_image[0 : guide_px,  output_w * 2 - 2 :  output_w * 2] = 0
        output_image[0 : 2,  output_w * 2 - guide_px :  output_w * 2] = 0
        output_image[output_h - guide_px : output_h, 0 : 2] = 0
        output_image[output_h - 2 : output_h, 0 : guide_px] = 0
        output_image[output_h - guide_px : output_h,  output_w * 2 - 2 :  output_w * 2] = 0
        output_image[output_h - 2 : output_h,  output_w * 2 - guide_px :  output_w * 2] = 0

        board_image = numpy.ones(shape = (output_h * 2, output_w * 2))
        board_image = img_as_ubyte(board_image)
        board_image[output_h : output_h * 2, 0 : output_w * 2] = output_image

        # Saving
        file_name = "{}.png".format(file_name)
        board_directory = os.path.join(args.output_directory, "board")
        table_directory = os.path.join(args.output_directory, "table")
        if not os.path.exists(args.output_directory):
            os.makedirs(args.output_directory)
        if not os.path.exists(board_directory):
            os.makedirs(board_directory)
        if not os.path.exists(table_directory):
            os.makedirs(table_directory)            
        io.imsave(os.path.join(table_directory, file_name), output_image)
        io.imsave(os.path.join(board_directory, file_name), board_image)
        
