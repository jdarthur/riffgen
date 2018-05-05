"""
author: JD Arthur
date: 5 May 2018

Test script for pyhyphen library.

This grabs a random line from one of Shakespeare's sonnets
and attempts to split it into syllables.
"""

import random
from hyphen import Hyphenator

def sonnet_line(sonnlist):
    """
    get a random line from a sonnet
    """

    random_line = ""
    index = 0
    while(random_line == ""
          or "SONNET" in random_line
          or "(    )" in random_line):
        index = random.randint(0, len(sonnlist) - 1)
        random_line = sonnlist[index].strip()
    sonn_num, line_num = get_sonnet_and_line_number(sonnlist, index)
    values = {
        "line" : random_line,
        "sonnet_number" : sonn_num,
        "line_number" : line_num
    }
    return values

def get_sonnet_and_line_number(sonnlist, line_index):
    """
    parse sonnlist to get the sonnet number and line within that sonnet
    """
    back_count = 0
    backwards_line = ""
    found = False
    while not found:
        backwards_line = sonnlist[line_index - back_count]
        if "SONNET" in backwards_line:
            found = True
            return backwards_line.split()[1], back_count - 1
        else:
            back_count += 1

def syllablize(line):
    """
    take a line and split it into a list of syllables
    """
    hyph_en = Hyphenator('en_US')
    syll_list = []
    #get words separately + count hyphenated words as 2 words
    words = line.replace("-", " ").split()
    for word in words:
        #remove common punctuation
        word = word.replace(",", "").replace(":", "").replace(";", "")
        syllables = hyph_en.syllables(word)
        if not syllables:
            #pyhyphen sometimes returns 1 syllable words back to you,
            #but sometimes return an empty list... don't know why
            syll_list.append(word)
        for syll in syllables:
            syll_list.append(syll)
    return syll_list

def syllablerun():
    """
    entry point to this module. This calls everything else.
    """
    filename = "sonnets.txt"
    sonnlist = None
    with open(filename, "r") as sonnets:
        sonnlist = sonnets.readlines()

    vals = sonnet_line(sonnlist)
    vals["syllables"] = syllablize(vals["line"])
    return vals

"""
import pprint
pprint.pprint(syllablerun())
"""