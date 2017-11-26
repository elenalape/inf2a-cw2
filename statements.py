# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        self.lx = {}

    def add(self, stem, cat):
        if self.lx.get(cat):
            self.lx[cat] = self.lx[cat] + [stem]
        else:
            self.lx[cat] = [stem]

    def getAll(self, cat):
        if self.lx.has_key(cat):
            return list(set(self.lx[cat]))
        return []

class FactBase:
    """stores unary and binary relational facts"""
    def __init__(self):
        self.unary = {}
        self.binary = {}

    def addUnary(self, pred, e1):
        if pred not in self.unary.keys():
            self.unary[pred] = []
        self.unary[pred].append(e1)

    def addBinary(self, pred, e1, e2):
        if pred not in self.binary.keys():
            self.binary[pred] = []
        self.binary[pred].append((e1, e2))

    def queryUnary(self, pred, e1):
        if pred in self.unary.keys():
            if e1 in self.unary[pred]:
                return True
        return False

    def queryBinary(self, pred, e1, e2):
        if pred in self.binary.keys():
            if (e1, e2) in self.binary[pred]:
                return True
        return False


import re
import nltk
from nltk.corpus import brown

vbz_verbs = []
vb_verbs = []
for word, pos in nltk.corpus.brown.tagged_words():
    if pos == "VBZ":
        vbz_verbs.append(word)
    elif pos == "VB":
        vb_verbs.append(word)

def verb_stem_helper(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    if re.match(r"^\w+[^iosxz]es$", s):
        if s[len(s)-1] + s[len(s)-2] != "ch" or s[len(s)-1] + s[len(s)-2] != "sh":
            return s[:len(s) - 1]

    if s.endswith("zzes") or s.endswith("sses"):
        return s[:len(s) - 2]

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

def verb_stem(s):

    if re.match(r"has", s):
        return "have"

    s_stem = verb_stem_helper(s)
    if s_stem in vb_verbs or s in vbz_verbs:
        return s_stem
    return ''

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.