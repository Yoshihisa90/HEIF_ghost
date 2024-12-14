#!/usr/bin/env python3

import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from pillow_heif import register_heif_opener
from tempfile import TemporaryDirectory
import numpy as np
import pickle
import os
import subprocess
from memory_profiler import profile

from common import LIBHEIFRunner, LIBHEIFFirstRunner
from parameters import single_iterator, second_iterator, triple_iterator, get_single_file_name, get_second_file_name, get_triple_file_name, get_single_pkl, get_second_pkl, get_triple_pkl, get_single_shift, get_second_shift, get_triple_shift, get_temporary_file_name, get_temporary_file_name2, get_temporary_file_name3


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--libheif-path', type=Path, default='.')
    parser.add_argument('-c', '--convert-path', type=Path, default='.')
    parser.add_argument('-i', '--input-path', type=Path, default='.')
    parser.add_argument('-o', '--output-path', type=Path, default='.')
    
    subparsers = parser.add_subparsers(title='command', dest='command', required=True)

    run_single_parser = subparsers.add_parser('run-single')
    run_single_parser.add_argument('index', type=int)
    
    run_second_parser = subparsers.add_parser('run-second')
    run_second_parser.add_argument('index', type=int)

    run_second_parser = subparsers.add_parser('run-triple')
    run_second_parser.add_argument('index', type=int)

    return parser


def get_image_circular_shift(image, number_shift, number_channels=3):    
    image_array = np.asarray(image)
    image_array = np.roll(image_array, number_shift * number_channels)
    new_image = Image.fromarray(image_array)
    return new_image


def get_luma(image):
    image_array = np.array(image)
    luma = 0.299 * image_array[:,:,0] + 0.587 * image_array[:,:,1] + 0.114 * image_array[:,:,2]
    
    #imageYCbCr = image.convert("YCbCr")
    #imageYCbCrMatrix = np.asarray(imageYCbCr)
    #luma = imageYCbCrMatrix[:, :, 0].astype(float)
    return luma



def get_ghost(input_path, temp_file, output_path, CTU, PRESET, args):
    luma_heif = get_luma(Image.open(input_path))
    
    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        temp_path = temp_dir / temp_file
        
        libheif = LIBHEIFFirstRunner(args.convert_path)
        libheif.run(input_path, temp_path)
    
        mean_vector = []
        for QP in range(0,52):
            print(f"ghost qp={QP}")        
            libheif = LIBHEIFRunner(args.libheif_path)
            libheif.run(temp_path, output_path, CTU, QP, PRESET)

            qp_heif_image = Image.open(output_path)

            luma_qp = get_luma(qp_heif_image)
            dif_luma = np.abs(luma_heif - luma_qp)
            actual_mean = np.mean(dif_luma)
            mean_vector.append(actual_mean)
            print(mean_vector)
        
    return mean_vector


def get_shifted_ghost(input_path, temp_file, output_shiftpath, CTU, PRESET, CIRCULAR_SHIFT, args):
    heif_image = Image.open(input_path)
    circular_shifted_image = get_image_circular_shift(heif_image, CIRCULAR_SHIFT, 3)
    circular_shifted_image.save(output_shiftpath)
    luma_heif = get_luma(Image.open(output_shiftpath))
    
    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        temp_path = temp_dir / temp_file
        
        libheif = LIBHEIFFirstRunner(args.convert_path)
        libheif.run(output_shiftpath, temp_path)
        
        mean_vector = []
        for QP in range(0,52):
            print(f"shifted ghost qp={QP}")
            libheif = LIBHEIFRunner(args.libheif_path)
            libheif.run(temp_path, output_shiftpath, CTU, QP, PRESET)
        
            qp_heif_image = Image.open(output_shiftpath)
            
            luma_qp = get_luma(qp_heif_image)
            dif_luma = np.abs(luma_heif - luma_qp)
            actual_mean = np.mean(dif_luma)
            mean_vector.append(actual_mean)
        
    return mean_vector


def main(args):
    if args.command == 'run-single':
        all_params = list(single_iterator())
        file_name, QP1, CTU, PRESET, CIRCULAR_SHIFT = all_params[args.index]

        input_file_name = get_single_file_name(file_name, QP1, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        temp_file = get_temporary_file_name(file_name, QP1, CTU, PRESET)
        
        output_file_name = get_single_pkl(file_name, QP1, CTU, PRESET)
        output_path = args.output_path / output_file_name

        output_shiftfile_name = get_single_shift(file_name, QP1, CTU, PRESET, CIRCULAR_SHIFT)
        output_shiftpath = args.output_path / output_shiftfile_name
                
        ghost_results = get_ghost(input_path, temp_file, output_path, CTU, PRESET, args)
        shifted_ghost_results = get_shifted_ghost(input_path, temp_file, output_shiftpath, CTU, PRESET, CIRCULAR_SHIFT, args)
        
        filehandler = open(output_path, 'wb')
        info = (ghost_results, shifted_ghost_results)
        pickle.dump(info, filehandler)

        print("Done")

    elif args.command == 'run-second':
        all_params = list(second_iterator())
        file_name, QP1, QP2, CTU, PRESET, CIRCULAR_SHIFT = all_params[args.index]

        input_file_name = get_second_file_name(file_name, QP1, QP2, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        temp_file = get_temporary_file_name2(file_name, QP1, QP2, CTU, PRESET)
        
        if QP1 > QP2:
        
            output_file_name = get_second_pkl(file_name, QP1, QP2, CTU, PRESET)
            output_path = args.output_path / output_file_name

            output_shiftfile_name = get_second_shift(file_name, QP1, QP2, CTU, PRESET, CIRCULAR_SHIFT)
            output_shiftpath = args.output_path / output_shiftfile_name

            ghost_results = get_ghost(input_path, temp_file, output_path, CTU, PRESET, args)
            shifted_ghost_results = get_shifted_ghost(input_path, temp_file, output_shiftpath, CTU, PRESET, CIRCULAR_SHIFT, args)
            
            # save results into a file
            filehandler = open(output_path, 'wb')
            info = (ghost_results, shifted_ghost_results)
            pickle.dump(info, filehandler)

            print("Done")
            
        else:
            print('Skip')
            
            
    elif args.command == 'run-triple':
        all_params = list(triple_iterator())
        file_name, QP1, QP2, QP3, CTU, PRESET, CIRCULAR_SHIFT = all_params[args.index]

        input_file_name = get_triple_file_name(file_name, QP1, QP2, QP3, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        temp_file = get_temporary_file_name3(file_name, QP1, QP2, QP3, CTU, PRESET)
        
        if QP1 < QP2 and QP2 == QP3:
        
            output_file_name = get_triple_pkl(file_name, QP1, QP2, QP3, CTU, PRESET)
            output_path = args.output_path / output_file_name

            output_shiftfile_name = get_triple_shift(file_name, QP1, QP2, QP3, CTU, PRESET, CIRCULAR_SHIFT)
            output_shiftpath = args.output_path / output_shiftfile_name

            ghost_results = get_ghost(input_path, temp_file, output_path, CTU, PRESET, args)
            shifted_ghost_results = get_shifted_ghost(input_path, temp_file, output_shiftpath, CTU, PRESET, CIRCULAR_SHIFT, args)
            
            # save results into a file
            filehandler = open(output_path, 'wb')
            info = (ghost_results, shifted_ghost_results)
            pickle.dump(info, filehandler)

            print("Done")
            
        else:
            print('Skip')

if __name__ == "__main__":
    parser = get_parser()
    main(parser.parse_args())

