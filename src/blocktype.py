from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

def block_to_block_type(block):
    if (
            block.startswith("# ") or
            block.startswith("## ") or
            block.startswith("### ") or
            block.startswith("#### ") or
            block.startswith("##### ") or
            block.startswith("###### ")
    ):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.splitlines()
    count_quote = 0
    count_unordered_list = 0
    count_ordered_list = 0
    for i in range(len(lines)):
        if lines[i].startswith(">"):
            count_quote += 1
        elif lines[i].startswith("- "):
            count_unordered_list += 1
        elif lines[i].startswith(f"{i + 1}. "):
            count_ordered_list += 1
    if len(lines) == count_quote:
        return BlockType.QUOTE
    if len(lines) == count_unordered_list:
        return BlockType.UNORDERED_LIST
    if len(lines) == count_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
