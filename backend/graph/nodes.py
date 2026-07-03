from rag.qa import ask_repository
from rag.utils import retrieve_context
from graph.prompts import DOCUMENTATION_PROMPT,REVIEW_PROMPT,BUG_PROMPT,TEST_PROMPT
from llm.llm import llm

def get_context(state):

    context, sources = retrieve_context(
        state["repository"],
        state["question"]
    )

    return context, sources

def repository_node(state):

    sources = get_context(state)

    answer = ask_repository(
        state["repository"],
        state["question"]
    )

    return {
        **state,
        "answer": answer["answer"],
        "sources": sources
    }


def documentation_node(state):

    context, sources = get_context(state)

    response = llm.invoke(
    DOCUMENTATION_PROMPT.format(
        memory=state["memory"],
        context=context,
        question=state["question"]
    )
)

    return {
        **state,
        "answer": response.content,
        "sources":sources
    }


def review_node(state):

    context, sources = get_context(state)

    response = llm.invoke(
    REVIEW_PROMPT.format(
        memory=state["memory"],
        context=context,
        question=state["question"]
    )
    )

    return {
        **state,
        "answer": response.content,
        "sources": sources
    }


def bug_node(state):

    context, sources = get_context(state)

    response = llm.invoke(
    BUG_PROMPT.format(
        memory=state["memory"],
        context=context,
        question=state["question"]
    )
    )

    return {
    **state,
    "answer": response.content,
    "sources": sources
}


def test_node(state):

    context, sources = get_context(state)


    response = llm.invoke(
    TEST_PROMPT.format(
        memory=state["memory"],
        context=context,
        question=state["question"]
    )
    )

    return {
        **state,
        "answer": response.content,
        "sources":sources
    }