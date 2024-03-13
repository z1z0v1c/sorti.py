import argparse
import configparser
import logging
import os
from pathlib import Path
import shutil
import sys


logging.basicConfig(level=logging.DEBUG)

config = configparser.ConfigParser()
config.read("config.ini")


def main():
    parser = argparse.ArgumentParser(
        description='A python console application for files organization'
    )
    
    # Define flags
    parser.add_argument(
        '--input', '-i', type=str, help='Specify a source (input) directory'
    )
    parser.add_argument(
        '--output', '-o', type=str, help='Specify a destination (output) directory'
    )
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    if args.input:
        src_dir = Path(args.input)
    else:
        src_dir = Path.cwd()
        
    if args.output:
        dest_dir = Path(args.output)
    else:
        dest_dir = Path.cwd()
    
    logging.debug(f"Source directory: {src_dir}")
    logging.debug(f"Destination directory: {dest_dir}")
    
    make_dir(dest_dir)
    
    sortify_files(src_dir, dest_dir)


def sortify_files(src_dir, dest_dir):
    change_dir(src_dir)
    
    contents = os.listdir(src_dir)

    for file in contents:
        for_other = True
            
        for file_type in config.sections():
            for extension in config[file_type]['extensions'].split(','):
                
                if file.endswith(extension):
                    subdir = dest_dir.joinpath(file_type) 
                    make_dir(subdir)
                    shutil.move(file, subdir.joinpath(file))
                    logging.info(f"{file_type}: {file}")
                    for_other = False
                        
        if for_other:
            other = dest_dir.joinpath("Other")
            make_dir(other)
            shutil.move(file, other.joinpath(file))
            logging.info(f"Other: {file}")


def change_dir(path):
    try:
        os.chdir(path)
        logging.debug(f"Changed working directory to: {path}")
    except FileNotFoundError:
        logging.error(f"The folder '{path}' does not exist.")
        sys.exit(1)


def make_dir(dir_path):
    if not dir_path.exists():
        os.makedirs(dir_path)
        logging.debug(f"Created directory: {dir_path}")
        
        
if __name__ == "__main__":
    main()
