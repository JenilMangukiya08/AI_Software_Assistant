import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from graph.prompts import ROUTER_PROMPT

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)


def router_node(state):

    question = state["question"]

    response = llm.invoke(

        f"""
{ROUTER_PROMPT}

Question:

{question}
"""

    )

    intent = response.content.strip().lower()

    return {

        **state,

        "intent": intent

    }