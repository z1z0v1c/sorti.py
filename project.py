import argparse
import configparser
import hashlib
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
    parser.add_argument(
        '--recursive', '-r', action='store_true', help='Perform recursive classification'
    )
    parser.add_argument(
        '--remove-duplicates', '-d', action='store_true', help='Remove duplicate files'
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

    sortify_files(src_dir, dest_dir, args.recursive, args.remove_duplicates)


def sortify_files(src_dir, dest_dir, recursive, remove_duplicates):
    contents = os.listdir(src_dir)
    unique_hashes = set()

    for file in contents:
        logging.debug(f"File: {file}")
        if src_dir.joinpath(file).is_dir() and recursive:
            sortify_files(src_dir.joinpath(file), dest_dir, recursive, remove_duplicates)
            continue

        if remove_duplicates and not src_dir.joinpath(file).is_dir():
            file_hash = generate_file_hash(src_dir.joinpath(file))
            if file_hash in unique_hashes:
                continue
            else:
                unique_hashes.add(file_hash)

        for_other = True

        for file_type in config.sections():
            for extension in config[file_type]['extensions'].split(','):

                if file.endswith(extension):
                    subdir = dest_dir.joinpath(file_type)
                    make_dir(subdir)
                    shutil.move(src_dir.joinpath(file), subdir.joinpath(file))
                    logging.info(f"{file_type}: {file}")
                    for_other = False

        if for_other:
            other = dest_dir.joinpath("Other")
            make_dir(other)
            shutil.move(src_dir.joinpath(file), other.joinpath(file))
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


def generate_file_hash(filepath):
    """Calculates the SHA-256 hash of a file's binary content.
    Args:
        filepath: The path to the file for which the hash needs to be generated.
    Returns:
        A string representing the SHA-256 hash of the file content.
    """
    with open(filepath, 'rb') as f:
        # Read the file in binary mode
        data = f.read()
        # Calculate the SHA3-512 hash
        logging.debug(f"Calculating the file's SHA3-512 hash: {filepath}")
        hash_obj = hashlib.sha3_512(data)

    return hash_obj.hexdigest()


if __name__ == "__main__":
    main()
