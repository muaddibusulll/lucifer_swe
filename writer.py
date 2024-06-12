import os
import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_project_info(file_content):
    # Regular expression pattern to extract project path
    path_pattern = r'Project Path: (.+)'
    # Regular expression pattern to extract project name
    name_pattern = r'\n(.+)\n├──'

    # Find the project path
    path_match = re.search(path_pattern, file_content)
    project_path = path_match.group(1) if path_match else None

    # Find the project name
    name_match = re.search(name_pattern, file_content)
    project_name = name_match.group(1).strip() if name_match else None

    return project_path, project_name



def validate_response(response: str):
    response = response.strip()
    if "~~~" not in response:
        return False

    response = response.split("~~~", 1)[1]
    response = response[:response.rfind("~~~")]
    response = response.strip()

    result = []
    current_file = None
    current_code = []
    code_block = False

    for line in response.split("\n"):
        if line.startswith("File: "):
            if current_file and current_code:
                result.append({"file": current_file, "code": "\n".join(current_code)})
            current_file = line.split(":")[1].strip()
            current_code = []
            code_block = False
        elif line.startswith("```"):
            code_block = not code_block
        else:
            current_code.append(line)

    if current_file and current_code:
        result.append({"file": current_file, "code": "\n".join(current_code)})

    return result
def sanitize_filename(filename):
    # Remove backticks and quotes from the filename
    return filename.replace('`', '').replace('"', '').replace("'", "")
def save_code_to_project(response, codebase_path_txt):
    file_path_dir = None
    project_dir, project_name = extract_project_info(read_file(codebase_path_txt))
    print(project_dir, project_name)

    for file in response:
        file_path = os.path.join(project_dir, sanitize_filename(file['file']))
        print(file_path)
        file_path_dir = os.path.dirname(file_path)
        os.makedirs(file_path_dir, exist_ok=True)

        # Check if the file exists
        if os.path.exists(file_path):
            mode = "w"  # Read and write mode if the file exists
        else:
            mode = "w"  # Write mode if the file does not exist

        # Write to the file
        with open(file_path, mode, encoding="utf-8") as f:
            if mode == "r+":
                f.write(file["code"])
            else:
                f.write(file["code"])
    
    return file_path_dir
