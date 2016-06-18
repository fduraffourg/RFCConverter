#!/bin/env python

import enum
import re

class BlockType(enum.Enum):
    unknown = 1
    text = 2
    header = 3
    quote = 4
    page_footer = 5
    page_header = 6


class Block(object):
    """ Represent a block of text separated by at least one blank line
    """
    def __init__(self, lines, firstLineNum):
        self.lines = lines
        self.firstLineNum = firstLineNum
        self.type = BlockType.unknown

    def __repr__(self):
        return "<Block type=%s>" % self.type


def cut_blocks(lines):
    list = []
    accumulator = None
    firstLineNum = 0

    for linenum, line in enumerate(lines):
        if line.strip() == "":
            # We found a blank line
            if accumulator is not None:
                list.append(Block(accumulator, firstLineNum))
                accumulator = None
            continue

        if accumulator is None:
            accumulator = [line]
            firstLineNum = linenum
        else:
            accumulator.append(line)

    return list


def search_and_mark_page_marks(blocks):
    """ We know that page headers are all identical and page footers are just
    above page headers
    """

    # First, search for a block with only one line, that is repeated all over
    # the document
    best_count = 0
    best_match = ""
    for item, model in enumerate(blocks):
        count = 0
        if len(model.lines) != 1:
            continue
        line = model.lines[0]
        if line == best_match:
            continue

        for block in blocks[item+1:]:
            if len(block.lines) != 1:
                continue
            if line == block.lines[0]:
                count += 1

        if count > best_count:
            best_count = count
            best_match = line

    # Now mark them
    prev = None
    for block in blocks:
        if len(block.lines) == 1 and block.lines[0] == best_match:
            block.type = BlockType.page_header
            if prev is not None:
                prev.type = BlockType.page_footer
        prev = block

    # The last block is a page footer
    prev.type = BlockType.page_footer


def guess_block_type(block):
    if len(block.lines) == 1:
        # Check if it matches a header
        #if header_re.match(block.lines[0]):
        if block.lines[0][0] != " ":
            return BlockType.header

    # Count the number of letters and other characters
    letters = 0
    others = 0
    for c in "".join(block.lines):
        if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            letters += 1
        else:
            others += 1

    if letters > others:
        return BlockType.text
    else:
        return BlockType.quote


def analyse_header(block):
    assert(block.type == BlockType.header)

    line = block.lines[0]
    cut = 0
    while True:
        if line[cut] in "0123456789.":
            cut += 1
        else:
            break

    if cut > 0:
        # This is a numbered title
        number = line[:cut]
        items = number.strip(".").split(".")
        level = len(items)
        block.header_numbered = True
        block.header_level = level
    else:
        block.header_numbered = False
        # By default, all unnumbered header are level 1
        block.header_level = 1

    title = line[cut:].strip()
    block.header_title = title


def analyse_blocks(blocks):
    search_and_mark_page_marks(blocks)
    for block in blocks:
        if block.type == BlockType.unknown:
            type = guess_block_type(block)
            block.type = type
            if type == BlockType.header:
                analyse_header(block)




if __name__ == '__main__':
    with open("/home/florian/repos/rfcconverter/rfc6265.txt") as fo:
        blocks = cut_blocks(fo)
        analyse_blocks(blocks)

    print(blocks)
