from typing import TypedDict

class GraphState(TypedDict):
    repository:str
    question: str
    intent: str
    answer: str
    route: str
    sources: list[str]
    memory:str
    plan:list[str]
    current_step:int
    history:list[str]
    current_file: str
    trace: list
    metrics: dict