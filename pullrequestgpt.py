def pullrequestprompt(head_branch, base_branch, issue, diff):
    return f""" You are Lucifer a software engineer at a company that uses GitHub for version control. You have been assigned a task to create a pull request from a colleague. 
    You have been provided with the following information:
    Issue: { issue }
    List of changes that has been done in the feature branch: { diff }
    HEAD_BRACH: { head_branch }
    BASE_BRANCH: { base_branch }

    YOUR TASK IS TO CREATE A PULL REQUEST DATA OF THE FORM:

    
     title: RELEVANT GENERATED TITLE,
     head: HEAD_BRANCH,
     base: BASE_BRANCH,
     body: RELEVANT GENERATED BODY
     

    > GENRATE A RELEVEANT TITLE
    > GENERATE A RELEVANT BODY THAT DESCRIBES THE PULL REQUEST
    > REPLACE HEAD_BRANCH AND BASE_BRANCH WITH THE HEAD AND BASE BRANCHE PROVIDED

    OUTPUT:

    title: RELEVANT GENERATED TITLE,
    head: HEAD_BRANCH,
    base: BASE_BRANCH,
    body: RELEVANT GENERATED BODY
     
     
    > OUTPUT SHOULD BE IN THE FORMAT PROVIDED ABOVE
    > DONT OUTPUT ANYTHINF ELSE OTHER THAN THE FORMAT PROVIDED ABOVE
    """

def parse_request_details(response):
    response = response.strip()
    response = response.split("\n")
    data = {}
    for line in response:
        if line.startswith("title:"):
            data['title'] = line.split(":")[1].strip()
        elif line.startswith("head:"):
            data['head'] = line.split(":")[1].strip()
        elif line.startswith("base:"):  
            data['base'] = line.split(":")[1].strip()
        elif line.startswith("body:"):
            data['body'] = line.split(":")[1].strip()
    return data

if __name__ == '__main__':
    print(parse_request_details(
        """```plaintext
title: Fix incorrect function implementations in first.py and second.py,
head: feature_branch,
base: main,
body: This pull request addresses the issue where function names in `first.py` and `second.py` were correct but their implementations were incorrect. The following changes have been made:
- Corrected the implementation of the `add` and `multiply` functions in `first.py`.
- Corrected the implementation of the `add` and `multiply` methods in the `testing` class in `second.py`.
- Fixed the `print_sum` method in the `testing` class to correctly call the `add` method.
```"""))