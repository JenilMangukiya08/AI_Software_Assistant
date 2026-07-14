from .class_diagram import generate_mermaid
from .sequence_diagram import generate_sequence
from .activity_diagram import generate_activity
from .state_diagram import generate_state


def generate_uml(repository, question):

    q = question.lower()

    ###################################################
    # Sequence Diagram
    ###################################################

    if "sequence" in q:

        return generate_sequence(
            repository,
            question
        )

    ###################################################
    # Activity Diagram
    ###################################################

    elif "activity" in q:

        return generate_activity(
            repository,
            question
        )

    ###################################################
    # State Diagram
    ###################################################

    elif "state" in q:

        return generate_state(
            repository,
            question
        )

    ###################################################
    # Default
    ###################################################

    else:

        return generate_mermaid(
            repository
        )