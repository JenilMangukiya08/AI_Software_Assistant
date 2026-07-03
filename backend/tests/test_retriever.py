from rag.utils import retrieve_context


context, sources = retrieve_context(
    "What is this project about?"
)

print(context)

print()

print(sources)