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
    validate_args()
    
    source_dir, dest_dir = get_dirs(sys.argv)
    
    logging.debug(f"Source directory: {source_dir}")
    logging.debug(f"Destination directory: {dest_dir}")
    
    make_dir(dest_dir)
    
    sortify_files(source_dir, dest_dir)
         
         
def validate_args():
        if (len(sys.argv) != 3):
            logging.error("Specify paths to the source and destination directories.")
            sys.exit(1)


def get_dirs(args):
    if (len(args) == 2):
        return Path(args[1]), Path(args[1])
    else:
        return Path(args[1]), Path(args[2])


def sortify_files(source_dir, dest_dir):
    change_dir(source_dir)
    
    contents = os.listdir(source_dir)

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


def make_dir(dir):
    if not dir.exists():
        os.makedirs(dir)
        logging.debug(f"Created directory: {dir}")
        
        
if __name__ == "__main__":
    main()
