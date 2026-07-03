from llm.llm import llm

from graph.prompts import CODE_METRICS_PROMPT

from tools.code_metrics import calculate_metrics


def code_metrics_agent(repository, question):

    metrics = calculate_metrics(repository)

    prompt = CODE_METRICS_PROMPT.format(

        metrics=metrics,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content