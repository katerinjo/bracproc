#!/usr/bin/env python3.7

import os
from pathlib import Path
import pprint
import sys

START_PY = '«'
END_PY = '»'
START_TXT = '‹'
END_TXT = '›'

def parse(raw_text):
    tree = []
    breadcrumbs = [tree]
    left_limit = 0
    textmode = True
    def grab_chunk(down_char, up_char):
        nonlocal left_limit, tree, breadcrumbs
        # find next bracket
        right_limit = left_limit
        while (
                right_limit < len(raw_text)
                and raw_text[right_limit] not in [down_char, up_char]
                ):
            right_limit += 1

        if right_limit < len(raw_text):
            # add current chunk to tree at working node
            breadcrumbs[-1].append(raw_text[left_limit:right_limit])

            # move in the tree
            if raw_text[right_limit] == down_char:
                # go deeper
                breadcrumbs[-1].append([]) # new node
                breadcrumbs.append(breadcrumbs[-1][-1]) # point at it
            else:
                # back out one level
                breadcrumbs.pop()

        # update location
        left_limit = right_limit + 1


    while left_limit < len(raw_text):
        if textmode:
            grab_chunk(START_PY, END_TXT)
        else:
            grab_chunk(START_TXT, END_PY)
        textmode = not textmode

    return tree


if __name__ == '__main__':
    this_file = Path(os.path.realpath(__file__))
    file_dir = this_file.parent
    called_from = Path.cwd()
    in_file = Path(sys.argv[1]).resolve()
    # out_file = Path(sys.argv[2]).resolve()

    with in_file.open() as f:
        raw_text = f.read()

    pprint.pprint(parse(raw_text))


