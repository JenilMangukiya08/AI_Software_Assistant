from .context_extractor import extract_relevant_context

def generate_state(repository, question):

    context = extract_relevant_context(
        repository,
        question,
        max_nodes=6,
        max_chars=8000
    )

    if not context:

        return "No repository context found."

    return context