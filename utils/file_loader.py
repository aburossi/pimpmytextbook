# file_loader.py
def load_textbook(path="inputs/chapter_01.txt"):
    with open(path) as f:
        return f.read()

def load_user_content(path="inputs/user_input.txt"):
    with open(path) as f:
        return f.read()

def load_didactic_guidelines(path="inputs/didactic_guidelines.md"):
    with open(path, encoding="utf-8") as f:
        return f.read()

