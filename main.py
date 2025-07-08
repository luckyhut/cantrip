import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("Error: prompt is required as an argument")
        sys.exit(1)
        
    verbose = False
    if len(args) > 1 and args[1] == '--verbose':
        verbose = True

    # user_prompt = " ".join(args)
    user_prompt = args[0]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages)
    
    print(response.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: { response.usage_metadata.prompt_token_count }")
        print(f"Response tokens: { response.usage_metadata.candidates_token_count }")

main()
