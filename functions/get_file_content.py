import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            content_string = f.read(MAX_CHARS)
            if f.read(1):
                content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content_string
    except Exception as err:
        return f"Error: {err}"
