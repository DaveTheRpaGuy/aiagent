import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    working_path = os.path.abspath(working_directory)
    if not full_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    directory_name = ""
    if directory_name == ".":
        directory_name = "current"
    else:
        directory_name = directory
    output = "Result for '{directory_name}' directory:\n"
    for item in os.listdir(full_path):
        try:
            output += f"- {item}: file_size={os.path.getsize(os.path.join(full_path, item))} bytes, is_dir={os.path.isdir(os.path.join(full_path, item))}\n"
        except Exception as e:
            return f"Error: {e}"
    return output
    #- README.md: file_size=1032 bytes, is_dir=False
    #- src: file_size=128 bytes, is_dir=True
    #- package.json: file_size=1234 bytes, is_dir=False


#- os.path.abspath(): Get an absolute path from a relative path
#- os.path.join(): Join two paths together safely (handles slashes)
#- .startswith(): Check if a string starts with a substring
#- os.path.isdir(): Check if a path is a directory
#- os.listdir(): List the contents of a directory
#- os.path.getsize(): Get the size of a file
#- os.path.isfile(): Check if a path is a file
#- .join(): Join a list of strings together with a separator

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)