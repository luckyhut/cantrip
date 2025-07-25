import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    wabs_path = os.path.abspath(working_directory)
    target_path = os.path.join(working_directory, directory)
    joined_path = os.path.abspath(target_path)
    
    # outside check
    if not joined_path.startswith(wabs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # is dir check
    if not os.path.isdir(joined_path):
        return f'Error: "{directory}" is not a directory'

    result = f'Result for "{directory}" directory:\n'
    for file in os.listdir(joined_path):
        file_size = os.path.getsize(os.path.join(joined_path, file))
        is_dir = os.path.isdir(os.path.join(joined_path, file))
        result += f'- {file}: file_size={file_size} bytes, is_dir={is_dir}\n'

    return result

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
