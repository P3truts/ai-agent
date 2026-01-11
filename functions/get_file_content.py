#from ..config import MAX_CHARS
import os
from google import genai
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Displays file content with a limit of 10000 characters in a specified directory relative to the working directory, providing details if the file was truncated because of the read limit.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to display content from, relative to the working directory. It is a required parameter.",
            ),
        },
        required=["file_path"]
    ),
)


def get_file_content(working_directory, file_path):
    abs_path_work_dir = os.path.abspath(working_directory)
    #print(abs_path_work_dir)
    dir_path = os.path.join(abs_path_work_dir, file_path)
    #print(dir_path)
    cleaned_file_path = os.path.normpath(dir_path)

    #print(cleaned_file_path)
    valid_target_dir = os.path.commonpath([abs_path_work_dir, cleaned_file_path]) == abs_path_work_dir
    #print(f"Result for '{file_path}' file path:")

    #print(valid_target_dir)
    if not valid_target_dir:
        err = f"\tError: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        print(err)
        return err

    if not os.path.isfile(cleaned_file_path):
        err = f"\tError: file not found or is not a regular file: {file_path}"
        print(err)
        return err

    MAX_CHARS = 10000

    try:
        #print(cleaned_file_path)
        with open(cleaned_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{cleaned_file_path}" truncated at {MAX_CHARS} characters]'
            cont_len = len(file_content_string)
            #print(f"File content length: {cont_len}")
            #print(file_content_string)
            return file_content_string

    except Exception as e:
        err = f"\tError: {e}"
        print(err)
        return err

