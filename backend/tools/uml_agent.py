from llm.llm import llm

from graph.prompts import UML_PROMPT

from tools.uml_generator import generate_mermaid_class


def uml_agent(repository, question):

    diagram = generate_mermaid_class(repository)

    prompt = UML_PROMPT.format(

        diagram=diagram,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content