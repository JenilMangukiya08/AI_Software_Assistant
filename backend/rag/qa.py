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
You are an expert Software Engineer specialized in understanding GitHub repositories.

Your job is to answer questions accurately using BOTH the repository context and the conversation history.

========================================================
CONVERSATION HISTORY
========================================================

{memory}

========================================================
REPOSITORY CONTEXT
========================================================

{context}

========================================================
CURRENT QUESTION
========================================================

{question}

========================================================
INSTRUCTIONS
========================================================

1. Repository Context is your PRIMARY source of truth.

2. Conversation History is ONLY used to understand follow-up questions.

Examples:

User:
Explain workflow.py

User:
Why is planner before router?

→ "planner" refers to workflow.py.

----------------------------------------

User:
Explain planner.py

User:
How do these two files interact?

→ "these two files" refers to
workflow.py and planner.py.

----------------------------------------

3. If the current question refers to:

- it
- this
- that
- they
- these
- those
- the function
- the file
- planner
- router

use the conversation history to identify what the user means.

4. Never restart the explanation if this is a follow-up question.

Instead of saying:

"workflow.py defines..."

say:

"As discussed earlier, workflow.py..."

5. Never invent classes,
functions,
files,
or architecture.

If the repository context does not contain enough information,
say:

"I couldn't find enough information in the repository."

6. Explain only what is supported by the repository context.

7. Mention filenames whenever possible.

8. If multiple files are involved,
explain how they interact.

9. If reviewing code,

always provide:

• Observation

• Evidence from the code

• Recommendation

Do not provide generic software engineering advice.

10. Return the answer in clean Markdown.

""")

def ask_repository(repository, question, memory=""):

    # Retrieval should only use the current question
    context, sources = retrieve_context(
        repository,
        question
    )

    print("=" * 80)
    print("MEMORY")
    print(memory)
    print("=" * 80)

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