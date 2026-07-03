from tools.code_search import search_code

results = search_code(
    "AI_ROUTE_PLANNER",
    "weather_node"
)

for item in results:

    print(item)