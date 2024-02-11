import os
import sys

extensions = {
    "apps" : [".deb", ".rpm", ".tar.gz", ".run", ".exe", ".msi", ".jar", ".dmg", ".app", ".apk"],
    "code" : [".py", ".java", ".go", ".c", ".h", ".cpp", ".cs", ".js", ".css", "html", ".xml"],
    "docs" : [".txt", ".pdf", ".odt", ".ods", ".odp", ".doc", ".docx", ".xlsx", ".pptx", ".csv", ".md"],
    "pics" : [".jpg", ".jpeg", ".png" ".svg", ".gif", ".bmp", ".psd", ".ai"],
    "video" : [".mp4", ".avi", ".mpg", ".mpeg", ".mkv", ".wmv", ".mov", ".m4v"],
    "audio" : [".mp3", ".wav",".wma", ".m4a", ".aac"]
}


def main():
    if (len(sys.argv) != 2):
        print("Specify the path to a single folder")
        sys.exit(1)
    else:
        try:
            directory_path = sys.argv[1]
            os.chdir(directory_path)
            print(f"Changed working directory to: {directory_path}")
        except FileNotFoundError:
            print(f"The folder '{directory_path}' does not exist.")
        
        contents = os.listdir(directory_path)

        for item in contents:
            print(item)


if __name__ == "__main__":
    main()
