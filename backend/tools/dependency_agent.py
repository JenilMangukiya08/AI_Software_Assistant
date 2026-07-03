from llm.llm import llm
from graph.prompts import DEPENDENCY_PROMPT

from tools.dependency_analyzer import read_dependencies


def dependency_agent(repository, question):

    dependencies = read_dependencies(repository)

    if not dependencies:

        return None

    prompt = DEPENDENCY_PROMPT.format(

        dependencies=dependencies,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content