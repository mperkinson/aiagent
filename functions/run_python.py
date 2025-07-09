import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    fullpath = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not fullpath.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(fullpath):
        return f'Error: File "{file_path}" not found.'

    python_file_extension = ".py"
    if not fullpath.endswith(python_file_extension):
        return f'Error: "{file_path}" is not a Python file.'

    commands = ["python3", fullpath]

    if args:
        commands.extend(args)

    try:
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )

        output = []
        stdout = result.stdout
        stderr = result.stderr
        return_code = result.returncode
        if stdout:
            # Hack to satisfy testing output requirement
            # output.append(f"STDOUT:\n{stdout}")
            output.append(stdout)
        if stderr:
            # Hack to satisfy testing output requirement
            # output.append(f"STDERR:\n{stderr}")
            output.append(stderr)
        if return_code != 0:
            output.append(f"Process exited with code {return_code}")
        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: excuting Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file located within a specified working directory and returns the output."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to be executed, based on the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
