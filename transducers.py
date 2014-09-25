from functools import reduce


def compose(*transducers):
    """Compose one or more transducers into a single transducer.

    For example, this composes a mapping and a filtering in a
    mapping-of-a-filtering:

    >>> import operator
    >>> tdx = compose(
    ...     mapping(lambda x: x * 2),
    ...     filtering(lambda x: x < 5))
    ...
    >>> x = reduce(tdx(operator.mul),
    ...            range(1, 10), 1)
    ...
    >>> seq = (i * 2 for i in range(1, 10) if i < 5)
    >>> y = reduce(operator.mul, seq, 1)
    >>> assert x == y
    """
    if not transducers:
        raise ValueError('compose() requires at least one function.')

    def transducer(reducer):
        return reduce(lambda r, t: t(r),
                      transducers,
                      reducer)
    return transducer


def mapping(f):
    """Create a transducer that maps a callable over the input values.

    For example, this maps `x * 2` over a range:

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

    >>> import operator
    >>> tdx = taking(5)
    >>> x = reduce(tdx(operator.add), range(100), 0)
    >>> y = sum(range(5))
    >>> assert x == y

    """
    def transducer(reducer):
        return _Taking(n, reducer)
    return transducer
