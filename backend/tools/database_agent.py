from llm.llm import llm

from graph.prompts import DATABASE_PROMPT

from tools.database_parser import (
    parse_database,
    generate_er_diagram
)


def database_agent(repository, question):

    models = parse_database(repository)

    diagram = generate_er_diagram(repository)

    prompt = DATABASE_PROMPT.format(

        database=models,

        diagram=diagram,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content