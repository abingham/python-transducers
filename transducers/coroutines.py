from functools import reduce
from itertools import chain


def coroutine(func):
    """A decorator for simplifying coroutines.

    Really all this does is initiate the coroutine and make the
    necessary first `next` call on it.

    For example:

    >>> @coroutine
    ... def printer():
    ...     while True:
    ...         print((yield))
    >>> p = printer()
    >>> for i in range(3):
    ...     p.send(i)
    0
    1
    2

    This was taken from Dave Beazley:
    http://www.dabeaz.com/coroutines/Coroutines.pdf
    """
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start


@coroutine
def append(l):
    """A coroutine that appends items to a list.
    """
    while True:
        x = yield
        l.append(x)


def mapping(f):
    """Create a coroutine that maps a callable over the input
    values.

    For example, this maps `x * 2` over a range:

    >>> result = []
    >>> m = mapping(lambda x: x * 2)
    >>> c = m(append(result))
    >>> for i in range(10):
    ...     c.send(i)
    ...
    >>> assert result == [x * 2 for x in range(10)]

    """
    @coroutine
    def gen(target):
        while True:
            x = yield
            target.send(f(x))
    return gen


def filtering(pred):
    """Create a coroutine that filters input values.

    For example, this filters out odd values:

    >>> result = []
    >>> f = filtering(lambda x: x % 2 == 0)
    >>> c = f(append(result))
    >>> for i in range(10):
    ...     c.send(i)
    ...
    >>> assert result == [x for x in range(10) if x % 2 == 0]

    """
    @coroutine
    def gen(target):
        while True:
            x = yield
            if pred(x):
                target.send(x)
    return gen


def taking(n):
    """Create a coroutine that only passes along the first `n` items it
    receives.

    Note that a `taking` simply ignores every item after the first
    `n`. They are still "consumed", but no downstream coroutine will see them.

    >>> result = []
    >>> appender = append(result)
    >>> t = taking(5)
    >>> c = t(append(result))
    >>> for i in range(1000):
    ...    c.send(i)
    >>> assert result == list(range(5))

    """
    @coroutine
    def gen(target):
        count = 0
        while True:
            x = (yield)
            if count < n:
                target.send(x)
                count += 1
    return gen
