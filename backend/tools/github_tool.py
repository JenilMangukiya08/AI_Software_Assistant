from pathlib import Path
from git import Repo

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORY_DIR = BASE_DIR / "repositories"


def open_repo(repository):

    path = REPOSITORY_DIR / repository

    return Repo(path)

def get_recent_commits(repository, limit=10):

    repo = open_repo(repository)

    commits = []

    for commit in repo.iter_commits(max_count=limit):

        commits.append({

            "hash": commit.hexsha[:8],

            "author": commit.author.name,

            "date": str(commit.committed_datetime),

            "message": commit.message.strip()

        })

    return commits


def get_branches(repository):

    repo = open_repo(repository)

    return [branch.name for branch in repo.branches]


def get_contributors(repository):

    repo = open_repo(repository)

    authors = {}

    for commit in repo.iter_commits():

        name = commit.author.name

        authors[name] = authors.get(name, 0) + 1

    return authors

def latest_changed_files(repository):

    repo = open_repo(repository)

    commit = next(repo.iter_commits())

    return list(commit.stats.files.keys())