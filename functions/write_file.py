import os
from google.genai import types

def write_file(working_directory, file_path, content):
    wabs_path = os.path.abspath(working_directory)
    target_path = os.path.join(working_directory, file_path)
    joined_path = os.path.abspath(target_path)

    # outside check
    if not joined_path.startswith(wabs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # create/write to file
    try:
        with open(joined_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as E:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the given file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that will be written to the file.",
            ),
        },
    ),
)
