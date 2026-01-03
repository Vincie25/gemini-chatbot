import os


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    try:
        target_list = os.listdir(target_dir)
        entries = []
        for i in target_list:
            abs_directory = os.path.join(target_dir, i)
            is_dir = os.path.isdir(abs_directory)
            size = os.path.getsize(abs_directory)
            entry = f"- {i}: file_size={size} bytes, is_dir={is_dir}"
            entries.append(entry)
        entries_string = "\n".join(entries)
        return entries_string
    except IOError as err:
        return f"Error: {err}"
    except Exception as err:
        return f"Error: {err}"
