import functools
import itertools

from transducers import coroutines


class _ResultHolder:
    """A simple 'box' to hold the final result of a pipeline of
    coroutines.
    """
    def __init__(self, init=None):
        self.value = init


@coroutines.coroutine
def _reduction_target(reducer, rh):
    "The 'tail' of the coroutine transformation pipeline."
    while True:
        new_value = (yield)
        rh.value = reducer(rh.value, new_value)


def _make_transducer_factory(make_coroutine):
    """Convert coroutine factories into transducer factories.

    Given a callable that returns a coroutine, this returns a callable
    that produces transducers that perform their transformations using
    the generated coroutines.. `make_coroutine` may accept any number
    of arguments and keywords; the callabled returned from this
    function will accept those same arguments and pass them along to
    `make_coroutine`.

    This is primarily an implementation detail that allows us to
    define general-purpose coroutines and conveniently convert those
    into transducers. You normally won't need to use this directly.

    If you decide to use it, though, here's how it works:

    >>> import operator
    >>> m = _make_transducer_factory(coroutines.mapping)
    >>> transducer = m(lambda x: x * 2)
    >>> reducer = transducer(operator.add)
    >>> x = reduce(reducer, range(10), 0)
    >>> assert x == sum(x * 2 for x in range(10))

    """
    def make_transducer(*args, **kwargs):
        def transducer(reducer):
            rh = _ResultHolder()  # This holds the final transduction result.

            # The coroutine transformation pipeline, ending in
            # `reduction_target`.
            pipeline = make_coroutine(*args, **kwargs)(
                _reduction_target(reducer, rh))

            def new_reducer(result, new_value):
                """A reducer that uses a coroutine pipeline to transform its input
                before reduction.
                """

                rh.value = result
                try:
                    pipeline.send(new_value)
                except coroutines.StopConsumption:
                    raise StopTransduction(rh.value)

                return rh.value

            return new_reducer
        return transducer
    return make_transducer


class StopTransduction(Exception):
    """Thrown to indicate that reduction should stop.

    This allows reducers to terminate consumption of the input
    sequence early. This is useful e.g. for creating reducers which
    only process a limited number of input elements.

    The final value of the reduction should be passed as the first
    argument to the `StopTransduction` initializer.
    """

    @property
    def value(self):
        """The result of the reduction.
        """
        return self.args[0]


mapping = _make_transducer_factory(coroutines.mapping)
filtering = _make_transducer_factory(coroutines.filtering)
mapcatting = _make_transducer_factory(coroutines.mapcatting)
taking = _make_transducer_factory(coroutines.taking)
taking_while = _make_transducer_factory(coroutines.taking_while)

_REDUCE_NO_INITIAL = object()


def reduce(func, seq, initial=_REDUCE_NO_INITIAL):
    """A drop-in replacement for `functools.reduce` which honors the
    transduction protocol for stopping reduction early when
    `StopTransduction` is received.
    """
    try:
        if initial is _REDUCE_NO_INITIAL:
            return functools.reduce(func, seq)
        else:
            return functools.reduce(func, seq, initial)
    except StopTransduction as e:
        return e.value


def conj(l, x):
    """Append `x` to the list `l` and return `l`.

    This is an analogue to clojure's `conj`.
    """
    l.append(x)
    return l


def map(func, seq):
    return reduce(mapping(func)(conj), seq, [])


def filter(pred, seq):
    return reduce(filtering(pred)(conj), seq, [])


def mapcat(func, seq):
    return reduce(mapcatting(func)(conj), seq, [])
