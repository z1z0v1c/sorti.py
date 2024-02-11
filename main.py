import os
import sys

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
