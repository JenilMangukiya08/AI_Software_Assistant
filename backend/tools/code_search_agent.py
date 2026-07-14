from tools.code_search import search_code

from graph.prompts import CODE_SEARCH_PROMPT

from llm.llm import llm
import re


def build_search_query(question):

    question = question.lower()

    question = re.sub(
        r"(find|search|locate|show|where is|where|display|give me|list|tell me|identify)",
        "",
        question
    )

    question = re.sub(
        r"(function|method|class|file|code|implementation|definition|defined|called|usage|uses|call|all)",
        "",
        question
    )

    question = re.sub(r"\s+", " ", question)

    return question.strip()
def explain_search(repository, question):

    query = build_search_query(question)

    results = search_code(
        repository,
        query
    )

    if not results:

        return (
            "I couldn't find any matching code "
            "for this question in the repository."
        )
    
    parts = []

    for item in results:

        parts.append(
            f"""
    File:
    {item['file']}

    Line:
    {item['line']}

    Relevance:
    {item['score']}

    Code:
    {item['content']}
    """
        )

    text = "\n\n".join(parts)

    





    prompt = CODE_SEARCH_PROMPT.format(
    query=query,
    results=text
)

    response = llm.invoke(prompt)

    return response.content