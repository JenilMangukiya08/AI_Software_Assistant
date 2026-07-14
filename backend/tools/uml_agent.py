from llm.llm import llm

from graph.prompts import (
    UML_PROMPT,
    ACTIVITY_PROMPT,
    STATE_PROMPT,
)

from tools.uml.state_diagram import generate_state
from tools.uml import generate_uml
from tools.uml.activity_diagram import generate_activity


def uml_agent(repository, question):

    question_lower = question.lower()

    ####################################################
    # Activity Diagram (LLM)
    ####################################################

    if "activity" in question_lower:

        code = generate_activity(
            repository,
            question
        )

        if code == "No matching function found.":

            return code

        prompt = ACTIVITY_PROMPT.format(

            question=question,
            code=code

        )

        response = llm.invoke(prompt)

        return response.content

    ####################################################
    # Class / Sequence / Others
    ####################################################

    diagram = generate_uml(
        repository,
        question
    )

    ####################################################
    # State Diagram (LLM)
    ####################################################

    if "state" in question_lower:

        code = generate_state(
            repository,
            question
        )

        if code == "No repository context found.":

            return code

        prompt = STATE_PROMPT.format(

            question=question,
            code=code

        )

        response = llm.invoke(prompt)

        return response.content
    

    ####################################################
    # Diagram request
    ####################################################

    diagram_keywords = [

        "class diagram",
        "sequence diagram",
        "uml",
        "generate diagram",
        "create diagram",
        "draw diagram",
        "mermaid",

    ]

    if any(word in question_lower for word in diagram_keywords):

        return f"""```mermaid
{diagram}
```"""

    ####################################################
    # Explanation
    ####################################################

    prompt = UML_PROMPT.format(

        diagram=diagram,
        question=question

    )

    response = llm.invoke(prompt)

    return response.content