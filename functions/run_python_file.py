import os
import subprocess as sp


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python", target_file]
    if args:
        command.extend(args)
    try:
        sub = sp.run(command,
                     cwd=working_directory,
                     capture_output=True,
                     text=True,
                     timeout=30,
                     check=False)
        output = ""
        if sub.returncode != 0:
            output += f"Process exited with code {sub.returncode}\n"
        if not sub.stdout and not sub.stderr:
            output += "No output produced\n"
        if sub.stdout:
            output += f"STDOUT: {sub.stdout}\n"
        if sub.stderr:
            output += f"STDERR: {sub.stderr}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
