import os
import subprocess
from google import genai
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python3 file, sometimes with arguments that come in a list, in a specified directory relative to the working directory, displaying the outputs and/or errors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to execute the python3 code from, relative to the working directory. It is a required parameter.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array of arguments to execute the python3 file with. Default is None.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Argument to run a python3 code from a file with."
                )
            ),
        },
        required=["file_path"]
    ),
)


def run_python_file(working_directory, file_path, args=None):
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
        err = f"\tError: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        print(err)
        return err

    if not os.path.isfile(cleaned_file_path):
        err = f"\tError: \"{file_path}\" does not exist or is not a regular file"
        print(err)
        return err

    if not cleaned_file_path.endswith(".py"):
        err = f"\tError: \"{file_path}\" is not a Python file"
        print(err)
        return err

    try:
        command = ["python", cleaned_file_path]
        if not args is None and len(args) != 0:
            for arg in args:
                command.extend(arg)

        res = subprocess.run(command, cwd=abs_path_work_dir, capture_output=True, text=True, timeout=30)

        output = ""
        if not res.stdout and not res.stderr:
            output = f"\tResult: No output produced"
        else:
            output = f"\tResult: STDOUT: {res.stdout} | STDERR: {res.stderr}"
            if res.returncode != 0:
                output += f"\n\tProcesss exited with code {res.returncode}"

        print(output)
        return output
    except Exception as e:
        err = f"\tError: executing Python file: {e}"
        print(err)
        return err

