import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    wabs_path = os.path.abspath(working_directory)
    target_path = os.path.join(working_directory, file_path)
    joined_path = os.path.abspath(target_path)

    # outside check
    if not joined_path.startswith(wabs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # exists check
    if not os.path.exists(joined_path):
        return f'Error: File "{file_path}" not found'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    try:
        run_result = subprocess.run(["python", joined_path], capture_output=True, timeout=30, cwd=wabs_path)
        
        result = []
        if run_result.stdout or run_result.stderr:
            result.append(f'STDOUT:\n {run_result.stdout.decode()} ')
            result.append(f'STDERR:\n {run_result.stderr.decode()} ')

        if run_result.returncode != 0:
            result.append(f' \n Process exited with code {run_result.returncode}\n ')

        return "\n".join(result) if result else "No output produced."
    
    except Exception as e:
        return f'Error: executing Python file: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a given python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the given python file.",
            ),
        },
    ),
)
