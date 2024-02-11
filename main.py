import os
import sys
import logging

logging.basicConfig(level=logging.INFO)

extensions = {
    "Applications" : [".deb", ".rpm", ".tar.gz", ".run", ".exe", ".msi", ".jar", ".dmg", ".app", ".apk"],
    "Code" : [".py", ".java", ".go", ".c", ".h", ".cpp", ".cs", ".js", ".css", "html", ".xml"],
    "Documents" : [".txt", ".pdf", ".odt", ".ods", ".odp", ".doc", ".docx", ".xlsx", ".pptx", ".csv", ".md"],
    "Pictures" : [".jpg", ".jpeg", ".png" ".svg", ".gif", ".bmp", ".psd", ".ai"],
    "Videos" : [".mp4", ".avi", ".mpg", ".mpeg", ".mkv", ".wmv", ".mov", ".m4v"],
    "Music" : [".mp3", ".wav",".wma", ".m4a", ".aac"]
}


def main():
    validate_args()
    
    directory_path = sys.argv[1]
    
    change_directory(directory_path)
        
    contents = os.listdir(directory_path)

    for file in contents:
        for_other = True
            
        for extension_type, exts in extensions.items():
            for extension in exts:
                if file.endswith(extension):
                    print(f"{extension_type}: {file}")
                    for_other = False
                        
        if for_other:
            print(f"Other: {file}")      
         
         
def validate_args():
        if (len(sys.argv) != 2):
            logging.error("Specify the path to a single folder")
            sys.exit(1)


def change_directory(directory_path):
    try:
        os.chdir(directory_path)
        logging.info(f"Changed working directory to: {directory_path}")
    except FileNotFoundError:
        logging.error(f"The folder '{directory_path}' does not exist.")
        sys.exit(1)


if __name__ == "__main__":
    main()
