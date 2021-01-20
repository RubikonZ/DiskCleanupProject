import glob
from pathlib import Path
import os

#  os.path.isdir(d) To check if file is directory
# path.cwd() - Current working directory

def check_folder(folder_path):
    print(f'I started checking "{folder_path}" path')
    if not glob.glob(f'{folder_path}/*'):
        print(f"Directory is empty: '{folder_path}'")
    else:
        for file in glob.glob(f'{folder_path}/*'):
            if file:
                # print(f'{file} exists')
                if os.path.isdir(file):
                    # How to make it iterate until the end
                    print(f'"{file}" is folder. Checking this folder as well')
                    check_folder(Path(file).absolute())



if __name__ == '__main__':
    initial_folder = Path.cwd()  # Path where user chooses to start checking folders
    check_folder(initial_folder)
