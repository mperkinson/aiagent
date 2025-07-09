import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from model_config import MAX_ITERATIONS, model, system_prompt
from call_function import available_functions, call_function


def generate_content(client, messages, verbose):
    resp = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print("Prompt tokens:", resp.usage_metadata.prompt_token_count)
        print("Response tokens:", resp.usage_metadata.candidates_token_count)

    if resp.candidates:
        for candidate in resp.candidates:
            candidate_content = candidate.content
            if candidate_content:
                messages.append(candidate_content)

    if not resp.function_calls:
        # print("No function call was generated.")
        # if resp.text:
        #     print("Model response:", resp.text)
        return resp.text

    function_responses = []
    for function_call_part in resp.function_calls:
        result = call_function(function_call_part, verbose)
        if not result:
            raise Exception(
                f"No result calling function: {function_call_part.name}({function_call_part.args})"
            )

        if not result.parts or not result.parts[0].function_response:
            raise Exception("Empty function call result")

        result_response = result.parts[0].function_response.response
        if not result_response:
            raise Exception(
                f"No result calling function: {function_call_part.name}({function_call_part.args})"
            )

        if result_response and verbose:
            print(f"-> {result_response}")

        function_responses.append(result.parts[0])
        if not function_responses:
            raise Exception("No function responsed generated.")

        messages.append(types.Content(role="tool", parts=function_responses))


def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if len(args) == 0:
        print("Error: Prompt not provided.")
        print('Usage: python3 main.py "user prompt" [--verbose]')
        sys.exit(1)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    i = 0
    while True:
        i += 1
        if i > MAX_ITERATIONS:
            print(f"Maximum iterations of {MAX_ITERATIONS} reached. Exiting.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
