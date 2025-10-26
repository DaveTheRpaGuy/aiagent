import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)
    if not full_path.startswith(working_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        try:
            with open(full_path, "x") as f:
                f.write(content)
        except Exception as e:
            return f"Error: {e}"
    else:
        try:            
            with open(full_path, "w") as f:
                f.write(content)
        except Exception as e:
            return f"Error: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        

#os.path.exists: Check if a path exists
#os.makedirs: Create a directory and all its parents
#os.path.dirname: Return the directory name

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates a new file with the provided content or overwrites the file if it already exists, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the Python file that should have the content written to it, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The new string content to write to the file",
            ),
        },
    ),
)