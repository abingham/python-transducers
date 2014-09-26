from functools import reduce
from itertools import chain, islice


def coroutine(func):
    # From Dave Beazley: http://www.dabeaz.com/coroutines/Coroutines.pdf
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start


def map_(f):
    @coroutine
    def gen(target):
        while True:
            x = yield
            target.send(f(x))
    return gen


def filter_(pred):
    @coroutine
    def gen(target):
        while True:
            x = yield
            if pred(x):
                target.send(x)
    return gen


def compose(f1, *funcs):
    def gen(sink):
        return reduce(
            lambda r, n: n(r),
            chain([f1], funcs),
            sink)
    return gen


@coroutine
def append_(l):
    while True:
        x = yield
        l.append(x)

gen = compose(
    map_(lambda x: x * 2),
    filter_(lambda x: x % 2 == 0))

result = []
a = append_(result)

f = gen(a)
for i in range(10):
    f.send(i)

print(result)
