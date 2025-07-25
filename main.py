import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("Error: prompt is required as an argument")
        sys.exit(1)
        
    verbose = False
    if len(args) > 1 and args[1] == '--verbose':
        verbose = True
    
    user_prompt = args[0]
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(1, 10):
        try:
            response = generate_content(client, messages, verbose)
            if response:
                print("Final response:")
                print(response)
                return
        except Exception as e:
            print(f'Error, exited process: {e}')

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config = types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )
    if verbose:
        print(f"Prompt tokens: { response.usage_metadata.prompt_token_count }")
        print(f"Response tokens: { response.usage_metadata.candidates_token_count }")

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
        
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        
        if verbose:
            print(f'-> {function_call_result.parts[0].function_response.response}')
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role='tool', parts=function_responses))

main()
