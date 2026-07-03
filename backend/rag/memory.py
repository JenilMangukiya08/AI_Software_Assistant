from api.models import ChatMessage


def get_memory(session, limit=8):

    chats = (
        ChatMessage.objects
        .filter(session=session)
        .order_by("created_at")
    )

    memory = ""

    for chat in chats:

        if chat.sender == "user":

            memory += f"User: {chat.message}\n"

        else:

            memory += f"Assistant: {chat.message}\n"

    return memory