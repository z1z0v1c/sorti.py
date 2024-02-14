import os
import sys
import logging
from pathlib import Path


logging.basicConfig(level=logging.DEBUG)

extensions = {
    "Applications" : [".deb", ".rpm", ".tar.gz", ".run", ".exe", ".msi", ".jar", ".dmg", ".app", ".apk"],
    "Code" : [".py", ".java", ".go", ".c", ".h", ".cpp", ".cs", ".js", ".css", "html", ".xml"],
    "Documents" : [".txt", ".pdf", ".odt", ".ods", ".odp", ".doc", ".docx", ".xlsx", ".pptx", ".csv", ".md"],
    "Pictures" : [".jpg", ".jpeg", ".png", ".svg", ".gif", ".bmp", ".psd", ".ai"],
    "Videos" : [".mp4", ".avi", ".mpg", ".mpeg", ".mkv", ".wmv", ".mov", ".m4v"],
    "Music" : [".mp3", ".wav",".wma", ".m4a", ".aac"]
}


def main():
    validate_args()
    
    source_dir, dest_dir = get_dirs(sys.argv)
    
    logging.debug(f"Source directory: {source_dir}")
    logging.debug(f"Destination directory to: {dest_dir}")
    
    make_dir(dest_dir)
    
    change_directory(source_dir)
        
    contents = os.listdir(source_dir)

    for file in contents:
        for_other = True
            
        for extension_type, exts in extensions.items():
            for extension in exts:
                
                if file.endswith(extension):
                    print(f"{extension_type}: {file}")
                    subdir = dest_dir.joinpath(extension_type)
                    make_dir(subdir)
                    for_other = False
                        
        if for_other:
            other = dest_dir.joinpath("Other")
            make_dir(other)
            print(f"Other: {file}")      
         
         
def validate_args():
        if (len(sys.argv) != 3):
            logging.error("Specify paths to the source and destination directories.")
            sys.exit(1)


def change_directory(directory_path):
    try:
        os.chdir(directory_path)
        logging.debug(f"Changed working directory to: {directory_path}")
    except FileNotFoundError:
        logging.error(f"The folder '{directory_path}' does not exist.")
        sys.exit(1)


def get_dirs(args):
    if (len(args) == 2):
        return Path(args[1]), Path(args[1])
    else:
        return Path(args[1]), Path(args[2])


def make_dir(dir):
    if not dir.exists():
        os.makedirs(dir)
        logging.debug(f"Created directory: {dir}") 
        
        
if __name__ == "__main__":
    main()
