import os

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