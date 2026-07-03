from rag.qa import ask_repository
from rag.utils import retrieve_context
from graph.prompts import DOCUMENTATION_PROMPT,REVIEW_PROMPT,BUG_PROMPT,TEST_PROMPT
from llm.llm import llm
from tools.tool_router import execute_tool
from tools.utils import extract_filename
def get_context(state):

    context, sources = retrieve_context(
        state["repository"],
        state["question"]
    )

    return context, sources

def repository_node(state):
    
    answer,sources = execute_tool(
            state["repository"],
            state["question"],
        )
    if answer is not None:
        return {
            **state,
            "answer": answer,
            "sources": sources
        }
    
    context, sources = get_context(state)

    answer = ask_repository(
        state["repository"],
        state["question"],
        history=state.get("history", []),
    )

    history = state.get("history", [])

    history.append({
        "agent": "repository",
        "answer": answer["answer"]
    })

    return {
        **state,
        "answer": answer["answer"],
        "sources": sources,
        "history":history
    }




def documentation_node(state):

    context, sources = get_context(state)

    response = llm.invoke(
    DOCUMENTATION_PROMPT.format(
        memory=state["memory"],
        context=context,
        question=state["question"],
        history=state.get("history", []),
    )
)
    history = state.get("history", [])

    history.append({
        "agent": "repository",
        "answer": response["response"]
    })

    return {
        **state,
        "answer": response.content,
        "sources":sources,
        "history":history
    }


def review_node(state):

    context, sources = get_context(state)

    response = llm.invoke(
    REVIEW_PROMPT.format(
        memory=state["memory"],
        context=context,
        question=state["question"],
        history=state.get("history", []),
    )
    )
    history = state.get("history", [])

    history.append({
        "agent": "repository",
        "answer": response["response"]
    })

    return {
        **state,
        "answer": response.content,
        "sources": sources,
        "history":history
    }


def bug_node(state):

    context, sources = get_context(state)

    response = llm.invoke(
    BUG_PROMPT.format(
        memory=state["memory"],
        context=context,
        question=state["question"],
        history=state.get("history", []),
    )
    )
    history = state.get("history", [])

    history.append({
        "agent": "repository",
        "answer": response["response"]
    })

    return {
    **state,
    "answer": response.content,
    "sources": sources,
    "history":history
}


def test_node(state):

    context, sources = get_context(state)


    response = llm.invoke(
    TEST_PROMPT.format(
        memory=state["memory"],
        context=context,
        question=state["question"],
        history=state.get("history", []),
    )
    )
    history = state.get("history", [])

    history.append({
        "agent": "repository",
        "answer": response["response"]
    })

    return {
        **state,
        "answer": response.content,
        "sources":sources,
        "history":history
    }