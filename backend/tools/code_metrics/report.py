from pathlib import Path

from .analyzer import analyze_repository
from .complexity import analyze_complexity
from .summary import analyze_summary

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def generate_metrics(repository):

    repo = REPOSITORY_DIR / repository

    repository_stats = analyze_repository(repo)

    complexity_stats = analyze_complexity(repo)

    summary_stats = analyze_summary(repo)

    report = {

        "repository": repository_stats,

        "complexity": complexity_stats,

        "summary": summary_stats

    }
    
    health = 10.0

    if repository_stats["comment_lines"] < 50:
        health -= 1

    if summary_stats["tests"] == 0:
        health -= 2

    if complexity_stats["largest_function_lines"] > 80:
        health -= 1

    if complexity_stats["average_function_length"] > 30:
        health -= 1

    if not summary_stats["readme"]:
        health -= 1

    if not summary_stats["requirements"]:
        health -= 1

    report["health_score"] = round(
        max(0, health),
        2
    )

    return report