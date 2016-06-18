#!/bin/env python

import parser


if __name__ == '__main__':
    with open("/home/florian/repos/rfcconverter/rfc6265.txt") as fo:
        blocks = parser.cut_blocks(fo)
        parser.analyse_blocks(blocks)

    print(blocks)
