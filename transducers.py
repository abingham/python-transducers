# ;;transducer signature
# (whatever, input -> whatever) -> (whatever, input -> whatever)
#

# ;;look Ma, no collection!
# (map f)

# returns a 'mapping' transducer. filter et al get similar support.

# You can build a 'stack' of transducers using ordinary function composition (comp):

# This arity will return a transducer that represents the same logic,
# independent of lazy sequence processing.

# (def xform (comp (map inc) (filter even?)))

# (defn mapping [f]
#    (fn [f1]
#      (fn [result input]
#        (f1 result (f input)))))

#  (defn filtering [pred]
#    (fn [f1]
#      (fn [result input]
#        (if (pred input)
#          (f1 result input)
#          result))))

#  (defn mapcatting [f]
#    (fn [f1]
#      (fn [result input]
#        (reduce f1 result (f input)))))

# (reduce + 0 (map inc [1 2 3 4]))
# ;;becomes
# (reduce ((mapping inc) +) 0 [1 2 3 4])

from functools import reduce
import operator
import unittest


def compose(*transducers):
    def transducer(reducer):
        return reduce(lambda r, n: n(r),
                      transducers,
                      reducer)
    return transducer


def mapping(f):
    def transducer(reducer):
        def new_reducer(result, new_value):
            return reducer(result, f(new_value))
        return new_reducer
    return transducer


def filtering(pred):
    def transducer(reducer):
        def new_reducer(result, new_value):
            if pred(new_value):
                return reducer(result, new_value)
            else:
                return result
        return new_reducer
    return transducer


class Tests(unittest.TestCase):
    def test_mapping(self):
        tdx = mapping(lambda x: x * 2)
        x = reduce(tdx(operator.add),
                   range(10), 0)
        self.assertEqual(
            x,
            sum(x * 2 for x in range(10)))

    def test_filtering(self):
        tdx = filtering(lambda x: x < 5)
        x = reduce(tdx(operator.add),
                   range(10), 0)
        self.assertEqual(
            x,
            sum(x for x in range(10) if x < 5))

    def test_compose_mapping_and_filter(self):
        tdx = compose(
            mapping(lambda x: x * 2),
            filtering(lambda x: x < 5))

        x = reduce(tdx(operator.mul),
                   range(1, 10), 1)

        self.assertEqual(
            x,
            reduce(operator.mul,
                   (i * 2 for i in range(1, 10) if i < 5),
                   1))

    def test_compose_three_transducers(self):
        tdx = compose(
            filtering(lambda x: x % 2 == 0),
            mapping(lambda x: x * x),
            mapping(lambda x: x * 2))

        x = reduce(tdx(operator.add),
                   range(100), 0)

        self.assertEqual(
            x,
            sum(filter(lambda x: x % 2 == 0,
                       (x * x
                        for x in (y * 2
                                  for y in range(100))))))


unittest.main(exit=False)
