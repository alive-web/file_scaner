import re


def is_hidden(path):
    hidden_path = ["/\.", "~$", "/tmp"]
    for hidden in hidden_path:
        if re.search(hidden, path):
            return True
    return False