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


class StopConsumption(Exception):
    """Thrown by coroutines when input processing should stop.
    """
    pass


def consume(pipeline, seq):
    """Pass consecutive elements from `seq` into `pipeline` until either
    `seq` is exhausted or `pipeline.send` raises `StopConsumption`.

    """
    try:
        for value in seq:
            pipeline.send(value)
    except StopConsumption:
        pass


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
    >>> consume(m(append(result)), range(10))
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
    >>> consume(f(append(result)), range(10))
    >>> assert result == [x for x in range(10) if x % 2 == 0]

    """
    @coroutine
    def gen(target):
        while True:
            x = yield
            if pred(x):
                target.send(x)
    return gen


def mapcatting(f):
    """Create a coroutine that mapcats sequences of sequences.


    >>> result = []
    >>> m = mapcatting(lambda x: reversed(x))
    >>> consume(m(append(result)),
    ...     [(3, 2, 1, 0), (6, 5, 4), (9, 8, 7)])
     >>> assert result == list(range(10))
    """
    @coroutine
    def gen(target):
        while True:
            xs = yield
            for x in f(xs):
                target.send(x)

    return gen

def taking(n):
    """Create a coroutine that only passes along the first `n` items it
    receives.

    This raises a `ValueError` if `n <= 0`.

    >>> result = []
    >>> consume(taking(5)(append(result)), range(1000))
    >>> assert result == list(range(5))

    """
    if n <= 0:
        raise ValueError('taking() requires a positive value.')

    @coroutine
    def gen(target):
        for _ in range(n):
            x = (yield)
            target.send(x)

        raise StopConsumption()

    return gen


def taking_while(pred):
    """Create a coroutine that only consumes input while a predicate
    returns True for input values.

    >>> result = []
    >>> consume(taking_while(lambda x: x < 5)(append(result)), range(1000))
    >>> assert result == list(range(5))
    """
    @coroutine
    def gen(target):
        while True:
            x = (yield)
            if pred(x):
                target.send(x)
            else:
                raise StopConsumption()

    return gen
