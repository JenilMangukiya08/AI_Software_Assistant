from llm.llm import llm

from graph.prompts import PROJECT_STRUCTURE_PROMPT

from tools.project_structure import (
    build_tree,
    read_readme
)


def architecture_agent(repository, question):

    tree = build_tree(repository)

    readme = read_readme(repository)

    prompt = PROJECT_STRUCTURE_PROMPT.format(

        tree=tree,

        readme=readme,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content