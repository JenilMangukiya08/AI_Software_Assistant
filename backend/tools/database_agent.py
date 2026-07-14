from llm.llm import llm

from graph.prompts import DATABASE_PROMPT

from tools.database_parser import (
    generate_er_diagram,
    build_database_summary,
    build_database_suggestions,
)



def database_agent(repository, question):

    

    diagram = generate_er_diagram(repository)

    summary = build_database_summary(repository)

    suggestions = "\n".join(
        f"- {s}"
        for s in build_database_suggestions(repository)
    )

    prompt = DATABASE_PROMPT.format(
    diagram=diagram,
    summary=summary,
    suggestions=suggestions,
    question=question
)

    response = llm.invoke(prompt)

    return response.content