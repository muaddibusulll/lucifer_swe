def coder_prompt(step_by_step_plan, user_context, knowledge_base_context): 


 return f"""Project Step-by-step Plan:
```
{ step_by_step_plan }
```

Context From User:
```
{ user_context }
```

Context From Knowledge Base:

{ knowledge_base_context}


Read the step-by-step plan carefully. Think step-by-step. Learn relevant information from the knowledge base context. Then write the code to implement the step-by-step plan.

Your response should only be in the following Markdown format:

~~~
File: `main.py`:
```py
print("Example")
```

File: `nested/directory/example/code.py`:
```py
print("Example")
```

File: `README.md`
```md
# Example

This is an example.
```
~~~

Rules:
- You should write clean and documented code.
- The code should work on the first try without any errors or bugs.
- Choose the library or dependency you know best.
- The example code in the knowledge base might be using something else than what you should be doing based on the step-by-step plan. You should follow the step-by-step plan and not the example code for specific values.
- The extension used for the Markdown code blocks should be accurate.
- Nested directories should be specified in the Markdown filename, the code structure should be accurate. If it requires to be nested to work, then it should be nested.
- You need to include required files for the code to run. Like: requirements.txt, Cargo.toml, etc.
- Files like Cargo.toml are mandatory to be included, the project won't work without it.

Any response other than this format will be rejected. You should not refuse to complete the task, you should try your absolute best and if there's any implementation detail that's impossible to complete, you should write a comment in the code explaining why it's impossible to complete. The refusal is only a last resort, it should never happen.

Your response should start with "~~~" and end with "~~~" just like the example format provided. Never provide any explanation or context inside the response, only the filenames and the code in the format provided. Do not leave any "Note"."""