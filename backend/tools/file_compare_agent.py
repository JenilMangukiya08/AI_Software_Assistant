from llm.llm import llm

from graph.prompts import COMPARE_FILES_PROMPT

from tools.file_compare import compare_files


def compare_agent(repository, question, file1, file2):

    diff = compare_files(
        repository,
        file1,
        file2
    )

    if diff is None:

        return "Unable to compare files."

    prompt = COMPARE_FILES_PROMPT.format(

        diff=diff,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content