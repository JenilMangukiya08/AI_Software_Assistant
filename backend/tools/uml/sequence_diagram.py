import ast
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"

IGNORE = {
    "__pycache__",
    "venv",
    ".git",
    "node_modules",
    "migrations",
    "tests",
}

IGNORE_FUNCTIONS = {

    # Python

    "print",
    "str",
    "len",
    "list",
    "dict",
    "set",
    "tuple",
    "int",
    "float",
    "bool",
    "enumerate",
    "zip",
    "range",
    "map",
    "filter",
    "sum",
    "max",
    "min",
    "round",
    "sorted",
    "reversed",
    "all",
    "any",
    "isinstance",

    # String

    "lower",
    "upper",
    "strip",
    "split",
    "join",
    "replace",
    "startswith",
    "endswith",
    "capitalize",
    "title",

    # Containers

    "append",
    "extend",
    "insert",
    "remove",
    "pop",
    "clear",
    "copy",
    "sort",

    # Django ORM

    "get",
    "filter",
    "exclude",
    "count",
    "exists",
    "first",
    "last",
    "all",
    "save",
    "delete",
    "create",
    "update",
    "aggregate",
    "annotate",
    "values",
    "values_list",
    "select_related",
    "prefetch_related",
    "order_by",
    "distinct",

    # Django

    "JsonResponse",
    "HttpResponse",
    "render",
    "redirect",

    # Utils

    "loads",
    "dumps",
    "open",
    "read",
    "write",
    "close",
    "BytesIO",

}
PARTICIPANT_MAP = {

    # ----------------------
    # Frontend
    # ----------------------

    "login": "Frontend",
    "logout": "Frontend",
    "register": "Frontend",
    "cart": "Frontend",
    "wishlist": "Frontend",

    # ----------------------
    # Backend APIs
    # ----------------------

    "ai_design": "Backend",
    "multilingual_search": "Backend",
    "chatbot": "Backend",

    # ----------------------
    # AI
    # ----------------------

    "analyze_image_with_gemini": "Gemini",

    "get_chatbot_reply": "LLM",

    "translate_to_english": "Translator",

    "query_huggingface": "HuggingFace",

    "query_huggingface_text": "HuggingFace",

    # ----------------------
    # Search
    # ----------------------

    "search_products": "Database",

    "serialize_products": "Database",

    "build_search_query": "Database",

    "filter_by_placement": "Database",

    # ----------------------
    # Payment
    # ----------------------

    "stripe": "Stripe",

    # ----------------------
    # Email
    # ----------------------

    "send_mail": "Email",

    # ----------------------
    # Authentication
    # ----------------------

    "authenticate": "Authentication",

    "login_required": "Authentication",

}

ACTION_MAP = {

    # ---------- AI ----------

    "analyze_image_with_gemini": "Analyze room image",
    "get_chatbot_reply": "Generate response",
    "translate_to_english": "Translate query",

    # ---------- Search ----------

    "search_products": "Search products",
    "serialize_products": "Serialize products",
    "build_search_query": "Build search query",
    "filter_by_placement": "Filter products",

    # ---------- Payment ----------

    "create_checkout_session": "Create payment",
    "verify_payment": "Verify payment",

    # ---------- Authentication ----------

    "login": "Login",
    "logout": "Logout",
    "register": "Register",

    # ---------- Email ----------

    "send_mail": "Send email"

}



def participant(name):

    if name in PARTICIPANT_MAP:

        return PARTICIPANT_MAP[name]

    return None

def interaction_action(function):

    if function in ACTION_MAP:
        return ACTION_MAP[function]

    return "Request"

def extract_calls(repository):

    repo = REPOSITORY_DIR / repository

    interactions = []

    for root, _, files in os.walk(repo):

        if any(x in root for x in IGNORE):
            continue

        for file in files:

            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)

            try:

                with open(path, encoding="utf-8") as f:

                    tree = ast.parse(f.read())

            except Exception:
                continue

            for node in tree.body:

                if isinstance(node, ast.FunctionDef):

                    caller = node.name

                    for child in ast.walk(node):

                        if isinstance(child, ast.Call):

                            if isinstance(child.func, ast.Attribute):

                                callee = child.func.attr

                            elif isinstance(child.func, ast.Name):

                                callee = child.func.id

                            else:
                                continue

                            if callee in IGNORE_FUNCTIONS:
                                continue

                            if callee.startswith("_"):
                                continue

                            if caller == callee:
                                continue

                            interactions.append(
                                (
                                    caller,
                                    callee
                                )
                            )
    filtered = []

    seen = set()

    for caller, callee in interactions:

        key = (
            caller,
            callee
        )

        if key in seen:
            continue

        seen.add(key)

        filtered.append(
            (
                caller,
                callee
            )
        )

    return filtered
   

FEATURE_MAP = {

    "login": [
        "login",
        "authenticate",
        "jwt",
        "signin",
        "logout"
    ],

    "search": [
        "search",
        "product",
        "multilingual",
        "translate"
    ],

    "design": [
        "design",
        "gemini",
        "image",
        "ai_design",
        "analyze"
    ],

    "cart": [
        "cart",
        "wishlist"
    ],

    "order": [
        "order",
        "checkout",
        "payment",
        "stripe"
    ],

    "review": [
        "review",
        "rating"
    ]

}
def generate_sequence(repository, question):

    query = question.lower()

    interactions = extract_calls(repository)

    selected = []

    for feature, keywords in FEATURE_MAP.items():

        if any(word in query for word in keywords):
            selected = keywords
            break

    participants = set()
    sequence = []
    added = set()

    # ----------------------------
    # First Pass
    # ----------------------------

    for caller_function, callee_function in interactions:

        if selected:

            text = (
                caller_function + " " + callee_function
            ).lower()

            if not any(word in text for word in selected):
                continue

        caller = participant(caller_function)
        callee = participant(callee_function)

        if caller is None or callee is None:
            continue

        participants.add(caller)
        participants.add(callee)

        key = (
            caller,
            callee,
            callee_function
        )

        if key in added:
            continue

        added.add(key)

        action = interaction_action(callee_function)

        sequence.append(
            (
                caller.replace("-", "_"),
                callee.replace("-", "_"),
                action
            )
        )

    # ----------------------------
    # Build Mermaid
    # ----------------------------

    lines = [
        "sequenceDiagram",
        "actor User"
    ]

    for p in sorted(participants):

        lines.append(
            f"participant {p}"
        )

    lines.append("")

    # User starts only if Backend exists

    if "Backend" in participants:

        lines.append(
            "User->>Backend: Request"
        )

    # Add interactions

    for caller, callee, action in sequence:

        lines.append(
            f"{caller}->>{callee}: {action}"
        )

    # Backend responds

    if "Backend" in participants:

        lines.append(
            "Backend-->>User: Response"
        )

    return "\n".join(lines) 