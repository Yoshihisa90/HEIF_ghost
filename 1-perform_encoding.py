#!/usr/bin/env python3

import argparse
from pathlib import Path
import subprocess

from common import LIBHEIFRunner, LIBHEIFFirstRunner
from parameters import single_iterator, second_iterator, triple_iterator, get_original_file_name, get_single_file_name, get_second_file_name, get_triple_file_name, get_temporary_file_name, get_temporary_file_name2, get_temporary_file_name3

import tempfile
import shutil

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--libheif-path', type=Path, default='.')
    parser.add_argument('-c', '--convert-path', type=Path, default='.')
    parser.add_argument('-i', '--input-path', type=Path, default='.')
    parser.add_argument('-o', '--output-path', type=Path, default='.')
    
    subparsers = parser.add_subparsers(title='command', dest='command', required=True)

    run_single_parser = subparsers.add_parser('run-single')
    run_single_parser.add_argument('index', type=int)
    
    run_first_parser = subparsers.add_parser('run-first')
    run_first_parser.add_argument('index', type=int)
    
    run_second_parser = subparsers.add_parser('run-second')
    run_second_parser.add_argument('index', type=int)
    
    run_first_parser = subparsers.add_parser('run-first2')
    run_first_parser.add_argument('index', type=int)
    
    run_second_parser = subparsers.add_parser('run-triple')
    run_second_parser.add_argument('index', type=int)

    return parser


def main(args):

    if args.command == 'run-single':
        all_params = list(single_iterator())
        file_name, QP1, CTU, PRESET, CIRCULAR_SHIFT = all_params[args.index]

        input_file_name = get_original_file_name(file_name)
        input_path = args.input_path / input_file_name

        output_file_name = get_single_file_name(file_name, QP1, CTU, PRESET)
        output_path = args.output_path / output_file_name

        libheif = LIBHEIFRunner(args.libheif_path)
        libheif.run(input_path, output_path, CTU, QP1, PRESET)
        
        
    elif args.command == 'run-first':
        all_params = list(single_iterator())
        file_name, QP1, CTU, PRESET, CIRCULAR_SHIFT = all_params[args.index]

        input_file_name = get_single_file_name(file_name, QP1, CTU, PRESET)
        input_path = args.input_path / input_file_name
        

        output_file_name = get_temporary_file_name(file_name, QP1, CTU, PRESET)
        output_path = args.output_path / output_file_name

        libheif = LIBHEIFFirstRunner(args.convert_path)
        libheif.run(input_path, output_path)
        
            
    elif args.command == 'run-second':
        all_params = list(second_iterator())
        file_name, QP1, QP2, CTU, PRESET, CIRCULAR_SHIFT = all_params[args.index]
        
        input_file_name = get_temporary_file_name(file_name, QP1, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        if QP1 < QP2:
            output_file_name = get_second_file_name(file_name, QP1, QP2, CTU, PRESET)
            output_path = args.output_path / output_file_name
            
            libheif = LIBHEIFRunner(args.libheif_path)
            libheif.run(input_path, output_path, CTU, QP2, PRESET)
            
        else:
            print('skip')
            
            
    elif args.command == 'run-first2':
        all_params = list(second_iterator())
        file_name, QP1, QP2, CTU, PRESET, CIRCULAR_SHIFT = all_params[args.index]

        input_file_name = get_second_file_name(file_name, QP1, QP2, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        if QP1 < QP2:
            output_file_name = get_temporary_file_name2(file_name, QP1, QP2, CTU, PRESET)
            output_path = args.output_path / output_file_name

            libheif = LIBHEIFFirstRunner(args.convert_path)
            libheif.run(input_path, output_path)
            
        else:
            print("skip")
            
            
    elif args.command == 'run-triple':
        all_params = list(triple_iterator())
        file_name, QP1, QP2, QP3, CTU, PRESET, CIRCULAR_SHIFT = all_params[args.index]
        
        input_file_name = get_temporary_file_name2(file_name, QP1, QP2, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        if QP1 < QP2 == QP3:
            output_file_name = get_triple_file_name(file_name, QP1, QP2, QP3, CTU, PRESET)
            output_path = args.output_path / output_file_name
            
            libheif = LIBHEIFRunner(args.libheif_path)
            libheif.run(input_path, output_path, CTU, QP3, PRESET)
            
        else:
            print('skip')
            


if __name__ == '__main__':
    parser = get_parser()
    main(parser.parse_args())
