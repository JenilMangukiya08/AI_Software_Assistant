from .context_extractor import extract_relevant_context


def generate_activity(repository, question):

    context = extract_relevant_context(
        repository,
        question,
        max_nodes=5,
        max_chars=7000
    )

    if not context:

        return "No matching function found."

    return context