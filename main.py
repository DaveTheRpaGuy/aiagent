import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    #if len(sys.argv) < 2:
    #    print("Invalid number of arguments. Must provide prompt.")
    #    sys.exit(1)

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    
    # TODO -- fix
    MAX_ITERS = 5

    user_prompt = sys.argv[1]
    
    verbose = "--verbose" in sys.argv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None or api_key == "":
        raise RuntimeError("API Key is empty")
    
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    iters = 0
    while iters < MAX_ITERS:
        iters+=1
        try:
            response = client.models.generate_content(
                model=model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt),
                )
        except Exception as e:
            print(f"Generate Content error: {e}")
            break
        
        if response.text and not response.function_calls:
            print(f"response.text: {response.text}")
            break
        else:
            for candidate in response.candidates:
                messages.append(candidate.content)

            if not response.usage_metadata:
                raise RuntimeError("Gemini API response appears to be malformed")
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count

            if response.function_calls:
                function_responses = []
                for function_call_part in response.function_calls:
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                    function_call_result = call_function(function_call_part, verbose)
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception("Fatal: function_call_result.parts[0].function_response.response not found")
                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    function_responses.append(function_call_result.parts[0])
                messages.append(
                    types.Content(
                        role="user",
                        parts=function_responses
                    )
                )
            else:
                print(f"Response: {response.text}")

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

    if iters >= MAX_ITERS:
        print(f"Maximum iterations ({MAX_ITERS}) reached.")

if __name__ == "__main__":
    main()
