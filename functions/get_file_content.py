import os
from google.genai import types

# not sure how to reference a config file that is upward in directory hierarchy
FILE_CHARACTER_LIMIT = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)
    if not full_path.startswith(working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    file_content_string = ""
    
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read()
    except Exception as e:
        return f"Error: {e}"
    if len(file_content_string) > FILE_CHARACTER_LIMIT:
        file_content_string = f'{file_content_string[:FILE_CHARACTER_LIMIT]}[...File "{file_path}" truncated at 10000 characters]'
    return file_content_string


#os.path.abspath: Get an absolute path from a relative path
#os.path.join: Join two paths together safely (handles slashes)
#.startswith: Check if a string starts with a specific substring
#os.path.isfile: Check if a path is a file

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the string content of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get string content from, relative to the working directory.",
            ),
        },
    ),
)