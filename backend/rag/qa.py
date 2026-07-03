import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from rag.utils import retrieve_context

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)



from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are an expert software engineer who explains GitHub repositories.

You are given one or more source files.
Conversation History
--------------------
{memory}
                                          
Repository Context:
------------------
{context}

User Question:
{question}

Rules:

1. If the repository context contains a file whose path matches the requested filename, assume that IS the requested file.

2. Never answer:
"There is no workflow.py file..."
"There is no state.py file..."
"There is no planner.py file..."
if the file path exists in the context.

3. Explain:
- the purpose of the file
- important classes/functions
- workflow
- how it interacts with other files

4. Base your answer ONLY on the repository context.
5. Answer using BOTH the conversation history and the repository context.
6. If the question refers to "this", "that", "it", "the function", etc.,
use the conversation history to determine what the user is referring to.
                                          
Return the answer in Markdown.
""")
def ask_repository(repository, question, memory=""):

    if memory:
        search_query = memory + "\n\nCurrent Question:\n" + question

    context, sources = retrieve_context(
        repository,
        search_query
    )

    print("=" * 80)
    print("CONTEXT")
    print(context)
    print("=" * 80)

    chain = prompt | llm

    filename = ""

    for word in question.split():

        if "." in word:

            filename = word.strip(".,?!")

            break

    response = chain.invoke({
        "filename": filename,
        "memory": memory,
        "context": context,
        "question": question

    })

    return {

        "answer": response.content,

        "sources": sources

    }