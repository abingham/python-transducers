import doctest
import itertools
import operator
import unittest

import transducers.transducers as tdc
from transducers.compose import compose


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(tdc))
    return tests


def append(l, item):
    l.append(item)
    return l


class Tests(unittest.TestCase):

    def test_mapping(self):
        tdx = tdc.mapping(lambda x: x * 2)
        x = tdc.reduce(tdx(operator.add), range(10), 0)
        self.assertEqual(x, sum(x * 2 for x in range(10)))

    def test_filtering(self):
        f = tdc.filtering(lambda x: x < 10)
        x = tdc.reduce(f(operator.add), range(100), 0)
        self.assertEqual(x, sum(range(10)))

    def test_mapcatting(self):
        m = tdc.mapcatting(reversed)
        x = tdc.reduce(m(tdc.conj), ((3, 2, 1, 0), (6, 5, 4)), [])
        self.assertListEqual(x, list(range(7)))

    def test_taking(self):
        t = tdc.taking(10)
        x = tdc.reduce(t(operator.add), range(100), 0)
        self.assertEqual(x, sum(range(10)))

    def test_taking_while(self):
        t = tdc.taking_while(lambda x: x < 10)
        x = tdc.reduce(t(operator.add), range(100), 0)
        self.assertEqual(x, sum(range(10)))

    def test_compose_mapping_and_filter(self):
        tdx = compose(
            tdc.filtering(lambda x: x < 5),
            tdc.mapping(lambda x: x * 2))

        x = tdc.reduce(tdx(operator.mul),
                   range(1, 10), 1)

        self.assertEqual(
            x,
            tdc.reduce(operator.mul,
                   (i * 2 for i in range(1, 10) if i < 5),
                   1))

    def test_compose_three_transducers(self):
        tdx = compose(
            tdc.mapping(lambda x: x * 2),
            tdc.mapping(lambda x: x * x),
            tdc.filtering(lambda x: x % 2 == 0))

        x = tdc.reduce(tdx(operator.add),
                   range(100), 0)

        self.assertEqual(
            x,
            sum(filter(lambda x: x % 2 == 0,
                       (x * x
                        for x in (y * 2
                                  for y in range(100))))))

    def test_reuse_single_taking_instance(self):
        take_5 = tdc.taking(5)
        tdx = compose(
            take_5,
            tdc.mapping(lambda x: x * 2),
            take_5)
        x = tdc.reduce(tdx(append), range(100), [])
        y = itertools.islice(
            (x * 2 for x in itertools.islice(range(100), 5)), 5)
        self.assertEqual(x, list(y))

    def test_taking_does_not_consume_all_input(self):
        take_5 = tdc.taking(5)
        input_data = (i for i in range(100))
        tdc.reduce(take_5(operator.add), input_data, 0)
        self.assertEqual(len(list(input_data)), 95)

    def test_taking_while_does_not_consume_all_input(self):
        lt_10 = tdc.taking_while(lambda x: x < 10)
        input_data = (i for i in range(100))
        tdc.reduce(lt_10(operator.add), input_data, 0)
        self.assertEqual(len(list(input_data)), 89)

    def test_map_simple(self):
        result = tdc.map(lambda x: x * 2, range(10))
        self.assertListEqual(
            result,
            [x * 2 for x in range(10)])

    def test_map_empty(self):
        result = tdc.map(lambda x: x * 2, [])
        self.assertListEqual(
            result, [])

    def test_filter_simple(self):
        result = tdc.filter(
            lambda x: x < 5,
            range(10))
        self.assertListEqual(
            result,
            [x for x in range(10) if x < 5])

    def test_mapcat_simple(self):
        result = tdc.mapcat(
            reversed,
            ((3, 2, 1, 0), (6, 5, 4)))

        self.assertListEqual(
            result,
            list(range(7)))
