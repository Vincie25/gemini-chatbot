import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    parent_dir = os.path.dirname(target_file)
    os.makedirs(parent_dir, exist_ok=True)
    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
            success = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        return success
    except Exception as err:
        return f"Error: {err}"

