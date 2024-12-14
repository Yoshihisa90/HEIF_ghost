# HEIF Ghost
This project provides a tool for encoding and decoding HEIF images, performing re-compression, and generating PKL files containing information for plotting the Mean Absolute Error (MAE) differences.

If you find these codes useful for academic research, you are highly encouraged to cite the following paper:

Furushita, Y., Fontani, M., Bressan, M., Bianchi, S., Piva, A., & Ramponi, G. (2024, February). Double Compression Detection of HEIF Images Using Coding Ghosts. In International Congress on Information and Communication Technology (pp. 305-315). Singapore: Springer Nature Singapore.


@inproceedings{furushita2024double,
  title={Double Compression Detection of HEIF Images Using Coding Ghosts},
  author={Furushita, Yoshihisa and Fontani, Marco and Bressan, Mattia and Bianchi, Stefano and Piva, Alessandro and Ramponi, Giovanni},
  booktitle={International Congress on Information and Communication Technology},
  pages={305--315},
  year={2024},
  organization={Springer}
}

## Abstract
Extensive research on double-compressed image analysis has been performed in image forensics, referring to the widely adopted JPEG coding. However, as HEIF gains popularity for its efficiency in reducing file sizes while maintaining image quality, the lack of methods for detecting double HEIF compression becomes apparent. Traditional JPEG-based techniques are not directly applicable to HEIF due to their distinct coding algorithms. In this study, we build upon Farid’s work on coding ghosts in JPEG images and introduce a method to detect double-aligned compression and estimate initial quantization coefficients in HEIF images. Our experiments show that this method performs effectively when the difference between the first and second quantization parameters (QP) exceeds 5.

## Authors
Yoshihisa Furushita　　
Mattia Bressan　　
Stefano Bianchi　　
Alessandro Piva　　
Giovanni Ramponi　　

## Main Features
### 0. Dataset

The dataset is a collection of TIF images, including indoor and outdoor landscapes, buildings, and people, taken from three cameras (Nikon D90, Nikon D40, and Nikon D7000), using the RAISE dataset.(https://git.lesc.dinfo.unifi.it/yoshihisa/TIFF_image.git) To reduce the computation load and uniform the resolution of input images, all images were cropped to a 3/2 aspect ratio and downsampled to 1200x800 using INTER-AREA, an interpolation algorithm from the OpenCV library, which prevents aliasing. All images were then saved in PNG format.

### 1. perform_encoding.py

A script for encoding PNG images into the HEIF format.
It generates single-compressed or double-compressed HEIF images.

### 2. creating_data.py

Re-encodes HEIF format images with the Quantization Parameter (QP) in the range of 0 to 51.
Calculates the MAE between the original and re-compressed images.
Saves the results in PKL file format.

### 3. performance_evaluation.py

Uses PKL files to classify single-compressed and double-compressed HEIF images.
Also estimates the QP value used in the first encoding.

### 4. ghost-analysis.py

Analyzes the MAE differences between the input and re-compressed images.
Plots the results of the MAE differences.

## Required Environment Software
The following must be installed:

Python 3.6 or later  
libheif: Library for encoding and decoding HEIF images.(https://github.com/strukturag/libheif)



