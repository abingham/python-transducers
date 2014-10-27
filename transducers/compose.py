from functools import reduce
from itertools import chain


def compose(c1, *composables):
    """Compose one or more composables into a single, composite
    composable.

    This works e.g. for transducers and coroutines.

    For example, this composes a `mapping` and a `filtering` in a
    mapping-of-a-filtering:

    >>> import operator
    >>> from transducers.transducers import filtering, mapping
    >>> tdx = compose(
    ...     filtering(lambda x: x < 5),
    ...     mapping(lambda x: x * 2))
    ...
    >>> x = reduce(tdx(operator.mul),
    ...            range(1, 10), 1)
    ...
    >>> seq = (i * 2 for i in range(1, 10) if i < 5)
    >>> y = reduce(operator.mul, seq, 1)
    >>> assert x == y

    """
    def composite(terminus):
        return reduce(lambda r, n: n(r),
                      chain(reversed(composables), [c1]),
                      terminus)
    return composite
