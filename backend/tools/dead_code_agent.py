from llm.llm import llm

from graph.prompts import DEAD_CODE_PROMPT

from tools.dead_code_detector import detect_dead_code


def dead_code_agent(repository, question):

    report = detect_dead_code(repository)

    prompt = DEAD_CODE_PROMPT.format(

        report=report,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content