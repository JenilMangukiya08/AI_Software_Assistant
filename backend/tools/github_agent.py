from llm.llm import llm

from graph.prompts import GITHUB_PROMPT

from tools.github_tool import *

def github_agent(repository, question):

    commits = get_recent_commits(repository)

    branches = get_branches(repository)

    contributors = get_contributors(repository)

    changed = latest_changed_files(repository)

    info = f"""

Recent Commits

{commits}

Branches

{branches}

Contributors

{contributors}

Latest Changed Files

{changed}

"""

    prompt = GITHUB_PROMPT.format(

        information=info,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content