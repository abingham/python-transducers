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
        return lambda r, n: reducer(r, f(n))
    return transducer


def filtering(pred):
    def transducer(reducer):
        return lambda r, n: reducer(r, n) if pred(n) else r
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

    def test_compose(self):
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

unittest.main(exit=False)
