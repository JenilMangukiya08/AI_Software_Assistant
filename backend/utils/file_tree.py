import os


def build_tree(root):

    tree = {}

    for current_path, dirs, files in os.walk(root):

        relative = os.path.relpath(current_path, root)

        current = tree

        if relative != ".":

            for part in relative.split(os.sep):
                current = current.setdefault(part, {})

        for file in files:

            if file.endswith((
                ".py",
                ".md",
                ".json",
                ".txt",
                ".yml",
                ".yaml"
            )):

                current[file] = None

    return tree