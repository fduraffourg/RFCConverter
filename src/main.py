#!/bin/env python

import argparse
import parser
import writer.html


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--input", required=True, type=str, help="Input file")
    argparser.add_argument("-o", "--output", required=True, type=str, help="Output file")

    args = argparser.parse_args()

    with open(args.input) as fo:
        blocks = parser.cut_blocks(fo)
        parser.analyse_blocks(blocks)

    with open(args.output, "w") as fo:
        writer.html.write(fo, blocks)
