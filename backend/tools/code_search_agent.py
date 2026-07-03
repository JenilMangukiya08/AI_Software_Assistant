from tools.code_search import search_code

from graph.prompts import CODE_SEARCH_PROMPT

from llm.llm import llm


def explain_search(repository, question):

    results = search_code(
        repository,
        question
    )

    if not results:

        return None

    text = ""

    for item in results:

        text += f"""

File:
{item['file']}

Line:
{item['line']}

Code:
{item['content']}

------------------

"""

    prompt = CODE_SEARCH_PROMPT.format(

        query=question,

        results=text

    )

    response = llm.invoke(prompt)

    return response.content