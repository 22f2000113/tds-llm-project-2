from importlib.metadata import files

import numpy as np
from PIL import Image
import colorsys
import os
from FileUtil import current_dir, get_files_in_directory
def number_of_pixels():
    # There is a mistake in the line below. Fix it
    file_path = current_dir+"/inputs/W2Q5"  # Replace with your directory path

    # Get a list of all files in the directory
    files = get_files_in_directory(file_path)
    image = Image.open(file_path+"/"+files[0])

    rgb = np.array(image) / 255.0
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
    light_pixels = np.sum(lightness > 0.227)

    return str(int(light_pixels))

