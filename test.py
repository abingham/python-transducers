import doctest
from functools import reduce
import itertools
import operator
import unittest

import transducers as tdc


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(tdc))
    return tests


def append(l, item):
    l.append(item)
    return l

class Tests(unittest.TestCase):

    def test_compose_mapping_and_filter(self):
        tdx = tdc.compose(
            tdc.mapping(lambda x: x * 2),
            tdc.filtering(lambda x: x < 5))

        x = reduce(tdx(operator.mul),
                   range(1, 10), 1)

        self.assertEqual(
            x,
            reduce(operator.mul,
                   (i * 2 for i in range(1, 10) if i < 5),
                   1))

    def test_compose_three_transducers(self):
        tdx = tdc.compose(
            tdc.filtering(lambda x: x % 2 == 0),
            tdc.mapping(lambda x: x * x),
            tdc.mapping(lambda x: x * 2))

        x = reduce(tdx(operator.add),
                   range(100), 0)

        self.assertEqual(
            x,
            sum(filter(lambda x: x % 2 == 0,
                       (x * x
                        for x in (y * 2
                                  for y in range(100))))))

    def test_reuse_single_taking_instance(self):
        take_5 = tdc.taking(5)
        tdx = tdc.compose(
            take_5,
            tdc.mapping(lambda x: x * 2),
            take_5)
        x = reduce(tdx(append), range(100), [])
        y = itertools.islice(
            (x * 2 for x in itertools.islice(range(100), 5)), 5)
        self.assertEqual(x, list(y))




def test():
    unittest.main(exit=False)

if __name__ == '__main__':
    test()
