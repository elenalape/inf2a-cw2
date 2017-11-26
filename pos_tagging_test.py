import unittest
from pos_tagging import *
from statements import Lexicon


class TestPosTagging(unittest.TestCase):
    def test_unchanging_plurals(self):

        self.assertItemsEqual(unchanging_plurals(), ['police', 'fish', 'deer', 'series', 'sheep', 'buffalo', 'multimedia', 'bison', 'cannabis',
                                                     'dna', 'headquarters', 'salmon', 'swine', 'trout', 'moose', 'marijuana', 'species'])

    def test_noun_stem(self):

        self.assertEqual(noun_stem("sheep"), "sheep")
        self.assertEqual(noun_stem("women"), "woman")
        self.assertEqual(noun_stem("men"), "man")
        self.assertEqual(noun_stem("flies"), "fly")
        self.assertEqual(noun_stem("cats"), "cat")
        self.assertEqual(noun_stem("flys"), "")
        self.assertEqual(noun_stem("likes"), "like")

    def test_tag_word(self):

        l = Lexicon()
        l.add("John","P")
        l.add("orange","N")
        l.add("orange","A")
        l.add("box","N")
        l.add("cat","N")
        l.add("fish","N")
        l.add("fish","T")
        l.add("fish","I")
        l.add("fish","N")
        l.add('like','T')
        l.add('like','N')
        l.add('like','I')
        l.add('police','N')
        l.add('animal','N')
        l.add('fly','N')
        l.add('fly','T')

        self.assertItemsEqual(tag_word(l, "John"), ["P"])
        self.assertItemsEqual(tag_word(l, "orange"), ["Ns", "A"])
        self.assertItemsEqual(tag_word(l, "fish"),  ["Ns", "Np", "Ip", "Tp"])
        self.assertItemsEqual(tag_word(l, "a"), ["AR"])
        self.assertItemsEqual(tag_word(l, "zxghqw"), [])
        self.assertItemsEqual(tag_word(l, "likes"), ["Is","Ts","Np"])
        self.assertItemsEqual(tag_word(l, "like"), ["Tp","Ns","Ip"])
        self.assertItemsEqual(tag_word(l, "police"), ["Np","Ns"])
        self.assertItemsEqual(tag_word(l, "animals"), ["Np"])
        self.assertItemsEqual(tag_word(l, "flies"), ["Np","Ts"])
