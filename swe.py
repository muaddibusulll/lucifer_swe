from openai import OpenAI
import difflib
import os
from planner import planner_prompt, parse_response
from coder import coder_prompt
from writer import validate_response, save_code_to_project
import json
# Set your OpenAI API key
_api_key =  '<API_KEY>'

client=OpenAI(api_key=_api_key)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def planner_inference(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": planner_prompt(prompt)}],
        max_tokens=1500,
        temperature=0.0,
        n=1,
        stop=None
    )


    solution = response.choices[0].message.content
    return parse_response(solution)

def coder_inference(plan, issue, codebase):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": coder_prompt(plan, issue, codebase)}],
        max_tokens=1500,
        temperature=0.0,
        n=1,
        stop=None
    )
    return response.choices[0].message.content


def get_prompt(codebase, issue):
    return f"Here is a codebase:\n\n{codebase}\n\nThe issue is:\n{issue}\n\nPlease solve the issue and provide the updated codebase."

def get_gpt_solution(codebase, issue):
    prompt = get_prompt(codebase, issue)
    plan_dict=json.dumps(planner_inference(prompt)['plans'])
    return coder_inference(plan_dict, issue, codebase)


def compare_codebases(original, modified):
    original_lines = original.splitlines()
    modified_lines = modified.splitlines()
    diff = difflib.unified_diff(original_lines, modified_lines, fromfile='original', tofile='modified', lineterm='')
    return '\n'.join(list(diff))

def main():
    # Input file paths
    codebase_file = '/Users/mohdtahaabbas/swe/examplecodebase2/examplecodebase2.txt'
    issue_file = '/Users/mohdtahaabbas/swe/issue.txt'

    # Read the codebase and issue
    codebase = read_file(codebase_file)
    issue = read_file(issue_file)

    # Get the solution from GPT
    solution = get_gpt_solution(codebase, issue)

    # Write the modified codebase to a new file
    modified_codebase_file = 'modified_codebase_examplecodebase2.txt'
    write_file(modified_codebase_file, solution)

    # Compare the original and modified codebases
    diff = compare_codebases(codebase, solution)

    # Output the difference
    diff_file = 'diffexamplecodebase2.txt'
    write_file(diff_file, diff)
    print(validate_response(solution))

    print(f'Differences saved to {diff_file}')

    print("writing to file")

    save_code_to_project(validate_response(solution), codebase_file)

    print("Done")


if __name__ == '__main__':

    main()
    
