import os

def get_files_info(working_directory, directory="."):
    combined_path = os.path.join(working_directory, directory)
    directory_absolute_path = os.path.abspath(directory)
    if not directory_absolute_path.startswith(combined_path):
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(directory_absolute_path):
        raise Exception(f'Error: "{directory}" is not a directory')
    output = ""
    for item in os.listdir(directory_absolute_path):
        

    #- README.md: file_size=1032 bytes, is_dir=False
    #- src: file_size=128 bytes, is_dir=True
    #- package.json: file_size=1234 bytes, is_dir=False