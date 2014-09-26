import doctest
import itertools
import unittest

from transducers.compose import compose
import transducers.coroutines as crt


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(crt))
    return tests


class Tests(unittest.TestCase):

    def test_compose_mapping_and_filter(self):
        composed = compose(
            crt.mapping(lambda x: x * 2),
            crt.filtering(lambda x: x < 5))

        result = []
        f = composed(crt.append(result))
        for i in range(10):
            f.send(i)
        self.assertListEqual(
            result,
            [x * 2 for x in range(10) if x < 5])

    def test_compose_three_coroutines(self):
        composed = compose(
            crt.filtering(lambda x: x % 2 == 0),
            crt.mapping(lambda x: x * x),
            crt.mapping(lambda x: x * 2))

        result = []
        f = composed(crt.append(result))

        for i in range(100):
            f.send(i)

        self.assertListEqual(
            result,
            list(filter(
                lambda z: z % 2 == 0,
                (x * x for x in
                 (y * 2 for y in
                  range(100))))))

    def test_reuse_single_taking_instance(self):
        take_5 = crt.taking(5)
        composed = compose(
            take_5,
            crt.mapping(lambda x: x * 2),
            take_5)

        result = []
        f = composed(crt.append(result))
        for i in range(1000):
            f.send(i)

        expected = list(itertools.islice(
            (x * 2 for x in itertools.islice(range(1000), 5)), 5))

        self.assertListEqual(
            result,
            expected)
