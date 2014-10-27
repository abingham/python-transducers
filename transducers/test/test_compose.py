import doctest
import itertools
import unittest

import transducers.compose


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(transducers.compose))
    return tests
