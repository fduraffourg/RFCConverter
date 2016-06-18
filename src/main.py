#!/bin/env python

import parser
import writer.html


if __name__ == '__main__':
    with open("/home/florian/repos/rfcconverter/rfc6265.txt") as fo:
        blocks = parser.cut_blocks(fo)
        parser.analyse_blocks(blocks)

    with open("/tmp/out.html", "w") as fo:
        writer.html.write(fo, blocks)
