import unittest
from statements import *

class TestStatements(unittest.TestCase):

    def test_get_all(self):
        l = Lexicon()
        l.add("like","T")
        l.add("John","P")
        l.add("Mary","P")
        l.add("like","T")

        self.assertEqual(l.getAll("P"), ["John", "Mary"])

    def test_fact_base(self):
        fb = FactBase()
        fb.addUnary("duck","John")
        fb.addBinary("love","John","Mary")

        self.assertEqual(fb.queryUnary("duck","John"), True)
        self.assertEqual(fb.queryBinary("love","Mary","John"), False)
        self.assertEqual(fb.queryBinary("love","Mary","Johnn"), False)

    def test_verb_stem(self):

        correct_words_test = ["eats", "tells", "shows", "pays", "buys", "flies", "unifies",
                      "dies", "goes", "fizzes", "dresses", "boxes", "loses", "analyzes",
                      "has", "Has", "likes", "bathes"]
        incorrect_words_test = ["flys", "unifys", "cats"]

        correct_words_test_res = list()
        incorrect_words_test_res = list()

        for word in correct_words_test:
            correct_words_test_res.append(verb_stem(word))
        for word in incorrect_words_test:
            incorrect_words_test_res.append(verb_stem(word))

        self.assertItemsEqual(correct_words_test_res, ['eat', 'tell', 'show', 'pay', 'buy', 'fly', 'unify', 'die', 'go',
                                              '', 'dress', 'box', 'lose', 'analyze', 'have', 'Have', 'like', 'bathe'])
        self.assertItemsEqual(incorrect_words_test_res, ['', '', ''])


