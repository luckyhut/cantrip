import os
from google.genai import types

def get_file_content(working_directory, file_path):
    wabs_path = os.path.abspath(working_directory)
    target_path = os.path.join(working_directory, file_path)
    joined_path = os.path.abspath(target_path)

    # outside check
    if not joined_path.startswith(wabs_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # exists check
    if not os.path.isfile(joined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        file_content_string = ''
        MAX_CHARS = 10000
        with open(joined_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == 10000:
            file_content_string += '[...File "{file_path}" truncated at 10000 characters].'
    except Exception as e:
        return f'Error: {e}'

    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get contents of given file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to list the contents of.",
            ),
        },
    ),
)
