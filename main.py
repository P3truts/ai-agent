import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from agent import run_ai_agent


def main():
    print("Hello from ai-agent!")

    # load env and check AI api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if(api_key is None):
        raise RuntimeError("missing AI key!")

    # build AI client
    client = genai.Client(api_key=api_key)

    run_ai_agent(client)


if __name__ == "__main__":
    main()

