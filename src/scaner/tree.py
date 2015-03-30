import os
import datetime


def build_tree(watched_dir):
    tree = []
    for root, dirs, files in os.walk(watched_dir, topdown=True):
        for folder in dirs:
            pathname = os.path.join(root, folder)
            object1 = {"path": root, "pathname": pathname, "is_dir": True, "date": datetime.datetime.fromtimestamp(
                os.path.getmtime(pathname))}
            tree.append(object1)
        for document in files:
            pathname = os.path.join(root, document)
            object1 = {"path": root, "pathname": pathname, "is_dir": False, "date": datetime.datetime.fromtimestamp(
                os.path.getmtime(pathname))}
            tree.append(object1)
    return tree