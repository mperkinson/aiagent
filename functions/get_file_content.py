import os
from model_config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    fullpath = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not fullpath.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(fullpath):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(fullpath, "r") as f:
            file_content = f.read(MAX_CHARS)

        if len(file_content) == MAX_CHARS:
            file_content += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )

        return file_content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=("Reads the content of a specified file up to MAX_CHARS characters"),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file from the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
