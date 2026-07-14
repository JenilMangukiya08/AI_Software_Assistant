from rag.context_manager import get_context


def extract_relevant_context(
    repository,
    question,
    max_nodes=8,
    max_chars=7000
):

    context, _ = get_context(
        repository,
        question,
        "uml"
    )

    return context