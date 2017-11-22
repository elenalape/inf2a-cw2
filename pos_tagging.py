# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    nn = []
    nns = []
    lines = ""
    with open("sentences.txt", "r") as f:
        for line in f:
            word_list = line.split(" ")
            temp_list = []

            for word in word_list:
                if tuple(word.split("|"))[1] == "NN":
                    nn.append(tuple(word.split("|"))[0])
                elif tuple(word.split("|"))[1] == "NNS":
                    nns.append(tuple(word.split("|"))[0])

    return list(set(nn).intersection(nns))

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    if s in unchanging_plurals_list:
        return s

    if s.endswith("men"):
        return s[:len(s) - 3] + "man"

    #copied from statements.py omitting verb assertion
    
    if re.match(r"^\w+[^iosxz]es$", s):
        if s[len(s)-1] + s[len(s)-2] != "ch" or s[len(s)-1] + s[len(s)-2] != "sh":
            return s[:len(s) - 1]

    if not s.endswith("zzes") and not s.endswith("sses"):
        if s.endswith("ses") or s.endswith("zes"):
            return s[:len(s) - 1]

    if re.match(r"^\w+(o|x|ch|sh|ss|zz)es$", s):
        return s[:len(s) - 2]
    
    if re.match(r"^[^aeiou]ies$", s):
        return s[:len(s) - 1]

    if re.match(r"^\w\w*[^aeiou]ies$", s):
        return s[:len(s) - 3] + "y"

    if re.match(r"^\w+[aeiou]ys$", s):
        return s[:len(s) - 1]

    if re.match(r"^\w+[^sxyzaeiou]s$", s):
        if not s.endswith("chs") and not s.endswith("shs"):
            return s[:len(s) - 1]

    return ""
    

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    wd_tags = []
    all_forms = [wd, verb_stem(wd), noun_stem(wd)]
    all_tags = ['P', 'A', 'Ns', 'Np', 'Is', 'Ip', 'Ts', 'Tp', 'BEs', 'BEp', 'DOs', 'DOp', 'AR', 'AND', 'WHO', 'WHICH', '?']
    for tag in all_tags:
        for form in all_forms:
            if form in lx.getAll(tag):
                wd_tags.append(tag)

    return list(set(wd_tags))

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
#print unchanging_plurals()
# lex = Lexicon()
# lex.add("John","P")
# lex.add("Mary","P")
# lex.add("Mary","Ns")
# lex.add("like","T")
# print(tag_word(lex, "Mary"))
