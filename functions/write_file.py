import os
from google import genai
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in a specified directory relative to the working directory, displaying how many characters were written to it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to display content from, relative to the working directory. It is a required parameter.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written in the provided file path. It is a required parameter.",
            )
        },
        required=["file_path", "content"]
    ),
)


def write_file(working_directory, file_path, content):
    abs_path_work_dir = os.path.abspath(working_directory)
    #print(abs_path_work_dir)
    dir_path = os.path.join(abs_path_work_dir, file_path)
    #print(dir_path)
    cleaned_file_path = os.path.normpath(dir_path)

    #print(cleaned_file_path)
    valid_target_dir = os.path.commonpath([abs_path_work_dir, cleaned_file_path]) == abs_path_work_dir
    print(f"Result for '{file_path}' file path:")

    #print(valid_target_dir)
    if not valid_target_dir:
        err = f"\tError: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        print(err)
        return err

    dir_path = os.path.dirname(cleaned_file_path)
    os.makedirs(dir_path, exist_ok=True)
    if os.path.exists(cleaned_file_path) and not os.path.isfile(cleaned_file_path):
        err = f"\tError: Cannot write to \"{cleaned_file_path}\" as it is a directory"
        print(err)
        return err

    try:
        with open(cleaned_file_path, "w") as f:
            f.write(content)
            msg = f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
            print(msg)
            return msg
    except Exception as e:
        err = f"\tError: {e}"
        print(err)
        return err
