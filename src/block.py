from enum import Enum



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.strip().splitlines()

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if len(lines) == 1 and lines[0].startswith("#"):
        if lines[0].lstrip().startswith(tuple(f"{'#' * i} " for i in range(1, 7))):
            return BlockType.HEADING

    if all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.strip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(
        line.strip().startswith(f"{i + 1}. ")
        for i, line in enumerate(lines)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
