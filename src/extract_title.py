def extract_title(markdown):
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.startswith("# "):
            return block.splitlines()[0][2:].strip()
    raise ValueError("No title found")