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
    
    generate_content(client, messages, verbose)

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

    if not response.function_calls:
        return response.text

    for fc in response.function_calls:
        result = call_function(fc, verbose)
        if not result.parts[0].function_response.response:
            raise Exception("No response found!")
        if verbose:
            print(f'-> {result.parts[0].function_response.response}')
        result_dict = result.parts[0].function_response.response
        print(result_dict['result'])

main()
