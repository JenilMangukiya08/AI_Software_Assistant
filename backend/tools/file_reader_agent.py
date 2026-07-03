from graph.prompts import FILE_READER_PROMPT
from llm.llm import llm

from tools.file_reader import read_file


def explain_file(repository, filename, question):

    content = read_file(
        repository,
        filename
    )

    if content is None:

        return None

    prompt = FILE_READER_PROMPT.format(

        filename=filename,

        content=content,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content