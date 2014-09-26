def mapping(f):
    """Create a transducer that maps a callable over the input values.

    For example, this maps `x * 2` over a range:

    >>> from functools import reduce
    >>> import operator
    >>> tdx = mapping(lambda x: x * 2)
    >>> x = reduce(tdx(operator.add), range(10), 0)
    >>> y = sum(x * 2 for x in range(10))
    >>> assert x == y
    """
    def transducer(reducer):
        def new_reducer(result, new_value):
            return reducer(result, f(new_value))
        return new_reducer
    return transducer


def filtering(pred):
    """Create a transducer that filters input values.

    >>> from functools import reduce
    >>> import operator
    >>> tdx = filtering(lambda x: x < 5)
    >>> x = reduce(tdx(operator.add), range(10), 0)
    >>> y = sum(x for x in range(10) if x < 5)
    >>> assert x == y
    """
    def transducer(reducer):
        def new_reducer(result, new_value):
            if pred(new_value):
                return reducer(result, new_value)
            else:
                return result
        return new_reducer
    return transducer


class _Taking:
    """Core implementation of the `taking` transducer.
    """
    def __init__(self, n, reducer):
        self.n = n
        self.count = 0
        self.reducer = reducer

    def __call__(self, result, new_value):
        if self.count < self.n:
            self.count += 1
            return self.reducer(result, new_value)
        return result


def taking(n):
    """Create a transducer that stop processing input after a specified
    number of values.

    Note that each reducer produced by `taking` transducers is
    independent. That is, you can produce multiple reducers from the
    same `taking` transducer, and each reducer will take the same,
    full count of items.

    >>> from functools import reduce
    >>> import operator
    >>> tdx = taking(5)
    >>> x = reduce(tdx(operator.add), range(100), 0)
    >>> y = sum(range(5))
    >>> assert x == y

    """
    def transducer(reducer):
        return _Taking(n, reducer)
    return transducer
