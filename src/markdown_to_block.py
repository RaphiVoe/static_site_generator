def markdown_to_block(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            new_blocks.append(block)
    return new_blocks