from llm.llm import llm

from graph.prompts import EXECUTION_PROMPT

from tools.code_runner import execute_python


def execution_agent(repository, question, filename):

    result = execute_python(

        repository,

        filename

    )

    prompt = EXECUTION_PROMPT.format(

        result=result,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content