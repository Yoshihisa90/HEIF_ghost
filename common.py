import subprocess
from PIL import Image
from pillow_heif import register_heif_opener
import numpy as np
import cv2
import pillow_heif

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

register_heif_opener()


class LIBHEIFRunner:
    def __init__(self, libheif_path):
        self.libheif_path = libheif_path

    def run(self, input_path, output_path, ctu, qp, preset):
        command = [
            self.libheif_path.absolute(),
            input_path,
            "-o", output_path,
            "-p", "x265:ipratio=1.0",
            "-p", f"preset={preset}",
            "-p", f"x265:ctu={ctu}",
            "-p", f"x265:qp={qp}",
            
        ]

        subprocess.run(command)
        
        
class LIBHEIFFirstRunner:
    def __init__(self, convert_path):
        self.convert_path = convert_path

    def run(self, input_path, output_path):
        command = [self.convert_path, input_path, output_path]
        subprocess.run(command)
        

