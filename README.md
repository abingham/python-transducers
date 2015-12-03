[![Build Status](https://travis-ci.org/abingham/python-transducers.png)](https://travis-ci.org/abingham/python-transducers)
[![Code health](https://landscape.io/github/abingham/python-transducers/master/landscape.png)](https://landscape.io/github/abingham/python-transducers)

**NOTE:** This project is going to sleep for the forseeable future. Active development of these ideas will take place [over here](https://github.com/sixty-north/python-transducers).

==================
python-transducers
==================

Transducers for Python.

Transducers are a concept from clojure, or at least that's where I
heard of them first. A *transducer* is a function that takes a
*reducer* (i.e. the kind of function you would pass to
`functools.reduce`) and returns another reducer. Transducers are a
distillation of concepts like mapping and filtering (among other
things) that are easily composable.

Note that this module is largely an exercise is "seeing how it works."
It's not clear if there are any real practical benefits to using
transducers in Python. While they do provide a certain conceptual
clarity and have some pleasing properties, they may be slow, limited
in applicability, and perhaps even non-Pythonic by some measure.

For more information, see
[Transducers are coming](http://blog.cognitect.com/blog/2014/8/6/transducers-are-coming)
and the earlier
[Anatomy of a reducer](http://clojure.com/blog/2012/05/15/anatomy-of-reducer.html),
both by Rich Hickey.

Quickstart
==========

Here's how you can implement Rich Hickey's example ``((def xform (comp
(map inc) (filter even?)))`` using `transducers`.

```python
from functools import reduce
from transducers.compose import compose
from transducers.transducers import filtering, mapping

# A reducer for appending to a list.
def append(l, item):
    l.append(item)
    return l

# a transducer that maps "x + 1" over input values
inc = mapping(lambda x: x + 1)

# a transducer that filters out odd values
evens = filtering(lambda x: x % 2 == 0)

# a composite transducer of inc and evens -> inc(evens(seq))
odds = compose(inc, evens)

# Apply the composite transducer to the first 10 non-negative integers,
# building a list out of the results.
x = reduce(odds(append), range(10), list())

# See that you've indeed got [1, 3, 5, 7, 9]
assert x == list(range(1, 10, 2))
```

Testing
=======

`transducers` testing uses Python's standard `unittest` and `doctest` modules. To run the tests, go to the root of the project and run:

```
python -m unittest discover transducers/test
```

MMutation testing
----------------

If you want to run mutation testing using
[`mut.py`](https://bitbucket.org/khalas/mutpy), you can use an
invocation like this:

```
mut.py --target transducers --unit-test transducers.test.test_coroutines transducers.test.test_transducers
```

This can be a bit fiddly, and it's mostly useful for developers. But
it's fun to play with if you're interested in that kind of stuff. And
of course you need to install `mut.py` yourself.

Coroutines
==========

You may have noticed that there's a `coroutines` module in here as
well. It turns out that coroutines and transducers are similarly
composable, even to the degree that a single `compose()` function
works for both of them. So in the interest of pure curiousity I've
added a parallel coroutines modules to match the transducers. As with
transducers, I have no idea if this is practical or useful, but it
sure is pretty.
