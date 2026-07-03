from typing import TypedDict

class GraphState(TypedDict):
    repository:str
    question: str
    intent: str
    answer: str
    route: str
    sources: list[str]
    memory:str