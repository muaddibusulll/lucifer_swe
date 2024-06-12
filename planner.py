
def planner_prompt(prompt):
    return f"""You are Lucifer, an AI Software Engineer.

    The user asked: {prompt}

    Based on the user's request, create a step-by-step plan to accomplish the task.

    Follow this format for your response:

    ```
    Project Name: <Write an apt project name with no longer than 5 words>

    Your Reply to the Human Prompter: <short human-like response to the prompt stating how you are creating the plan, do not start with "As an AI".>

    Current Focus: Briefly state the main objective or focus area for the plan.

    Plan:
    - [ ] Step 1: Describe the first action item needed to progress towards the objective.
    - [ ] Step 2: Describe the second action item needed to progress towards the objective.
    ...
    - [ ] Step N: Describe the final action item needed to complete the objective.

    Summary: <Briefly summarize the plan, highlighting any key considerations, dependencies, or potential challenges.>
    ```

    Each step should be a clear, concise description of a specific task or action required. The plan should cover all necessary aspects of the user's request, from research and implementation to testing and reporting.

    Write the plan with knowing that you have access to the browser and search engine to accomplish the task.

    After listing the steps, provide a brief summary of the plan, highlighting any key considerations, dependencies, or potential challenges.

    Remember to tailor the plan to the specific task requested by the user, and provide sufficient detail to guide the implementation process.

    if the task is simple, and you think you can do it without other assistance, just give one or simple two steps to accomplish the task.
    don't need to overcomplicate if it's not necessary.

    Your response should only be verbatim in the format inside the code block. Any other response format will be rejected."""

def parse_response(response: str):
    result = {
        "project": "",
        "reply": "",
        "focus": "",
        "plans": {},
        "summary": ""
    }

    current_section = None
    current_step = None

    for line in response.split("\n"):
        line = line.strip()

        if line.startswith("Project Name:"):
            current_section = "project"
            result["project"] = line.split(":", 1)[1].strip()            
        elif line.startswith("Your Reply to the Human Prompter:"):
            current_section = "reply"
            result["reply"] = line.split(":", 1)[1].strip()
        elif line.startswith("Current Focus:"):
            current_section = "focus"
            result["focus"] = line.split(":", 1)[1].strip()
        elif line.startswith("Plan:"):
            current_section = "plans"
        elif line.startswith("Summary:"):
            current_section = "summary"
            result["summary"] = line.split(":", 1)[1].strip()
        elif current_section == "reply":
            result["reply"] += " " + line
        elif current_section == "focus":
            result["focus"] += " " + line
        elif current_section == "plans":
            if line.startswith("- [ ] Step"):
                current_step = line.split(":")[0].strip().split(" ")[-1]
                result["plans"][int(current_step)] = line.split(":", 1)[1].strip()
            elif current_step:
                result["plans"][int(current_step)] += " " + line
        elif current_section == "summary":
            result["summary"] += " " + line.replace("```", "")

    result["project"] = result["project"].strip()
    result["reply"] = result["reply"].strip()
    result["focus"] = result["focus"].strip()
    result["summary"] = result["summary"].strip()

    return result  