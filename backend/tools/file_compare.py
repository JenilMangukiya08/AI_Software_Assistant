from pathlib import Path
from tools.file_reader import read_file
import difflib


def compare_files(repository, file1, file2):

    content1 = read_file(repository, file1)
    content2 = read_file(repository, file2)

    if content1 is None:
        return None

    if content2 is None:
        return None

    diff = difflib.unified_diff(

        content1.splitlines(),
        content2.splitlines(),

        fromfile=file1,
        tofile=file2,

        lineterm=""
    )

    return "\n".join(diff)