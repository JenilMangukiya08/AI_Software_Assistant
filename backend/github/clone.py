import os
import shutil
import stat
from git import Repo

BASE_DIR = "repositories"


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repository(repo_url):

    os.makedirs(BASE_DIR, exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1]

    destination = os.path.join(BASE_DIR, repo_name)

    if os.path.exists(destination):
        shutil.rmtree(destination, onexc=remove_readonly)

    # Clone repository
    repo = Repo.clone_from(repo_url, destination)
    repo.close()

    # Remove .git folder (not needed for RAG)
    git_dir = os.path.join(destination, ".git")

    if os.path.exists(git_dir):
        shutil.rmtree(git_dir, onexc=remove_readonly)

    return destination