import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt


def main() ->None:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("Environment variable 'GEMINI_API_KEY' not found."
                       "Please set it in your environment or .env file.")
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-3-flash', contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],
                                               system_instruction=system_prompt)
            )
        if response.usage_metadata is None:
            raise RuntimeError("failed API request")
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if not response.function_calls:
            print(response.text)
            return
        else:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("Error")
                if not function_call_result.parts[0].function_response:
                    raise Exception("Error")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Error")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
    print("Maximum iterations reached without final response")
    exit(1)


if __name__ == "__main__":
    main()
