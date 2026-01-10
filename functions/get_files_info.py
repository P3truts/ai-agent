import os
from google import genai
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    abs_path_work_dir = os.path.abspath(working_directory)
    #print(abs_path_work_dir)
    if directory.startswith("/"):
        directory = directory.replace("/", "")
    dir_path = os.path.join(abs_path_work_dir, directory)
    #print(dir_path)
    cleaned_dir_path = os.path.normpath(dir_path)

    #print(cleaned_dir_path)
    valid_target_dir = os.path.commonpath([abs_path_work_dir, cleaned_dir_path]) == abs_path_work_dir

    print(f"Result for '{directory}' directory:")

    #print(valid_target_dir)
    if not valid_target_dir:
        err = f"\tError: Cannot list \"{directory}\" as it is outside the permitted working directory"
        print(err)
        return err

    if not os.path.isdir(cleaned_dir_path):
        err = f"\tError: \"{directory}\" is not a directory"
        print(err)
        return err

    try:
        dir_items = os.listdir(cleaned_dir_path)
        dir_items_list = []

        for item in dir_items:
            item_path = os.path.join(cleaned_dir_path, item)
            file_size = os.path.getsize(item_path)
            if os.path.isfile(item_path):
                item_status = f"\t- {item}: file_size={file_size} bytes, is_dir=False"
            else:
                item_status = f"\t- {item}: file_size={file_size} bytes, is_dir=True"

            dir_items_list.append(item_status)
        print("\n".join(dir_items_list))

    except Exception as e:
        err = f"\tError: {e}"
        print(err)
        return err
