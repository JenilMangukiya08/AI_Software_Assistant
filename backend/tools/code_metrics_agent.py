from llm.llm import llm
import json

from tools.code_metrics.report import generate_metrics
from graph.prompts import CODE_METRICS_PROMPT

def code_metrics_agent(repository, question):

    metrics = generate_metrics(repository)

    prompt = CODE_METRICS_PROMPT.format(

        metrics=json.dumps(
            metrics,
            indent=2
        ),

        question=question

    )

    response = llm.invoke(prompt)

    return response.content