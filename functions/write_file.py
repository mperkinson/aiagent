import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    fullpath = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not fullpath.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(fullpath):
        try:
            os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        except Exception as e:
            return f"Error: {e}"

    if os.path.exists(fullpath) and os.path.isdir(fullpath):
        return f'Error: "{file_path}" is a directory, not a file'

    try:
        with open(fullpath, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes the provided content to a file located at the specified path."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to write, including the file name.",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="The content to write to the file."
            ),
        },
        required=["file_path", "content"],
    ),
)
