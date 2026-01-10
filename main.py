import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    print("Hello from ai-agent!")

    # load env and check AI api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if(api_key is None):
        raise RuntimeError("missing AI key!")

    # build AI client
    client = genai.Client(api_key=api_key)

    # parse user prompt and flag args
    parser = argparse.ArgumentParser(description="Devbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.user_prompt

    # create roles
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # get response
    response = client.models.generate_content(model='gemini-2.5-flash', contents=messages, 
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    resp_meta = response.usage_metadata

    # display verbose response
    if(args.verbose):
        #print(f"User prompt: {user_prompt}")
        if (resp_meta is not None):
            response_prompt_tokens = f"Prompt tokens: {resp_meta.prompt_token_count}"
            response_tokens = f"Response tokens: {resp_meta.candidates_token_count}"
            print(f"{response_prompt_tokens}\n{response_tokens}")

    # display function call results
    if not (response.function_calls is None):
        #print(f"checking function calls: {len(response.function_calls)}")
        for func in response.function_calls:
            func_call_res = call_function(func)
            if len(func_call_res.parts) == 0:
                err = f"\tError: function call result parts list is empty!"
                raise Exception(err)

            if func_call_res.parts[0].function_response is None:
                err = f"\tError: function call result parts first item response object is None!"
                raise Exception(err)

            if func_call_res.parts[0].function_response.response is None:
                err = f"\tError: function call result parts first item response is None!"
                raise Exception(err)

            func_results = [func_call_res.parts[0]]

            output = ""
            if args.verbose:
                output = f"-> {func_call_res.parts[0].function_response.response}"
            else:
                output = f"Calling function: {func.name}({func.args})"

            print(output)

    # display simple response
    print(response.text)


if __name__ == "__main__":
    main()
