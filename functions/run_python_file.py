import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_path = os.path.abspath(working_directory)
    if not os.path.commonpath([full_path, working_path]) == working_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(["python", full_path, *args], timeout=30, cwd=working_path, capture_output=True, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}."
    stdout = completed_process.stdout
    stderr = completed_process.stderr
    if completed_process.returncode != 0:
        return f"Process exited with code {completed_process.returncode}."
    if stdout == "" and stderr == "":
        return "No output produced."
    return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the Python code contained in the file and returns the result, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the file containing the Python code, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An array of optional arguments",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single command-line argument."
                ),
            ),
        },
    ),
)